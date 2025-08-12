#!/usr/bin/env python3
"""
Enhanced Real-time VAD + Faster-Whisper Transcription
Containerized version with configuration support and improved architecture.
"""

import queue, sys, time, threading, numpy as np, logging, os, yaml
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel
from collections import deque
import subprocess
import platform
from pathlib import Path

# Configure logging (use temp directory for log file to avoid permission issues)
import tempfile
log_dir = tempfile.gettempdir()

# Clear any existing handlers to prevent duplicates
root_logger = logging.getLogger()
root_logger.handlers.clear()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)
logger = logging.getLogger(__name__)

class Config:
    """Configuration manager with environment variable override support."""
    
    def __init__(self, config_path='/app/config/config.yaml'):
        self.config = self.load_config(config_path)
        self.apply_env_overrides()
        
    def load_config(self, config_path):
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self.default_config()
            
    def default_config(self):
        """Default configuration values."""
        return {
            'audio': {'sample_rate': 16000, 'frame_duration_ms': 20},
            'vad': {'aggressiveness': 2, 'start_gate_ms': 200, 'end_gate_ms': 400, 'padding_ms': 250},
            'model': {'size': 'small', 'device': 'auto', 'compute_type': 'auto'},
            'transcription': {'partial_interval_sec': 0.9, 'partial_beam_size': 1, 'final_beam_size': 5,
                            'language': None, 'temperature': 0.0, 'condition_on_previous': False},
            'typing': {'backend': 'auto', 'delay_ms': 0, 'use_clipboard': False},
            'performance': {'max_chunk_duration_sec': 30, 'model_cache_size': 1},
            'debug': {'log_level': 'INFO', 'log_vad_activity': False, 'log_transcription_time': True, 'save_audio_chunks': False}
        }
    
    def apply_env_overrides(self):
        """Override config values with environment variables."""
        env_mappings = {
            'MODEL_SIZE': ('model', 'size'),
            'DEVICE': ('model', 'device'),
            'VAD_AGGRESSIVENESS': ('vad', 'aggressiveness'),
            'PARTIAL_INTERVAL': ('transcription', 'partial_interval_sec'),
            'START_GATE_MS': ('vad', 'start_gate_ms'),
            'END_GATE_MS': ('vad', 'end_gate_ms'),
            'PAD_MS': ('vad', 'padding_ms'),
        }
        
        for env_key, (section, key) in env_mappings.items():
            if env_key in os.environ:
                value = os.environ[env_key]
                # Type conversion
                if key in ['aggressiveness', 'start_gate_ms', 'end_gate_ms', 'padding_ms']:
                    value = int(value)
                elif key == 'partial_interval_sec':
                    value = float(value)
                    
                self.config[section][key] = value
                logger.info(f"Override {section}.{key} = {value} from env var {env_key}")
    
    def get(self, section, key, default=None):
        """Get configuration value."""
        return self.config.get(section, {}).get(key, default)

class AudioCapture:
    """Real-time audio capture with proper buffering."""
    
    def __init__(self, config):
        self.config = config
        self.sr = config.get('audio', 'sample_rate', 16000)
        self.frame_ms = config.get('audio', 'frame_duration_ms', 20)
        self.frame_size = int(self.sr * self.frame_ms / 1000)
        self.audio_queue = queue.Queue()
        self.stream = None
        
    def callback(self, indata, frames, time, status):
        """Audio callback function."""
        if status:
            logger.warning(f"Audio callback status: {status}")
        
        # Convert float32 [-1,1] to int16 bytes
        pcm16 = (np.clip(indata[:, 0], -1, 1) * 32767).astype(np.int16).tobytes()
        self.audio_queue.put(pcm16)
    
    def start(self):
        """Start audio capture."""
        logger.info(f"Starting audio capture: {self.sr}Hz, {self.frame_ms}ms frames")
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.sr,
            blocksize=self.frame_size,
            dtype='float32',
            callback=self.callback
        )
        self.stream.start()
    
    def stop(self):
        """Stop audio capture."""
        if self.stream:
            self.stream.stop()
            self.stream.close()

