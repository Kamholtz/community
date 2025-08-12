# 🎙️ Audio Recording Guide for VAD Testing

## Quick Recording Options

### Option 1: Using Built-in System Tools

**On Linux:**
```bash
# Using arecord (ALSA)
arecord -f cd -t wav -d 30 test_recording.wav

# Using pulseaudio
parecord --format=s16le --rate=16000 --channels=1 test_recording.wav
```

**On macOS:**
```bash
# Using sox (install with: brew install sox)
sox -t coreaudio default test_recording.wav trim 0 30

# Using ffmpeg (install with: brew install ffmpeg)  
ffmpeg -f avfoundation -i ":0" -t 30 -ar 16000 -ac 1 test_recording.wav
```

**On Windows:**
- Use built-in Voice Recorder app
- Or use Audacity (free): https://www.audacityteam.org/

### Option 2: Using Python (if dependencies work)

Create and run this simple recorder:

```python
import sounddevice as sd
import soundfile as sf
import time

# Recording parameters
duration = 30  # seconds
samplerate = 16000  # Hz
channels = 1

print("🎙️  Recording will start in 3 seconds...")
print("Instructions: Say 'the quick brown fox jumps over the lazy dog' 5 times")
print("Speak clearly with natural pauses between repetitions")

time.sleep(3)
print("🔴 Recording started!")

# Record audio
audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
sd.wait()  # Wait for recording to complete

# Save to file
sf.write('quick_fox_test.wav', audio, samplerate)
print("✅ Recording saved as 'quick_fox_test.wav'")
```

### Option 3: Online Audio Recorder

1. Go to https://online-voice-recorder.com/
2. Click "Record" 
3. Say the test phrase 5 times clearly
4. Download as WAV format
5. Convert to 16kHz mono if needed

## 📋 Recording Instructions

### What to Say
**Phrase**: "the quick brown fox jumps over the lazy dog"
**Repetitions**: Exactly 5 times
**Timing**: 2-3 second pause between each repetition

### Recording Quality Tips
- **Quiet environment** - minimize background noise
- **Consistent distance** - stay same distance from microphone  
- **Clear pronunciation** - speak each word distinctly
- **Natural pace** - don't rush or speak unnaturally slowly
- **Consistent volume** - maintain steady speaking volume

### Technical Requirements
- **Format**: WAV (preferred) or high-quality MP3
- **Sample Rate**: 16kHz (or 44.1kHz - can be converted)
- **Channels**: Mono (1 channel)
- **Duration**: 25-30 seconds total
- **Bit Depth**: 16-bit minimum

## 🔄 Audio Conversion

If your recording isn't in the right format:

### Using ffmpeg (recommended):
```bash
# Convert any audio file to optimal format
ffmpeg -i input_file.mp3 -ar 16000 -ac 1 -acodec pcm_s16le output_file.wav
```

### Using online converter:
1. Go to https://convertio.co/
2. Upload your audio file
3. Convert to WAV format
4. Set parameters: 16kHz, Mono, 16-bit

## 📊 Test Your Recording

Once you have a recording, test it with:

```bash
# Analyze the recording
python simple_vad_test.py your_recording.wav

# Or test with the actual system
# (replace the live microphone input with file input)
```

## 🎯 Expected Results

**Good Recording Indicators:**
- Clear, distinct pronunciation of each word
- Natural pauses between repetitions  
- Consistent audio levels throughout
- No background noise or distortion
- Exactly 5 complete phrase repetitions

**File Validation:**
- Duration: 25-35 seconds
- Size: ~800KB for 30 seconds at 16kHz
- Playback: Should sound clear when played back
- Waveform: Should show 5 distinct speech segments with silence gaps

## 🚀 Next Steps After Recording

1. **Test current system** with your recording
2. **Run parameter optimization** if testing framework available
3. **Compare results** with different VAD settings
4. **Fine-tune parameters** based on results
5. **Validate improvements** with additional test recordings

## 🛠️ Alternative: Use Existing Audio

If recording is difficult, you can also:
- Find sample "quick brown fox" audio online
- Use text-to-speech to generate test audio
- Record using your phone and transfer the file

The key is having **consistent, standardized test audio** for reliable comparisons between different VAD parameter configurations.