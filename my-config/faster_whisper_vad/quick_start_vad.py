#!/usr/bin/env python3
"""
Quick Start VAD Testing Script

This script provides an easy way to get started with VAD testing.
"""

from vad_tester import AudioRecorder, VADTester, TranscriptionEvaluator
from vad_dashboard import VADDashboard
import sys

def main():
    print("🚀 Quick Start VAD Testing")
    print("=" * 30)
    
    print("\nWhat would you like to do?")
    print("1. Record test audio")
    print("2. Run quick parameter test") 
    print("3. Generate dashboard from existing results")
    print("4. Full testing workflow")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        recorder = AudioRecorder()
        filename = input("Audio filename (default: quick_test.wav): ").strip()
        if not filename:
            filename = "quick_test.wav"
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        recorder.record_test_audio(filename, duration=20)
        print(f"✅ Recording complete: {filename}")
        
    elif choice == "2":
        audio_file = input("Path to audio file: ").strip()
        if not audio_file:
            print("❌ Audio file required")
            return
        
        tester = VADTester()
        results = tester.parameter_sweep(audio_file, quick_test=True)
        best = tester.find_optimal_parameters(results)
        tester.save_results(results)
        
        print("✅ Quick test complete!")
        
    elif choice == "3":
        dashboard = VADDashboard()
        try:
            dashboard.create_full_dashboard()
            print("✅ Dashboard generated!")
        except Exception as e:
            print(f"❌ Dashboard generation failed: {e}")
            
    elif choice == "4":
        print("🔄 Running full workflow...")
        
        # Step 1: Record audio
        recorder = AudioRecorder()
        audio_file = recorder.record_test_audio("workflow_test.wav", duration=25)
        
        # Step 2: Run tests
        tester = VADTester()
        print("\n🧪 Running parameter tests...")
        results = tester.parameter_sweep(audio_file, quick_test=True)
        
        # Step 3: Find best parameters
        best = tester.find_optimal_parameters(results)
        results_file = tester.save_results(results)
        
        # Step 4: Generate dashboard
        dashboard = VADDashboard()
        try:
            outputs = dashboard.create_full_dashboard()
            print("\n🎉 Complete workflow finished!")
            print(f"Results: {results_file}")
            print("Dashboard files:")
            for name, path in outputs.items():
                print(f"  {name}: {path}")
        except Exception as e:
            print(f"⚠️  Dashboard generation failed: {e}")
            
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