class TypingBackend:
    """Cross-platform text typing backend."""
    
    def __init__(self, config):
        self.config = config
        self.backend = config.get('typing', 'backend', 'auto')
        self.delay_ms = config.get('typing', 'delay_ms', 0)
        self.use_clipboard = config.get('typing', 'use_clipboard', False)
        self.os = platform.system().lower()
        
        if self.backend == 'auto':
            self.backend = self.detect_backend()
        
        logger.info(f"Using typing backend: {self.backend}")
    
    def detect_backend(self):
        """Auto-detect the best typing backend for the platform."""
        if "linux" in self.os:
            # Check for xdotool first, then wtype
            if self.command_exists('xdotool'):
                return 'xdotool'
            elif self.command_exists('wtype'):
                return 'wtype'
        elif "windows" in self.os:
            return 'keyboard'
        
        return 'fallback'
    
    def command_exists(self, command):
        """Check if a command exists on the system."""
        try:
            subprocess.run(['which', command], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def type_text(self, text):
        """Type text using the configured backend."""
        if not text:
            return
        
        try:
            if self.backend == 'xdotool':
                result = subprocess.run(['xdotool', 'type', '--delay', str(self.delay_ms), text], 
                                      check=True, capture_output=True, text=True)
            elif self.backend == 'wtype':
                result = subprocess.run(['wtype', text], check=True, capture_output=True, text=True)
            elif self.backend == 'keyboard':
                import keyboard
                keyboard.write(text, delay=self.delay_ms/1000.0)
            else:
                # Fallback: print to stdout
                sys.stdout.write(f"[TRANSCRIBED]: {text}")
                sys.stdout.flush()
                
        except subprocess.CalledProcessError as e:
            if "display" in e.stderr.lower():
                logger.warning(f"X11 display not accessible, falling back to stdout output")
                sys.stdout.write(f"[TRANSCRIBED]: {text}")
            else:
                logger.error(f"Failed to type text with {self.backend}: {e}")
                sys.stdout.write(f"[TRANSCRIBED]: {text}")
            sys.stdout.flush()
        except Exception as e:
            logger.error(f"Failed to type text with {self.backend}: {e}")
            # Fallback to stdout
            sys.stdout.write(f"[TRANSCRIBED]: {text}")
            sys.stdout.flush()

class VADProcessor:
    """Voice Activity Detection with smart chunking."""
    
    def __init__(self, config):
        self.config = config
        self.vad = webrtcvad.Vad(config.get('vad', 'aggressiveness', 2))
        
        # VAD parameters
        self.frame_ms = config.get('audio', 'frame_duration_ms', 20)
        self.start_gate_ms = config.get('vad', 'start_gate_ms', 200)
        self.end_gate_ms = config.get('vad', 'end_gate_ms', 400)
        self.pad_ms = config.get('vad', 'padding_ms', 250)
        
        # State tracking
        self.lookback = deque(maxlen=int(self.pad_ms / self.frame_ms))
        self.speech_started = False
        self.speech_run = 0
        self.nonspeech_run = 0
        self.buffer = bytearray()
        
        self.log_activity = config.get('debug', 'log_vad_activity', False)
        
    def process_frame(self, frame, sample_rate):
        """Process a single audio frame and return speech segments."""
        self.lookback.append(frame)
        is_speech = self.vad.is_speech(frame, sample_rate)
        
        if self.log_activity:
            logger.debug(f"VAD: {'SPEECH' if is_speech else 'SILENCE'}")
        
        speech_segment = None
        
        if is_speech:
            self.speech_run += 1
            self.nonspeech_run = 0
            
            if not self.speech_started and self.speech_run * self.frame_ms >= self.start_gate_ms:
                self.speech_started = True
                # Add lookback padding
                self.buffer.extend(b"".join(self.lookback))
                logger.debug("Speech started, added lookback")
            
            if self.speech_started:
                self.buffer.extend(frame)
        else:
            self.nonspeech_run += 1
            self.speech_run = 0
            
            if self.speech_started and self.nonspeech_run * self.frame_ms >= self.end_gate_ms:
                # End of speech detected
                speech_segment = bytes(self.buffer)
                self.reset()
                logger.debug(f"Speech ended, segment length: {len(speech_segment)} bytes")
        
        return speech_segment, self.buffer if self.speech_started else None
    
    def reset(self):
        """Reset VAD state."""
        self.buffer.clear()
        self.speech_started = False
        self.lookback.clear()
        self.speech_run = 0
        self.nonspeech_run = 0

class TranscriptionEngine:
    """Faster-whisper transcription engine."""
    
    def __init__(self, config):
        self.config = config
        self.model_size = config.get('model', 'size', 'small')
        self.device = config.get('model', 'device', 'auto')
        self.compute_type = config.get('model', 'compute_type', 'auto')
        
        # Transcription parameters
        self.language = config.get('transcription', 'language')
        self.temperature = config.get('transcription', 'temperature', 0.0)
        self.condition_on_previous = config.get('transcription', 'condition_on_previous', False)
        
        self.log_time = config.get('debug', 'log_transcription_time', True)
        
        logger.info(f"Loading whisper model: {self.model_size}, device: {self.device}")
        start_time = time.time()
        
        # Use HF_HOME if set, otherwise default to /app/models
        download_root = os.environ.get('HF_HOME', '/app/models')
        
        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
            download_root=download_root
        )
        
        load_time = time.time() - start_time
        logger.info(f"Model loaded in {load_time:.2f}s")
        
        # Text tracking for differential output
        self.typed_so_far = ""
    
    def transcribe_bytes(self, audio_bytes, beam_size=1):
        """Transcribe audio bytes to text."""
        if not audio_bytes:
            return ""
        
        start_time = time.time()
        
        # Convert bytes to float32 numpy array
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        
        segments, info = self.model.transcribe(
            audio_array,
            language=self.language or "en",  # Force English if not specified
            beam_size=beam_size,
            temperature=self.temperature,
            condition_on_previous_text=self.condition_on_previous,
            vad_filter=False  # We handle VAD externally
        )
        
        # Merge all segments
        text = "".join(seg.text for seg in segments).strip()
        
        if self.log_time:
            duration = time.time() - start_time
            audio_duration = len(audio_bytes) / (2 * 16000)  # 16-bit, 16kHz
            realtime_factor = audio_duration / duration if duration > 0 else 0
            logger.debug(f"Transcribed {audio_duration:.2f}s audio in {duration:.3f}s ({realtime_factor:.1f}x realtime)")
        
        return text
    
    def get_differential_text(self, full_text):
        """Get only the new text to type."""
        if full_text.startswith(self.typed_so_far):
            delta = full_text[len(self.typed_so_far):]
            self.typed_so_far = full_text
            return delta
        else:
            # Fallback for mismatches - add space and continue
            delta = " " + full_text
            self.typed_so_far += delta
            return delta
    
    def reset_context(self):
        """Reset the typing context (e.g., for new sessions)."""
        self.typed_so_far = ""

