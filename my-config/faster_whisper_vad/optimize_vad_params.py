"""
Quick VAD Parameter Optimization

Based on the test results, this script helps you optimize your VAD parameters.
"""

import os
from pathlib import Path

def update_vad_parameters(aggressiveness=1, start_gate_ms=200, end_gate_ms=800, volume_threshold=0.008):
    """Update VAD parameters in the main script."""
    
    vad_script = Path("faster_whisper_vad.py")
    
    if not vad_script.exists():
        print("❌ faster_whisper_vad.py not found")
        return False
    
    # Read current script
    with open(vad_script, 'r') as f:
        content = f.read()
    
    # Update parameters
    replacements = {
        'START_GATE_MS = int(os.environ.get(\'START_GATE_MS\', 300))': 
            f'START_GATE_MS = int(os.environ.get(\'START_GATE_MS\', {start_gate_ms}))',
        'END_GATE_MS = int(os.environ.get(\'END_GATE_MS\', 1000))':
            f'END_GATE_MS = int(os.environ.get(\'END_GATE_MS\', {end_gate_ms}))',
        'VOLUME_THRESHOLD = 0.01':
            f'VOLUME_THRESHOLD = {volume_threshold}',
        'vad = webrtcvad.Vad(2)':
            f'vad = webrtcvad.Vad({aggressiveness})'
    }
    
    # Apply replacements
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print(f"✅ Updated: {old.split('=')[0].strip()} -> {new.split('=')[1].strip()}")
        else:
            print(f"⚠️  Could not find: {old.split('=')[0].strip()}")
    
    # Write updated script
    with open(vad_script, 'w') as f:
        f.write(content)
    
    print(f"✅ VAD parameters updated in {vad_script}")
    return True

def update_dockerfile():
    """Update Dockerfile to rebuild with new parameters."""
    
    dockerfile = Path("Dockerfile")
    
    if dockerfile.exists():
        print("📦 Dockerfile found - you'll need to rebuild the container:")
        print("   docker build -t realtime-transcription .")
        return True
    else:
        print("⚠️  No Dockerfile found - running directly with Python")
        return False

def main():
    """Main optimization function."""
    
    print("🎯 VAD Parameter Optimization")
    print("=" * 40)
    
    # Based on test results, these parameters performed best
    print("📊 Test results showed these optimal parameters:")
    print("   • Aggressiveness: 1 (less aggressive)")
    print("   • Start Gate: 200ms (more responsive)")  
    print("   • End Gate: 800ms (shorter segments)")
    print("   • Volume Threshold: 0.008 (more sensitive)")
    
    choice = input("\\nApply these optimized parameters? (y/N): ").strip().lower()
    
    if choice == 'y':
        print("\\n🔧 Applying optimized parameters...")
        
        success = update_vad_parameters(
            aggressiveness=1,
            start_gate_ms=200,
            end_gate_ms=800,
            volume_threshold=0.008
        )
        
        if success:
            has_dockerfile = update_dockerfile()
            
            print("\\n✅ Parameter optimization complete!")
            print("\\n🚀 Next steps:")
            if has_dockerfile:
                print("1. Rebuild Docker container:")
                print("   docker build -t realtime-transcription .")
                print("2. Test the updated system:")
                print("   ./run.sh")
            else:
                print("1. Test the updated system:")
                print("   python faster_whisper_vad.py")
            
            print("3. Say 'the quick brown fox jumps over the lazy dog' 5 times")
            print("4. Compare results with previous output")
            
        else:
            print("❌ Failed to update parameters")
    else:
        print("\\n⚠️  No changes made")
        print("\\n💡 Manual optimization options:")
        print("   • Set aggressiveness to 1 in your VAD configuration")
        print("   • Reduce START_GATE_MS to 200")
        print("   • Reduce END_GATE_MS to 800") 
        print("   • Lower VOLUME_THRESHOLD to 0.008")

if __name__ == "__main__":
    main()