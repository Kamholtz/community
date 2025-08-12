import queue, sys, time, threading, numpy as np, os
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel
from collections import deque
import subprocess
import platform
from text_differ_v2 import StreamingASRTextDiffer

# ---- config ----
SR = 16000
FRAME_MS = 20
PARTIAL_EVERY_SEC = 0.9
START_GATE_MS = int(os.environ.get('START_GATE_MS', 200))
END_GATE_MS = int(os.environ.get('END_GATE_MS', 800))  # Optimized for better segmentation
PAD_MS = int(os.environ.get('PAD_MS', 250))
MODEL_SIZE = "small"  # tiny/ base/ small/ medium.en/ large-v3
DEVICE = "auto"       # "cuda" if available else "cpu"
VOLUME_THRESHOLD = 0.008  # Optimized volume threshold for better sensitivity

# ---- typing backends ----
OS = platform.system().lower()
def type_text(delta):
    if not delta: return
    
    if "linux" in OS:
        # Prefer xdotool (X11). On Wayland try wtype.
        try:
            subprocess.run(["xdotool", "type", "--delay", "0", delta], check=True)
        except Exception:
            subprocess.run(["wtype", delta])
    elif "windows" in OS:
        import keyboard
        keyboard.write(delta, delay=0)
    else:
        # Fallback: print to stdout
        sys.stdout.write(delta); sys.stdout.flush()

# ---- audio capture ----
BYTES_PER_FRAME = int(SR * FRAME_MS / 1000) * 2  # 16-bit mono
audio_q = queue.Queue()

def audio_cb(indata, frames, t, status):
    if status: pass
    # convert float32 [-1,1] to int16 bytes
    pcm16 = (np.clip(indata[:, 0], -1, 1) * 32767).astype(np.int16).tobytes()
    audio_q.put(pcm16)

def start_stream():
    sd.InputStream(channels=1, samplerate=SR, blocksize=int(SR*FRAME_MS/1000),
                   dtype="float32", callback=audio_cb).start()

# ---- VAD chunker ----
vad = webrtcvad.Vad(1)  # Optimized: less aggressive VAD
lookback = deque(maxlen=int(PAD_MS/FRAME_MS))
speech_started = False
speech_run = 0; nonspeech_run = 0
buf = bytearray()
last_partial_emit = 0.0

# ---- ASR ----
download_root = os.environ.get('HF_HOME', '/app/models')
model = WhisperModel(MODEL_SIZE, device=DEVICE, download_root=download_root)
text_differ = StreamingASRTextDiffer()  # Handle differential typing

def transcribe_bytes(b, beam=1):
    # faster-whisper accepts numpy float32 or audio files; convert bytes to float32
    a = np.frombuffer(b, dtype=np.int16).astype(np.float32) / 32768.0
    segments, _ = model.transcribe(a, language=None, vad_filter=False,
                                   beam_size=beam, temperature=0.0,
                                   condition_on_previous_text=False)
    # merge text
    return "".join(seg.text for seg in segments).strip()

def handle_partial_transcription(full_text):
    """Handle partial transcription results during utterance."""
    print(f"[PARTIAL_ASR] '{full_text}'")
    delta = text_differ.process_partial_hypothesis(full_text)
    if delta:
        print(f"[PARTIAL_OUT] '{delta}'")
    type_text(delta)

def handle_final_transcription(full_text):
    """Handle final transcription at end of utterance."""
    print(f"[FINAL_ASR] '{full_text}'")
    delta = text_differ.process_final_hypothesis(full_text)
    if delta:
        print(f"[FINAL_OUT] '{delta}'")
    type_text(delta)

def loop():
    global speech_started, speech_run, nonspeech_run, buf, last_partial_emit
    start_stream()
    while True:
        frame = audio_q.get()
        lookback.append(frame)
        
        # Check volume threshold in addition to VAD
        audio_data = np.frombuffer(frame, dtype=np.int16).astype(np.float32) / 32768.0
        rms_volume = np.sqrt(np.mean(audio_data ** 2))
        
        is_speech = vad.is_speech(frame, SR) and rms_volume > VOLUME_THRESHOLD
        if is_speech:
            speech_run += 1; nonspeech_run = 0
            if not speech_started and speech_run*FRAME_MS >= START_GATE_MS:
                speech_started = True
                # prepend lookback padding
                buf.extend(b"".join(lookback))
            if speech_started:
                buf.extend(frame)
                now = time.time()
                if now - last_partial_emit >= PARTIAL_EVERY_SEC and len(buf) >= SR*2*0.5:
                    last_partial_emit = now
                    # PARTIAL decode (fast)
                    partial_text = transcribe_bytes(bytes(buf), beam=1)
                    handle_partial_transcription(partial_text)
        else:
            nonspeech_run += 1; speech_run = 0
            if speech_started and nonspeech_run*FRAME_MS >= END_GATE_MS:
                # FINAL decode (cleaner)
                final_audio = bytes(buf)
                buf.clear(); speech_started = False; lookback.clear()
                final_text = transcribe_bytes(final_audio, beam=5)
                handle_final_transcription(final_text)
                # add a trailing space and reset context for next utterance
                space = text_differ.end_utterance()
                type_text(space)

def check_microphone():
    """Test microphone setup and show available devices"""
    print("=== Microphone Setup Check ===")
    try:
        devices = sd.query_devices()
        print("Available audio devices:")
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"  {i}: {device['name']} (input channels: {device['max_input_channels']})")
        
        default_input = sd.default.device[0]
        if default_input is not None:
            default_device = devices[default_input]
            print(f"\nDefault input device: {default_device['name']}")
        else:
            print("\nNo default input device found!")
            return False
        
        print("\nTesting microphone for 2 seconds...")
        test_audio = sd.rec(int(2 * SR), samplerate=SR, channels=1, dtype='float32')
        sd.wait()
        
        rms_volume = np.sqrt(np.mean(test_audio ** 2))
        print(f"Recorded RMS volume: {rms_volume:.6f}")
        print(f"Volume threshold: {VOLUME_THRESHOLD}")
        
        if rms_volume > VOLUME_THRESHOLD:
            print("✅ Microphone appears to be working and above threshold")
        else:
            print("⚠️  Warning: Recorded volume is below threshold - may not detect speech")
            print("   Try speaking louder or adjusting VOLUME_THRESHOLD")
        
        print("=== End Microphone Check ===\n")
        return True
        
    except Exception as e:
        print(f"❌ Error testing microphone: {e}")
        return False

if __name__ == "__main__":
    # Print actual device being used by model
    actual_device = model.device if hasattr(model, 'device') else "unknown"
    print(f"Model: {MODEL_SIZE}, Configured Device: {DEVICE}, Actual Device: {actual_device}")
    print(f"VAD: aggressiveness=1, gates={START_GATE_MS}/{END_GATE_MS}ms")
    print(f"Volume threshold: {VOLUME_THRESHOLD}")
    print()
    
    if check_microphone():
        # Auto-start in Docker, otherwise wait for input
        if os.path.exists('/.dockerenv'):
            print("Running in Docker - auto-starting transcription...")
        else:
            input("Press Enter to start transcription or Ctrl+C to exit...")
        loop()
    else:
        print("Microphone check failed. Please fix audio setup and try again.")