class RealtimeTranscriber:
    """Main real-time transcription coordinator."""
    
    def __init__(self, config_path='/app/config/config.yaml'):
        self.config = Config(config_path)
        self.setup_logging()
        
        self.audio = AudioCapture(self.config)
        self.vad = VADProcessor(self.config)
        self.engine = TranscriptionEngine(self.config)
        self.typing = TypingBackend(self.config)
        
        self.partial_interval = self.config.get('transcription', 'partial_interval_sec', 0.9)
        self.partial_beam = self.config.get('transcription', 'partial_beam_size', 1)
        self.final_beam = self.config.get('transcription', 'final_beam_size', 5)
        
        self.last_partial_time = 0.0
        self.running = False
        
    def setup_logging(self):
        """Configure logging based on config."""
        log_level = self.config.get('debug', 'log_level', 'INFO')
        logging.getLogger().setLevel(getattr(logging, log_level))
        
    def run(self):
        """Main transcription loop."""
        logger.info("Starting real-time transcription")
        logger.info(f"Model: {self.engine.model_size}, Device: {self.engine.device}")
        logger.info(f"VAD: aggressiveness={self.config.get('vad', 'aggressiveness', 2)}, gates={self.vad.start_gate_ms}/{self.vad.end_gate_ms}ms")
        
        self.running = True
        self.audio.start()
        
        try:
            while self.running:
                # Get audio frame
                frame = self.audio.audio_queue.get()
                
                # Process with VAD
                speech_segment, partial_buffer = self.vad.process_frame(frame, self.audio.sr)
                
                # Handle completed speech segment
                if speech_segment:
                    logger.debug("Processing final speech segment")
                    final_text = self.engine.transcribe_bytes(speech_segment, self.final_beam)
                    if final_text:
                        delta = self.engine.get_differential_text(final_text)
                        if delta:
                            self.typing.type_text(delta)
                            logger.info(f"Final: '{delta.strip()}'")
                        
                        # Add trailing space for next utterance and reset context
                        self.typing.type_text(" ")
                        self.engine.reset_context()
                
                # Handle partial transcription
                elif partial_buffer and len(partial_buffer) > self.audio.sr * 2 * 0.5:  # Min 0.5s of audio
                    current_time = time.time()
                    if current_time - self.last_partial_time >= self.partial_interval:
                        self.last_partial_time = current_time
                        
                        logger.debug("Processing partial speech segment")
                        partial_text = self.engine.transcribe_bytes(bytes(partial_buffer), self.partial_beam)
                        if partial_text:
                            delta = self.engine.get_differential_text(partial_text)
                            if delta:
                                self.typing.type_text(delta)
                                logger.info(f"Partial: '{delta.strip()}'")
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"Transcription error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop transcription."""
        logger.info("Stopping real-time transcription")
        self.running = False
        self.audio.stop()

def main():
    """Main entry point."""
    logger.info("Real-time VAD + Faster-Whisper Transcription Starting...")
    
    # Check GPU availability
    try:
        import torch
        gpu_available = torch.cuda.is_available()
        if gpu_available:
            gpu_name = torch.cuda.get_device_name(0)
            logger.info(f"GPU available: {gpu_name}")
        else:
            logger.info("GPU not available, using CPU")
    except ImportError:
        logger.info("PyTorch not available for GPU check")
    
    try:
        transcriber = RealtimeTranscriber()
        transcriber.run()
    except Exception as e:
        logger.error(f"Failed to start transcription: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()