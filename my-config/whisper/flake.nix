{
  description = "Dictation via whisper.cpp with paste injection";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
  let
    forAll = f: nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" ] (system:
      let pkgs = import nixpkgs { inherit system; };
      in f pkgs);
  in
  {
    packages = forAll (pkgs: {
      dictate-x11-docker = pkgs.writeShellApplication {
        name = "dictate-x11-docker";
        runtimeInputs = [ pkgs.curl pkgs.jq pkgs.xdotool pkgs.xclip pkgs.pulseaudio pkgs.sox ];
        text = ''
          set -euo pipefail

          # Configuration - adjust these for your setup
          WHISPER_URL="http://localhost:8000"

          # Test if whisper service is available
          echo "Testing connection to faster-whisper service..." >&2
          if ! curl -s "$WHISPER_URL" > /dev/null 2>&1; then
            echo "Cannot connect to faster-whisper at $WHISPER_URL" >&2
            echo "Please ensure your faster-whisper container is running and accessible" >&2
            exit 1
          fi

          echo "Connected to faster-whisper service!" >&2
          echo "Dictation ready - speak now! (Ctrl+C to stop)" >&2

          while true; do
            # Record 15 seconds of audio (longer chunks for better accuracy and efficiency)
            TEMP_AUDIO=$(mktemp --suffix=.mp3)

            # Use parecord to capture audio, then compress with sox
            TEMP_WAV=$(mktemp --suffix=.mp3)
            timeout 15 parecord \
              --format=s16le \
              --rate=16000 \
              --channels=1 \
              "$TEMP_WAV" \
              2>/dev/null || true

            # Convert to FLAC for better compression
            if [ -f "$TEMP_WAV" ] && [ -s "$TEMP_WAV" ]; then
              sox "$TEMP_WAV" "$TEMP_AUDIO" 2>/dev/null || cp "$TEMP_WAV" "$TEMP_AUDIO"
              rm -f "$TEMP_WAV"
            fi

            # Process any audio we captured (removed minimum size check)
            if [ -f "$TEMP_AUDIO" ] && [ -s "$TEMP_AUDIO" ]; then
              echo "Processing audio..." >&2

              # Send to faster-whisper service with longer timeout
              RESPONSE=$(timeout 25 curl -s -X POST \
                --max-time 25 \
                -F "file=@$TEMP_AUDIO" \
                -F "model=Systran/faster-distil-whisper-small.en" \
                -F "response_format=json" \
                "$WHISPER_URL/v1/audio/transcriptions" 2>/dev/null || echo "")

                if [ -n "$RESPONSE" ]; then
                  # Extract text from response
                  TEXT=$(echo "$RESPONSE" | jq -r '.text // empty' 2>/dev/null || echo "")

                  if [ -n "$TEXT" ] && [ "$TEXT" != "null" ] && [ "$TEXT" != "" ]; then
                    # Clean the text
                    CLEAN_TEXT=$(echo "$TEXT" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

                    if [ -n "$CLEAN_TEXT" ] && [[ "$CLEAN_TEXT" =~ [[:alpha:]] ]]; then
                      echo "Pasting: '$CLEAN_TEXT'" >&2
                      printf '%s ' "$CLEAN_TEXT" | xclip -selection clipboard
                      sleep 0.1
                      xdotool key --clearmodifiers ctrl+v
                    fi
                  fi
                else
                  echo "No response from whisper service" >&2
                fi
            fi

            # Clean up temp audio file
            rm -f "$TEMP_AUDIO"

            # Short pause before next recording
            sleep 0.5
          done
        '';
      };

      dictate-x11 = pkgs.writeShellApplication {
        name = "dictate-x11";
        runtimeInputs = [ pkgs.whisper-cpp pkgs.xdotool pkgs.xclip pkgs.pulseaudio ];
        text = ''
          set -euo pipefail
          MODEL="$HOME/.local/share/whisper/models/ggml-small.en.bin"
          if [ ! -f "$MODEL" ]; then
            echo "Model not found: $MODEL" >&2; exit 1
          fi

          echo "Streaming dictation ready - speak now! (Ctrl+C to stop)" >&2

          while true; do
            # Record 3 seconds of audio
            TEMP_AUDIO=$(mktemp --suffix=.wav)

            # Use parecord to capture audio
            timeout 3 parecord --format=s16le --rate=16000 --channels=1 "$TEMP_AUDIO" 2>/dev/null || true

            if [ -f "$TEMP_AUDIO" ] && [ -s "$TEMP_AUDIO" ]; then
              # Process with whisper-cli
              RESULT=$(whisper-cli -m "$MODEL" -f "$TEMP_AUDIO" --no-timestamps 2>/dev/null | grep -v "^$" | head -1 || echo "")

              if [ -n "$RESULT" ]; then
                # Clean up the result and filter out whisper tokens
                CLEAN_RESULT=$(echo "$RESULT" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

                # Skip whisper special tokens and empty results
                if [ -n "$CLEAN_RESULT" ] && \
                   [[ "$CLEAN_RESULT" =~ [[:alpha:]] ]] && \
                   [[ ! "$CLEAN_RESULT" =~ ^\[.*\]$ ]] && \
                   [ "$CLEAN_RESULT" != "[BLANK_AUDIO]" ]; then
                  echo "Pasting: '$CLEAN_RESULT'" >&2
                  printf '%s ' "$CLEAN_RESULT" | xclip -selection clipboard
                  sleep 0.1
                  xdotool key --clearmodifiers ctrl+v
                fi
              fi
            fi

            # Clean up temp audio file
            rm -f "$TEMP_AUDIO"

            # Short pause before next recording
            sleep 0.5
          done
        '';
      };

      dictate-x11-simple = pkgs.writeShellApplication {
        name = "dictate-x11-simple";
        runtimeInputs = [ pkgs.whisper-cpp pkgs.xdotool pkgs.xclip pkgs.pulseaudio ];
        text = ''
          set -euo pipefail
          MODEL="$HOME/.local/share/whisper/models/ggml-small.en.bin"
          if [ ! -f "$MODEL" ]; then
            echo "Model not found: $MODEL" >&2; exit 1
          fi

          echo "Simple dictation test - speak for 5 seconds..." >&2

          # Record 5 seconds of audio directly
          TEMP_AUDIO=$(mktemp --suffix=.wav)
          trap 'rm -f "$TEMP_AUDIO"' EXIT

          # Use parecord to capture from default microphone
          timeout 5 parecord --format=s16le --rate=16000 --channels=1 "$TEMP_AUDIO" 2>/dev/null || true

          if [ -f "$TEMP_AUDIO" ] && [ -s "$TEMP_AUDIO" ]; then
            echo "Processing audio..." >&2

            # Use whisper-cli directly on the audio file
            RESULT=$(whisper-cli -m "$MODEL" -f "$TEMP_AUDIO" --no-timestamps --output-txt 2>/dev/null || echo "")

            if [ -n "$RESULT" ]; then
              # Clean up the result
              CLEAN_RESULT=$(echo "$RESULT" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

              if [ -n "$CLEAN_RESULT" ]; then
                echo "Transcription: '$CLEAN_RESULT'" >&2
                printf '%s' "$CLEAN_RESULT" | xclip -selection clipboard
                sleep 0.1
                xdotool key --clearmodifiers ctrl+v
                echo "Pasted!" >&2
              else
                echo "No transcription detected" >&2
              fi
            else
              echo "No audio processed" >&2
            fi
          else
            echo "No audio recorded" >&2
          fi
        '';
      };

      dictate-wayland = pkgs.writeShellApplication {
        name = "dictate-wayland";
        runtimeInputs = [ pkgs.whisper-cpp pkgs.wtype pkgs.wl-clipboard pkgs.curl pkgs.jq pkgs.sox ];
        text = ''
          set -euo pipefail
          MODEL="$HOME/.local/share/whisper/models/ggml-small.en.bin"
          if [ ! -f "$MODEL" ]; then
            echo "Model not found: $MODEL" >&2; exit 1
          fi

          # Start whisper server in background
          echo "Starting whisper server..." >&2
          whisper-server -m "$MODEL" -t "$(nproc)" --host 127.0.0.1 --port 8080 > /dev/null 2>&1 &
          SERVER_PID=$!

          # Wait for server to start
          echo "Waiting for server to initialize..." >&2
          sleep 8

          # Test if server is ready
          if ! curl -s http://127.0.0.1:8080 > /dev/null; then
            echo "Failed to start whisper server" >&2
            kill $SERVER_PID 2>/dev/null || true
            exit 1
          fi

          echo "Dictation ready - speak now! (Ctrl+C to stop)" >&2

          # Cleanup function
          cleanup() {
            echo "Stopping server..." >&2
            kill $SERVER_PID 2>/dev/null || true
            exit 0
          }
          trap cleanup EXIT INT TERM

          # Continuous audio capture and transcription loop
          while true; do
            # Record 3 seconds of audio
            TEMP_AUDIO=$(mktemp --suffix=.wav)

            # Use sox to record from the specified microphone
            timeout 3 sox -t alsa hw:1,0 -r 16000 -c 1 "$TEMP_AUDIO" silence 1 0.1 2% 1 0.5 2% 2>/dev/null || true

            # Check if we got any audio
            if [ -f "$TEMP_AUDIO" ] && [ -s "$TEMP_AUDIO" ]; then
              # Send to whisper server for transcription
              RESPONSE=$(curl -s -X POST http://127.0.0.1:8080/inference \
                -H "Content-Type: multipart/form-data" \
                -F "file=@$TEMP_AUDIO" \
                -F "response_format=json") || true

              # Extract transcription from JSON response
              if [ -n "$RESPONSE" ]; then
                TRANSCRIPTION=$(echo "$RESPONSE" | jq -r '.text // empty' 2>/dev/null | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

                if [ -n "$TRANSCRIPTION" ] && [ "$TRANSCRIPTION" != "null" ] && [ "$TRANSCRIPTION" != "" ]; then
                  printf '%s ' "$TRANSCRIPTION" | wl-copy
                  wtype --keys ctrl+v
                fi
              fi
            fi

            # Clean up temp audio file
            rm -f "$TEMP_AUDIO"

            # Short pause before next recording
            sleep 0.5
          done
        '';
      };

      dictate-wsl-out = pkgs.writeShellApplication {
        name = "dictate-wsl-out";
        runtimeInputs = [ pkgs.whisper-cpp pkgs.coreutils ];
        text = ''
          set -euo pipefail
          OUT="${OUT:-/mnt/c/Users/$USER/dictation.out}"
          : > "$OUT"
          MODEL="$HOME/.local/share/whisper/models/ggml-small.en.bin"
          if [ ! -f "$MODEL" ]; then
            echo "Model not found: $MODEL" >&2; exit 1
          fi
          whisper-stream -m "$MODEL" -t "$(nproc)" \
          | sed -E 's/^\[[^]]+\]\s*//' \
          | awk 'NF' >> "$OUT"
        '';
      };

      dictate-x11-realtime = pkgs.writeShellApplication {
        name = "dictate-x11-realtime";
        runtimeInputs = [ pkgs.curl pkgs.jq pkgs.xdotool pkgs.xclip pkgs.pulseaudio pkgs.coreutils pkgs.sox ];
        text = ''
          set -euo pipefail

          # Configuration - adjust these for your setup
          WHISPER_URL="http://localhost:8000"
          MODEL="Systran/faster-distil-whisper-small.en"

          # Test if we can reach the service
          echo "Testing connection to speaches service..." >&2
          if ! curl -s "$WHISPER_URL" > /dev/null 2>&1; then
            echo "Cannot connect to speaches at $WHISPER_URL" >&2
            echo "Please ensure your speaches container is running" >&2
            exit 1
          fi

          echo "Starting fast streaming dictation - speak now! (Ctrl+C to stop)" >&2
          echo "Using very short audio chunks for low latency" >&2

          # Cleanup function
          cleanup() {
            echo "Stopping streaming transcription..." >&2
            pkill -f "parecord" 2>/dev/null || true
          }
          trap cleanup EXIT INT TERM

          while true; do
            # Capture short chunks of audio (3 seconds) for meaningful content
            TEMP_AUDIO=$(mktemp --suffix=.wav)

            # Use parecord to capture short audio segments  
            timeout 3 parecord \
              --format=s16le \
              --rate=16000 \
              --channels=1 \
              "$TEMP_AUDIO" \
              2>/dev/null || true

            # Process any captured audio immediately (no minimum size check)
            if [ -f "$TEMP_AUDIO" ] && [ -s "$TEMP_AUDIO" ]; then
              # Convert to FLAC for better compression and speed
              TEMP_FLAC=$(mktemp --suffix=.flac)
              sox "$TEMP_AUDIO" "$TEMP_FLAC" 2>/dev/null || cp "$TEMP_AUDIO" "$TEMP_FLAC"

              # Send to speaches service with reasonable timeout
              RESPONSE=$(timeout 8 curl -s -X POST \
                --max-time 8 \
                -F "file=@$TEMP_FLAC" \
                -F "model=$MODEL" \
                -F "response_format=json" \
                "$WHISPER_URL/v1/audio/transcriptions" 2>/dev/null || echo "")

              if [ -n "$RESPONSE" ]; then
                # Extract text from response
                TEXT=$(echo "$RESPONSE" | jq -r '.text // empty' 2>/dev/null || echo "")

                if [ -n "$TEXT" ] && [ "$TEXT" != "null" ] && [ "$TEXT" != "" ]; then
                  # Clean the text
                  CLEAN_TEXT=$(echo "$TEXT" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

                  if [ -n "$CLEAN_TEXT" ] && [[ "$CLEAN_TEXT" =~ [[:alpha:]] ]]; then
                    echo "Fast: '$CLEAN_TEXT'" >&2
                    printf '%s ' "$CLEAN_TEXT" | xclip -selection clipboard
                    sleep 0.05
                    xdotool key --clearmodifiers ctrl+v
                  fi
                fi
              fi

              # Clean up temp files
              rm -f "$TEMP_AUDIO" "$TEMP_FLAC"
            else
              rm -f "$TEMP_AUDIO"
            fi

            # Very short pause for continuous streaming
            sleep 0.2
          done
        '';
      };

      dictate-x11-sliding = pkgs.writeShellApplication {
        name = "dictate-x11-sliding";
        runtimeInputs = [ pkgs.curl pkgs.jq pkgs.xdotool pkgs.xclip pkgs.pulseaudio pkgs.coreutils pkgs.sox ];
        text = ''
          set -euo pipefail

          # Configuration
          WHISPER_URL="http://localhost:8000"
          MODEL="Systran/faster-distil-whisper-small.en"
          WINDOW_SIZE=5    # seconds of audio per window
          OVERLAP_SIZE=1   # seconds of overlap between windows
          
          # Test connection
          if ! curl -s "$WHISPER_URL" > /dev/null 2>&1; then
            echo "Cannot connect to speaches at $WHISPER_URL" >&2
            exit 1
          fi

          echo "Starting sliding window dictation (prevents word splitting)" >&2
          echo "Window: ''${WINDOW_SIZE}s, Overlap: ''${OVERLAP_SIZE}s" >&2

          # Create audio buffer file
          AUDIO_BUFFER=$(mktemp --suffix=.wav)
          LAST_TRANSCRIPT=""
          
          cleanup() {
            echo "Stopping sliding window transcription..." >&2
            pkill -f "parecord" 2>/dev/null || true
            rm -f "$AUDIO_BUFFER" 2>/dev/null || true
          }
          trap cleanup EXIT INT TERM

          # Start continuous audio recording in background
          parecord --format=s16le --rate=16000 --channels=1 "$AUDIO_BUFFER" &
          
          echo "Audio recording started, processing in sliding windows..." >&2
          sleep 2  # Let some audio accumulate

          while true; do
            # Extract current window from the continuous recording
            CURRENT_WINDOW=$(mktemp --suffix=.wav)
            
            # Get the last WINDOW_SIZE seconds of audio
            sox "$AUDIO_BUFFER" "$CURRENT_WINDOW" trim -"''${WINDOW_SIZE}" 2>/dev/null || continue
            
            # Check if we have enough audio
            AUDIO_SIZE=$(wc -c < "$CURRENT_WINDOW" 2>/dev/null || echo 0)
            if [ "$AUDIO_SIZE" -lt 32000 ]; then
              rm -f "$CURRENT_WINDOW"
              sleep 0.5
              continue
            fi

            # Convert to FLAC for faster upload
            CURRENT_FLAC=$(mktemp --suffix=.flac)
            sox "$CURRENT_WINDOW" "$CURRENT_FLAC" 2>/dev/null || cp "$CURRENT_WINDOW" "$CURRENT_FLAC"

            # Transcribe the window
            RESPONSE=$(timeout 10 curl -s -X POST \
              --max-time 10 \
              -F "file=@$CURRENT_FLAC" \
              -F "model=$MODEL" \
              -F "response_format=json" \
              "$WHISPER_URL/v1/audio/transcriptions" 2>/dev/null || echo "")

            if [ -n "$RESPONSE" ]; then
              TRANSCRIPT=$(echo "$RESPONSE" | jq -r '.text // empty' 2>/dev/null || echo "")
              
              if [ -n "$TRANSCRIPT" ] && [ "$TRANSCRIPT" != "null" ] && [ "$TRANSCRIPT" != "" ]; then
                CLEAN_TRANSCRIPT=$(echo "$TRANSCRIPT" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
                
                if [ -n "$CLEAN_TRANSCRIPT" ] && [[ "$CLEAN_TRANSCRIPT" =~ [[:alpha:]] ]]; then
                  # Extract new words by comparing with last transcript
                  if [ -n "$LAST_TRANSCRIPT" ]; then
                    # Simple word diff - find new words at the end
                    NEW_WORDS=$(echo "$CLEAN_TRANSCRIPT" | sed "s/^$(echo "$LAST_TRANSCRIPT" | sed 's/[[\.*^$(){}?+|\\]]/\\&/g')//")
                    if [ -n "$NEW_WORDS" ] && [ "$NEW_WORDS" != "$CLEAN_TRANSCRIPT" ]; then
                      NEW_WORDS=$(echo "$NEW_WORDS" | sed 's/^[[:space:]]*//')
                      if [ -n "$NEW_WORDS" ]; then
                        echo "New: '$NEW_WORDS'" >&2
                        printf '%s ' "$NEW_WORDS" | xclip -selection clipboard
                        sleep 0.05
                        xdotool key --clearmodifiers ctrl+v
                      fi
                    fi
                  else
                    # First transcript - use it all
                    echo "First: '$CLEAN_TRANSCRIPT'" >&2
                    printf '%s ' "$CLEAN_TRANSCRIPT" | xclip -selection clipboard
                    sleep 0.05
                    xdotool key --clearmodifiers ctrl+v
                  fi
                  
                  LAST_TRANSCRIPT="$CLEAN_TRANSCRIPT"
                fi
              fi
            fi

            rm -f "$CURRENT_WINDOW" "$CURRENT_FLAC"
            
            # Sleep for (WINDOW_SIZE - OVERLAP_SIZE) to create overlap
            sleep $((WINDOW_SIZE - OVERLAP_SIZE))
          done
        '';
      };

      dictate-whisperx-setup = pkgs.writeShellApplication {
        name = "dictate-whisperx-setup";
        runtimeInputs = [
          pkgs.python3
          pkgs.python3Packages.pip
          pkgs.portaudio
          pkgs.python3Packages.pyaudio  # Pre-built to avoid compilation issues
        ];
        text = ''
          python3 setup_whisperx.py "$@"
        '';
      };
      
      dictate-whisperx-venv = pkgs.writeShellApplication {
        name = "dictate-whisperx-venv";
        runtimeInputs = [
          pkgs.python3
          pkgs.xdotool
          pkgs.xclip
          pkgs.portaudio
        ];
        text = ''
          # Check if venv exists
          if [ ! -d "venv_whisperx" ]; then
            echo "Virtual environment not found!" >&2
            echo "Run: nix run .#dictate-whisperx-setup" >&2
            echo "Or manually: python3 setup_whisperx.py" >&2
            exit 1
          fi
          
          # Check if run script exists
          if [ -f "run_whisperx.sh" ]; then
            exec ./run_whisperx.sh "$@"
          else
            # Fallback: use venv python directly
            exec venv_whisperx/bin/python dictate_whisperx.py "$@"
          fi
        '';
      };

      dictate-faster-whisper-setup = pkgs.writeShellApplication {
        name = "dictate-faster-whisper-setup";
        runtimeInputs = [
          pkgs.python3
          pkgs.python3Packages.pip
          pkgs.portaudio
          pkgs.python3Packages.pyaudio
        ];
        text = ''
          python3 setup_faster_whisper.py "$@"
        '';
      };
      
      dictate-faster-whisper-venv = pkgs.writeShellApplication {
        name = "dictate-faster-whisper-venv";
        runtimeInputs = [
          pkgs.python3
          pkgs.xdotool
          pkgs.xclip
          pkgs.portaudio
        ];
        text = ''
          # Check if venv exists
          if [ ! -d "venv_faster_whisper" ]; then
            echo "Virtual environment not found!" >&2
            echo "Run: nix run .#dictate-faster-whisper-setup" >&2
            echo "Or manually: python3 setup_faster_whisper.py" >&2
            exit 1
          fi
          
          # Check if run script exists
          if [ -f "run_faster_whisper.sh" ]; then
            exec ./run_faster_whisper.sh "$@"
          else
            # Fallback: use venv python directly
            exec venv_faster_whisper/bin/python dictate_faster_whisper.py "$@"
          fi
        '';
      };

      test-dictate = pkgs.writeShellApplication {
        name = "test-dictate";
        runtimeInputs = [ pkgs.whisper-cpp pkgs.xdotool pkgs.xclip pkgs.coreutils ];
        text = ''
          set -euo pipefail
          MODEL="$HOME/.local/share/whisper/models/ggml-small.en.bin"
          if [ ! -f "$MODEL" ]; then
            echo "Model not found: $MODEL" >&2; exit 1
          fi

          echo "Testing dictation pipeline..."
          echo "Model: $MODEL"
          echo "Starting whisper-stream..."

          # Add timeout and verbose output
          timeout 30 whisper-stream -m "$MODEL" -t "$(nproc)" -c 1 2>&1 | while IFS= read -r line; do
            echo "Raw output: '$line'"

            # Clean the line
            cleaned=$(echo "$line" | sed -E 's/^\[[^]]+\]\s*//')
            echo "Cleaned: '$cleaned'"

            # Skip empty lines
            if [ -z "''${cleaned// }" ]; then
              echo "Skipping empty line"
              continue
            fi

            echo "Processing: '$cleaned'"

            # Try clipboard
            printf '%s ' "$cleaned" | xclip -selection clipboard
            echo "Copied to clipboard"

            # Check clipboard
            clipcontent=$(xclip -selection clipboard -o)
            echo "Clipboard contains: '$clipcontent'"

            # Try paste
            echo "Attempting paste..."
            xdotool key --clearmodifiers ctrl+v

            sleep 0.5
          done
        '';
      };
    });

    apps = {
      x86_64-linux.dictate-x11 = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-x11}/bin/dictate-x11";
      };
      x86_64-linux.dictate-wayland = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-wayland}/bin/dictate-wayland";
      };
      x86_64-linux.dictate-wsl-out = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-wsl-out}/bin/dictate-wsl-out";
      };
      aarch64-linux.dictate-x11 = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-x11}/bin/dictate-x11";
      };
      aarch64-linux.dictate-wayland = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-wayland}/bin/dictate-wayland";
      };
      aarch64-linux.dictate-wsl-out = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-wsl-out}/bin/dictate-wsl-out";
      };
      x86_64-linux.test-dictate = {
        type = "app"; program = "${self.packages.x86_64-linux.test-dictate}/bin/test-dictate";
      };
      aarch64-linux.test-dictate = {
        type = "app"; program = "${self.packages.aarch64-linux.test-dictate}/bin/test-dictate";
      };
      x86_64-linux.dictate-x11-simple = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-x11-simple}/bin/dictate-x11-simple";
      };
      aarch64-linux.dictate-x11-simple = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-x11-simple}/bin/dictate-x11-simple";
      };
      x86_64-linux.dictate-x11-docker = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-x11-docker}/bin/dictate-x11-docker";
      };
      aarch64-linux.dictate-x11-docker = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-x11-docker}/bin/dictate-x11-docker";
      };
      x86_64-linux.dictate-x11-realtime = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-x11-realtime}/bin/dictate-x11-realtime";
      };
      aarch64-linux.dictate-x11-realtime = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-x11-realtime}/bin/dictate-x11-realtime";
      };
      x86_64-linux.dictate-x11-sliding = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-x11-sliding}/bin/dictate-x11-sliding";
      };
      aarch64-linux.dictate-x11-sliding = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-x11-sliding}/bin/dictate-x11-sliding";
      };
      x86_64-linux.dictate-whisperx-setup = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-whisperx-setup}/bin/dictate-whisperx-setup";
      };
      aarch64-linux.dictate-whisperx-setup = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-whisperx-setup}/bin/dictate-whisperx-setup";
      };
      x86_64-linux.dictate-whisperx-venv = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-whisperx-venv}/bin/dictate-whisperx-venv";
      };
      aarch64-linux.dictate-whisperx-venv = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-whisperx-venv}/bin/dictate-whisperx-venv";
      };
      x86_64-linux.dictate-faster-whisper-setup = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-faster-whisper-setup}/bin/dictate-faster-whisper-setup";
      };
      aarch64-linux.dictate-faster-whisper-setup = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-faster-whisper-setup}/bin/dictate-faster-whisper-setup";
      };
      x86_64-linux.dictate-faster-whisper-venv = {
        type = "app"; program = "${self.packages.x86_64-linux.dictate-faster-whisper-venv}/bin/dictate-faster-whisper-venv";
      };
      aarch64-linux.dictate-faster-whisper-venv = {
        type = "app"; program = "${self.packages.aarch64-linux.dictate-faster-whisper-venv}/bin/dictate-faster-whisper-venv";
      };
    };
  };
}
