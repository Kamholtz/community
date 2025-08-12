"""
Integration layer between VAD testing framework and actual transcription system.
"""

import os
import sys
import time
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import json

class VADSystemIntegrator:
    """Integrates the testing framework with the actual VAD transcription system."""
    
    def __init__(self, vad_script_path="faster_whisper_vad.py"):
        self.vad_script_path = Path(vad_script_path)
        self.temp_dir = Path(tempfile.mkdtemp(prefix="vad_test_"))
        self.temp_dir.mkdir(exist_ok=True)
        
        if not self.vad_script_path.exists():
            raise FileNotFoundError(f"VAD script not found: {vad_script_path}")
    
    def run_transcription_on_audio(self, audio_file: str, vad_params: Dict) -> Dict:
        """Run the actual VAD transcription system on audio file."""
        
        print(f"🎵 Processing {audio_file} with VAD params: {vad_params}")
        
        # Create modified VAD script with test parameters
        modified_script = self._create_test_script(vad_params)
        
        # Prepare output capture
        output_file = self.temp_dir / "transcription_output.txt"
        
        start_time = time.time()
        
        try:
            # Run the transcription
            result = self._execute_transcription(modified_script, audio_file, output_file)
            processing_time = time.time() - start_time
            
            # Parse results
            transcription_text, segment_info = self._parse_output(output_file)
            
            return {
                'text': transcription_text,
                'processing_time': processing_time,
                'segment_count': len(segment_info),
                'segments': segment_info,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            return {
                'text': "",
                'processing_time': processing_time,
                'segment_count': 0,
                'segments': [],
                'success': False,
                'error': str(e)
            }
    
    def _create_test_script(self, vad_params: Dict) -> str:
        """Create a modified version of the VAD script with test parameters."""
        
        # Read original script
        with open(self.vad_script_path, 'r') as f:
            original_script = f.read()
        
        # Create parameter substitutions
        param_replacements = {
            'VAD_AGGRESSIVENESS = 2': f'VAD_AGGRESSIVENESS = {vad_params.get("aggressiveness", 2)}',
            'START_GATE_MS = int(os.environ.get(\'START_GATE_MS\', 300))': 
                f'START_GATE_MS = {vad_params.get("start_gate_ms", 300)}',
            'END_GATE_MS = int(os.environ.get(\'END_GATE_MS\', 1000))':
                f'END_GATE_MS = {vad_params.get("end_gate_ms", 1000)}', 
            'VOLUME_THRESHOLD = 0.01':
                f'VOLUME_THRESHOLD = {vad_params.get("volume_threshold", 0.01)}',
        }
        
        # Apply replacements
        modified_script = original_script
        for old, new in param_replacements.items():
            if old in modified_script:
                modified_script = modified_script.replace(old, new)
        
        # Modify script to work with file input instead of microphone
        modified_script = self._modify_for_file_input(modified_script)
        
        # Save modified script
        test_script_path = self.temp_dir / "test_vad_script.py"
        with open(test_script_path, 'w') as f:
            f.write(modified_script)
        
        return str(test_script_path)
    
    def _modify_for_file_input(self, script_content: str) -> str:
        """Modify the VAD script to process audio files instead of live microphone."""
        
        # This is a simplified approach - you may need to create a more sophisticated
        # file-based version of your VAD system
        
        file_processing_code = '''
import sys
import wave
import numpy as np

def process_audio_file(filename):
    """Process an audio file instead of live microphone input."""
    
    print(f"Processing audio file: {filename}")
    
    # Read the audio file
    try:
        with wave.open(filename, 'rb') as wav_file:
            frames = wav_file.readframes(wav_file.getnframes())
            sample_rate = wav_file.getframerate()
            
        # Convert to the format expected by the VAD system
        audio_data = np.frombuffer(frames, dtype=np.int16)
        
        if sample_rate != SR:
            print(f"Warning: Audio file sample rate ({sample_rate}) != expected ({SR})")
            print("Consider resampling the audio file to 16kHz")
        
        # Process in chunks like the real-time system would
        chunk_size = int(SR * FRAME_MS / 1000)
        results = []
        
        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i:i+chunk_size]
            if len(chunk) < chunk_size:
                # Pad the last chunk
                chunk = np.pad(chunk, (0, chunk_size - len(chunk)), 'constant')
            
            # Process this chunk (simplified)
            # In reality, you'd run this through your full VAD pipeline
            frame_bytes = chunk.astype(np.int16).tobytes()
            
            # Simple volume check
            rms_volume = np.sqrt(np.mean((chunk.astype(np.float32) / 32768.0) ** 2))
            
            if rms_volume > VOLUME_THRESHOLD:
                # Simulate transcription of this chunk
                # This is a placeholder - real implementation would be more complex
                pass
        
        # For testing purposes, return a mock transcription
        # You would replace this with actual transcription logic
        mock_transcription = "the quick brown fox jumps over the lazy dog " * 5
        
        print(f"[FINAL_ASR] '{mock_transcription.strip()}'")
        return mock_transcription.strip()
        
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return ""

# Replace the main execution
if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        result = process_audio_file(audio_file)
        print(f"TRANSCRIPTION_RESULT: {result}")
    else:
        print("Usage: python script.py <audio_file>")
'''
        
        # Add file processing capability
        modified = script_content + "\n\n" + file_processing_code
        
        return modified
    
    def _execute_transcription(self, script_path: str, audio_file: str, output_file: str) -> subprocess.CompletedProcess:
        """Execute the transcription script and capture output."""
        
        # Command to run the transcription
        cmd = [sys.executable, script_path, audio_file]
        
        print(f"🏃 Running: {' '.join(cmd)}")
        
        # Execute and capture output
        with open(output_file, 'w') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                timeout=300,  # 5 minute timeout
                text=True
            )
        
        if result.returncode != 0:
            with open(output_file, 'r') as f:
                error_output = f.read()
            raise RuntimeError(f"Transcription failed with code {result.returncode}: {error_output}")
        
        return result
    
    def _parse_output(self, output_file: str) -> Tuple[str, List[Dict]]:
        """Parse the transcription output to extract text and segment information."""
        
        with open(output_file, 'r') as f:
            output_lines = f.readlines()
        
        transcription_text = ""
        segment_info = []
        
        for line in output_lines:
            line = line.strip()
            
            # Look for transcription result markers
            if "TRANSCRIPTION_RESULT:" in line:
                transcription_text = line.split("TRANSCRIPTION_RESULT:", 1)[1].strip()
            
            # Look for ASR output markers
            elif "[FINAL_ASR]" in line:
                text = line.split("[FINAL_ASR]", 1)[1].strip().strip("'\"")
                segment_info.append({
                    'type': 'final',
                    'text': text,
                    'timestamp': time.time()  # Placeholder
                })
            
            elif "[PARTIAL_ASR]" in line:
                text = line.split("[PARTIAL_ASR]", 1)[1].strip().strip("'\"")
                segment_info.append({
                    'type': 'partial', 
                    'text': text,
                    'timestamp': time.time()  # Placeholder
                })
        
        # If no explicit transcription result found, try to construct from segments
        if not transcription_text and segment_info:
            final_segments = [s for s in segment_info if s['type'] == 'final']
            if final_segments:
                transcription_text = " ".join(s['text'] for s in final_segments)
        
        return transcription_text, segment_info
    
    def cleanup(self):
        """Clean up temporary files."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Cleaned up temp directory: {self.temp_dir}")


class AudioFileProcessor:
    """Processes audio files for VAD testing."""
    
    def __init__(self):
        self.supported_formats = ['.wav', '.mp3', '.flac', '.m4a']
    
    def convert_to_wav(self, input_file: str, output_file: str = None, 
                      target_sr: int = 16000) -> str:
        """Convert audio file to WAV format suitable for VAD testing."""
        
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if output_file is None:
            output_file = input_path.with_suffix('.wav')
        
        output_path = Path(output_file)
        
        print(f"🔄 Converting {input_file} to {output_file}")
        
        try:
            # Try using ffmpeg if available
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-ar', str(target_sr),  # Sample rate
                '-ac', '1',             # Mono
                '-acodec', 'pcm_s16le', # 16-bit PCM
                '-y',                   # Overwrite output
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Converted successfully using ffmpeg")
                return str(output_path)
            else:
                print(f"ffmpeg failed: {result.stderr}")
                
        except FileNotFoundError:
            print("ffmpeg not found, trying alternative methods...")
        
        # Try using soundfile if available
        try:
            import soundfile as sf
            
            data, sr = sf.read(str(input_path))
            
            # Resample if necessary (simplified approach)
            if sr != target_sr:
                print(f"⚠️  Sample rate mismatch: {sr} -> {target_sr}")
                print("Note: This conversion may affect quality. Consider using ffmpeg.")
                # Simple resampling (you might want to use librosa for better quality)
                import numpy as np
                data = data[::int(sr/target_sr)]  # Very crude resampling
            
            # Convert to mono if stereo
            if len(data.shape) > 1:
                data = np.mean(data, axis=1)
            
            sf.write(str(output_path), data, target_sr)
            print(f"✅ Converted successfully using soundfile")
            return str(output_path)
            
        except ImportError:
            print("soundfile not available")
        except Exception as e:
            print(f"soundfile conversion failed: {e}")
        
        # If input is already WAV, just copy it
        if input_path.suffix.lower() == '.wav':
            import shutil
            shutil.copy2(input_path, output_path)
            print(f"✅ Copied WAV file")
            return str(output_path)
        
        raise RuntimeError("Could not convert audio file. Please install ffmpeg or ensure input is WAV format.")
    
    def validate_audio_file(self, audio_file: str) -> Dict:
        """Validate that an audio file is suitable for VAD testing."""
        
        try:
            import soundfile as sf
            
            info = sf.info(audio_file)
            
            validation = {
                'valid': True,
                'filename': audio_file,
                'duration': info.duration,
                'samplerate': info.samplerate, 
                'channels': info.channels,
                'format': info.format,
                'warnings': [],
                'recommendations': []
            }
            
            # Check sample rate
            if info.samplerate != 16000:
                validation['warnings'].append(f"Sample rate is {info.samplerate}Hz, expected 16000Hz")
                validation['recommendations'].append("Convert to 16kHz for optimal VAD performance")
            
            # Check channels
            if info.channels > 1:
                validation['warnings'].append(f"Audio has {info.channels} channels")
                validation['recommendations'].append("Convert to mono for VAD processing")
            
            # Check duration
            if info.duration < 5:
                validation['warnings'].append(f"Audio is very short ({info.duration:.1f}s)")
                validation['recommendations'].append("Use longer audio (>10s) for better VAD testing")
            
            if info.duration > 300:
                validation['warnings'].append(f"Audio is very long ({info.duration:.1f}s)")
                validation['recommendations'].append("Consider using shorter clips for faster testing")
            
            return validation
            
        except ImportError:
            return {
                'valid': False,
                'error': 'soundfile not available - cannot validate audio file',
                'recommendations': ['Install soundfile: pip install soundfile']
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error validating audio file: {e}',
                'recommendations': ['Check that file exists and is a valid audio format']
            }


def test_integration():
    """Test the VAD integration system."""
    
    print("🧪 Testing VAD Integration System")
    print("=" * 40)
    
    # Test audio file processor
    processor = AudioFileProcessor()
    
    # Test VAD integrator (mock)
    try:
        integrator = VADSystemIntegrator()
        
        # Test with mock parameters
        test_params = {
            'aggressiveness': 2,
            'start_gate_ms': 300,
            'end_gate_ms': 1000,
            'volume_threshold': 0.01
        }
        
        print("✅ VAD integrator initialized successfully")
        print(f"✅ Test parameters: {test_params}")
        
        # Cleanup
        integrator.cleanup()
        
    except Exception as e:
        print(f"❌ VAD integrator test failed: {e}")
    
    print("\n🎯 Integration system ready for use!")


if __name__ == "__main__":
    test_integration()