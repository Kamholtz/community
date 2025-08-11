import queue, sys, time, threading, numpy as np
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel
from collections import deque
import subprocess
import platform

# ---- config ----
SR = 16000
FRAME_MS = 20
PARTIAL_EVERY_SEC = 0.9
START_GATE_MS = 200
END_GATE_MS = 400
PAD_MS = 250
MODEL_SIZE = "small"  # tiny/ base/ small/ medium.en/ large-v3
DEVICE = "auto"       # "cuda" if available else "cpu"

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
vad = webrtcvad.Vad(2)
lookback = deque(maxlen=int(PAD_MS/FRAME_MS))
speech_started = False
speech_run = 0; nonspeech_run = 0
buf = bytearray()
last_partial_emit = 0.0

# ---- ASR ----
model = WhisperModel(MODEL_SIZE, device=DEVICE)
typed_so_far = ""  # committed to the target field

def transcribe_bytes(b, beam=1):
    # faster-whisper accepts numpy float32 or audio files; convert bytes to float32
    a = np.frombuffer(b, dtype=np.int16).astype(np.float32) / 32768.0
    segments, _ = model.transcribe(a, language=None, vad_filter=False,
                                   beam_size=beam, temperature=0.0,
                                   condition_on_previous_text=False)
    # merge text
    return "".join(seg.text for seg in segments).strip()

def diff_and_type(full_text):
    global typed_so_far
    # find delta to type
    if full_text.startswith(typed_so_far):
        delta = full_text[len(typed_so_far):]
        type_text(delta)
        typed_so_far = full_text
    else:
        # fallback: if mismatch (e.g., punctuation corrections), just type a space + rest
        # (or you could send backspaces to reconcile)
        type_text(" " + full_text)
        typed_so_far += " " + full_text

def loop():
    global speech_started, speech_run, nonspeech_run, buf, last_partial_emit
    start_stream()
    while True:
        frame = audio_q.get()
        lookback.append(frame)
        is_speech = vad.is_speech(frame, SR)
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
                    diff_and_type(partial_text)
        else:
            nonspeech_run += 1; speech_run = 0
            if speech_started and nonspeech_run*FRAME_MS >= END_GATE_MS:
                # FINAL decode (cleaner)
                final_audio = bytes(buf)
                buf.clear(); speech_started = False; lookback.clear()
                final_text = transcribe_bytes(final_audio, beam=5)
                diff_and_type(final_text)
                # add a trailing space so next partials don’t stick to the last word
                diff_and_type(typed_so_far + " ")

if __name__ == "__main__":
    loop()
