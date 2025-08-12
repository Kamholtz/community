#!/usr/bin/env python3
"""
Audio Quality Analyzer for VAD Testing
Analyzes audio files for quality metrics that affect ASR performance.
"""

import os
import wave
import numpy as np
from pathlib import Path
import json

class AudioQualityAnalyzer:
    """Analyze audio file quality for ASR optimization."""
    
    def __init__(self):
        self.target_sample_rate = 16000
        self.target_channels = 1
        self.optimal_rms_range = (0.01, 0.1)  # Optimal RMS volume range
    
    def analyze_audio_file(self, audio_file):
        """Comprehensive audio file analysis."""
        
        if not os.path.exists(audio_file):
            return {"error": f"Audio file not found: {audio_file}"}
        
        try:
            results = {
                "file_path": audio_file,
                "file_size_bytes": os.path.getsize(audio_file),
                "analysis_timestamp": str(np.datetime64('now')),
            }
            
            # Basic file properties
            results.update(self._analyze_file_properties(audio_file))
            
            # Audio content analysis
            if audio_file.lower().endswith('.wav'):
                results.update(self._analyze_wav_content(audio_file))
            
            # Quality assessment
            results.update(self._assess_quality(results))
            
            # Recommendations
            results["recommendations"] = self._generate_audio_recommendations(results)
            
            return results
            
        except Exception as e:
            return {"error": f"Audio analysis failed: {str(e)}"}
    
    def _analyze_file_properties(self, audio_file):
        """Analyze basic file properties."""
        
        file_size = os.path.getsize(audio_file)
        
        # Estimate properties based on file size for WAV
        # 16kHz mono 16-bit WAV: ~32KB per second
        estimated_duration = file_size / 32000
        
        return {
            "file_extension": Path(audio_file).suffix.lower(),
            "estimated_duration_seconds": estimated_duration,
            "size_quality": "good" if file_size > 200000 else "poor",  # >6 seconds
        }
    
    def _analyze_wav_content(self, audio_file):
        """Analyze WAV file audio content."""
        
        try:
            with wave.open(audio_file, 'rb') as wav_file:
                # Basic WAV properties
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                n_frames = wav_file.getnframes()
                duration = n_frames / sample_rate
                
                # Read audio data
                frames = wav_file.readframes(n_frames)
                
                # Convert to numpy array
                if sample_width == 2:  # 16-bit
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                elif sample_width == 4:  # 32-bit
                    audio_data = np.frombuffer(frames, dtype=np.int32)
                else:
                    audio_data = np.frombuffer(frames, dtype=np.uint8)
                
                # Handle multi-channel
                if channels > 1:
                    audio_data = audio_data.reshape(-1, channels)
                    audio_data = audio_data[:, 0]  # Take first channel
                
                # Normalize to float32 [-1, 1]
                if sample_width == 2:
                    audio_float = audio_data.astype(np.float32) / 32768.0
                else:
                    audio_float = audio_data.astype(np.float32) / (2**(sample_width*8-1))
                
                # Analyze audio content
                content_analysis = self._analyze_audio_content(audio_float, sample_rate)
                
                return {
                    "sample_rate": sample_rate,
                    "channels": channels,
                    "sample_width_bytes": sample_width,
                    "duration_seconds": duration,
                    "total_samples": len(audio_data),
                    "sample_rate_optimal": sample_rate == self.target_sample_rate,
                    "channels_optimal": channels == self.target_channels,
                    **content_analysis
                }
                
        except Exception as e:
            return {"wav_analysis_error": str(e)}
    
    def _analyze_audio_content(self, audio_data, sample_rate):
        """Analyze the actual audio content."""
        
        # Volume analysis
        rms_volume = np.sqrt(np.mean(audio_data ** 2))
        max_amplitude = np.max(np.abs(audio_data))
        peak_to_rms_ratio = max_amplitude / rms_volume if rms_volume > 0 else 0
        
        # Dynamic range
        dynamic_range = 20 * np.log10(max_amplitude / (np.mean(np.abs(audio_data)) + 1e-10))
        
        # Silence detection
        silence_threshold = 0.001
        silence_frames = np.sum(np.abs(audio_data) < silence_threshold)
        silence_percentage = silence_frames / len(audio_data) * 100
        
        # Speech activity detection (simple energy-based)
        frame_size = int(0.025 * sample_rate)  # 25ms frames
        hop_size = int(0.010 * sample_rate)    # 10ms hop
        
        speech_frames = 0
        total_frames = 0
        
        for i in range(0, len(audio_data) - frame_size, hop_size):
            frame = audio_data[i:i + frame_size]
            energy = np.sum(frame ** 2)
            
            if energy > silence_threshold:
                speech_frames += 1
            total_frames += 1
        
        speech_activity_ratio = speech_frames / total_frames if total_frames > 0 else 0
        
        # Clipping detection
        clipping_threshold = 0.99
        clipped_samples = np.sum(np.abs(audio_data) >= clipping_threshold)
        clipping_percentage = clipped_samples / len(audio_data) * 100
        
        # Frequency analysis (simplified)
        if len(audio_data) > 1024:
            fft = np.fft.fft(audio_data[:8192])  # Use first 8192 samples
            freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
            magnitude = np.abs(fft)
            
            # Find dominant frequency
            dominant_freq_idx = np.argmax(magnitude[1:len(magnitude)//2]) + 1
            dominant_frequency = abs(freqs[dominant_freq_idx])
            
            # Energy distribution
            low_freq_energy = np.sum(magnitude[1:len(magnitude)//8])  # 0-2kHz
            mid_freq_energy = np.sum(magnitude[len(magnitude)//8:len(magnitude)//4])  # 2-4kHz  
            high_freq_energy = np.sum(magnitude[len(magnitude)//4:len(magnitude)//2])  # 4-8kHz
            
            total_energy = low_freq_energy + mid_freq_energy + high_freq_energy
            
            freq_distribution = {
                "low_freq_ratio": low_freq_energy / total_energy if total_energy > 0 else 0,
                "mid_freq_ratio": mid_freq_energy / total_energy if total_energy > 0 else 0,
                "high_freq_ratio": high_freq_energy / total_energy if total_energy > 0 else 0,
            }
        else:
            dominant_frequency = 0
            freq_distribution = {"low_freq_ratio": 0, "mid_freq_ratio": 0, "high_freq_ratio": 0}
        
        return {
            "rms_volume": float(rms_volume),
            "max_amplitude": float(max_amplitude),
            "peak_to_rms_ratio": float(peak_to_rms_ratio),
            "dynamic_range_db": float(dynamic_range),
            "silence_percentage": float(silence_percentage),
            "speech_activity_ratio": float(speech_activity_ratio),
            "clipping_percentage": float(clipping_percentage),
            "dominant_frequency_hz": float(dominant_frequency),
            "volume_optimal": self.optimal_rms_range[0] <= rms_volume <= self.optimal_rms_range[1],
            **freq_distribution
        }
    
    def _assess_quality(self, analysis_results):
        """Assess overall audio quality."""
        
        quality_score = 100
        issues = []
        
        # Sample rate check
        if not analysis_results.get("sample_rate_optimal", False):
            quality_score -= 15
            issues.append("Non-optimal sample rate")
        
        # Channels check  
        if not analysis_results.get("channels_optimal", False):
            quality_score -= 10
            issues.append("Non-optimal channel count")
        
        # Volume check
        if not analysis_results.get("volume_optimal", False):
            quality_score -= 20
            issues.append("Suboptimal volume level")
        
        # Clipping check
        clipping = analysis_results.get("clipping_percentage", 0)
        if clipping > 1.0:
            quality_score -= 25
            issues.append("Audio clipping detected")
        elif clipping > 0.1:
            quality_score -= 10
            issues.append("Minor audio clipping")
        
        # Silence check
        silence = analysis_results.get("silence_percentage", 0)
        if silence > 70:
            quality_score -= 20
            issues.append("Too much silence")
        elif silence < 10:
            quality_score -= 10
            issues.append("Too little silence (may affect VAD)")
        
        # Speech activity check
        speech_ratio = analysis_results.get("speech_activity_ratio", 0)
        if speech_ratio < 0.3:
            quality_score -= 15
            issues.append("Low speech activity")
        
        return {
            "audio_quality_score": max(0, quality_score),
            "quality_issues": issues,
            "quality_grade": self._get_quality_grade(max(0, quality_score))
        }
    
    def _get_quality_grade(self, score):
        """Convert quality score to letter grade."""
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Acceptable)"
        elif score >= 60:
            return "D (Poor)"
        else:
            return "F (Unusable)"
    
    def _generate_audio_recommendations(self, analysis_results):
        """Generate recommendations for improving audio quality."""
        
        recommendations = []
        
        # Sample rate recommendations
        if not analysis_results.get("sample_rate_optimal", False):
            current_sr = analysis_results.get("sample_rate", "unknown")
            recommendations.append(f"Convert audio from {current_sr}Hz to 16kHz for optimal ASR performance")
        
        # Volume recommendations
        rms_volume = analysis_results.get("rms_volume", 0)
        if rms_volume < self.optimal_rms_range[0]:
            recommendations.append(f"Audio too quiet (RMS: {rms_volume:.4f}) - increase recording volume or apply gain")
        elif rms_volume > self.optimal_rms_range[1]:
            recommendations.append(f"Audio too loud (RMS: {rms_volume:.4f}) - reduce recording volume to prevent clipping")
        
        # Clipping recommendations
        if analysis_results.get("clipping_percentage", 0) > 0:
            recommendations.append("Audio clipping detected - reduce input gain and re-record")
        
        # Silence recommendations  
        silence_pct = analysis_results.get("silence_percentage", 0)
        if silence_pct > 50:
            recommendations.append("Excessive silence detected - trim audio or check microphone sensitivity")
        
        # Speech activity recommendations
        speech_ratio = analysis_results.get("speech_activity_ratio", 0)
        if speech_ratio < 0.4:
            recommendations.append("Low speech activity - check microphone placement and background noise")
        
        # File format recommendations
        if analysis_results.get("file_extension") != ".wav":
            recommendations.append("Convert to WAV format for best compatibility")
        
        return recommendations

def analyze_test_audio_directory(directory="test_audio"):
    """Analyze all audio files in the test directory."""
    
    if not os.path.exists(directory):
        print(f"❌ Directory not found: {directory}")
        return
    
    analyzer = AudioQualityAnalyzer()
    
    audio_files = []
    for ext in [".wav", ".mp3", ".flac", ".m4a"]:
        audio_files.extend(Path(directory).glob(f"*{ext}"))
    
    if not audio_files:
        print(f"📂 No audio files found in {directory}/")
        return
    
    print(f"🎵 Analyzing {len(audio_files)} audio files...")
    print("=" * 60)
    
    all_results = {}
    
    for audio_file in audio_files:
        print(f"\n🔍 Analyzing: {audio_file.name}")
        
        results = analyzer.analyze_audio_file(str(audio_file))
        all_results[str(audio_file)] = results
        
        if "error" in results:
            print(f"   ❌ {results['error']}")
            continue
        
        print(f"   Quality Score: {results.get('audio_quality_score', 0):.1f}/100")
        print(f"   Grade: {results.get('quality_grade', 'Unknown')}")
        print(f"   Duration: {results.get('duration_seconds', 0):.1f}s")
        print(f"   RMS Volume: {results.get('rms_volume', 0):.4f}")
        
        if results.get("quality_issues"):
            print("   ⚠️  Issues:")
            for issue in results["quality_issues"][:3]:
                print(f"      - {issue}")
        
        if results.get("recommendations"):
            print("   💡 Top recommendation:")
            print(f"      - {results['recommendations'][0]}")
    
    # Save comprehensive report
    report_file = "audio_quality_report.json"
    with open(report_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\n📊 Full analysis saved to: {report_file}")
    
    return all_results

def main():
    """Main function for audio quality analysis."""
    
    print("🎵 Audio Quality Analyzer for VAD Testing")
    print("=" * 50)
    
    # Analyze test audio directory
    analyze_test_audio_directory()
    
    # Also analyze any specific files mentioned
    test_files = ["test_audio/quick_fox_test.wav", "quick_fox_test.wav"]
    
    analyzer = AudioQualityAnalyzer()
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n🎯 Detailed analysis of {test_file}:")
            results = analyzer.analyze_audio_file(test_file)
            
            if "error" not in results:
                print(f"   📊 Quality Score: {results.get('audio_quality_score', 0):.1f}/100")
                print(f"   🎓 Grade: {results.get('quality_grade', 'Unknown')}")
                print(f"   ⏱️  Duration: {results.get('duration_seconds', 0):.1f} seconds")
                print(f"   🔊 RMS Volume: {results.get('rms_volume', 0):.4f}")
                print(f"   📈 Speech Activity: {results.get('speech_activity_ratio', 0)*100:.1f}%")
                
                if results.get("recommendations"):
                    print("   💡 Recommendations:")
                    for i, rec in enumerate(results["recommendations"][:3], 1):
                        print(f"      {i}. {rec}")

if __name__ == "__main__":
    main()