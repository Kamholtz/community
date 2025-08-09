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
      dictate-x11 = pkgs.writeShellApplication {
        name = "dictate-x11";
        runtimeInputs = [ pkgs.whisper-cpp pkgs.xdotool pkgs.xclip pkgs.coreutils ];
        text = ''
          set -euo pipefail
          MODEL="$HOME/.local/share/whisper/models/ggml-small.en.bin"
          if [ ! -f "$MODEL" ]; then
            echo "Model not found: $MODEL" >&2; exit 1
          fi
          whisper-stream -m "$MODEL" -t "$(nproc)" -c 1 \
          | sed -E 's/^\[[^]]+\]\s*//' \
          | while IFS= read -r line; do
              [ -z "''${line// }" ] && continue
              echo "Pasting: $line" >&2
              printf '%s ' "$line" | xclip -selection clipboard
              sleep 0.1
              xdotool key --clearmodifiers ctrl+v
            done
        '';
      };

      dictate-wayland = pkgs.writeShellApplication {
        name = "dictate-wayland";
        runtimeInputs = [ pkgs.whisper-cpp pkgs.wtype pkgs.wl-clipboard pkgs.coreutils ];
        text = ''
          set -euo pipefail
          MODEL="$HOME/.local/share/whisper/models/ggml-small.en.bin"
          if [ ! -f "$MODEL" ]; then
            echo "Model not found: $MODEL" >&2; exit 1
          fi
          whisper-stream -m "$MODEL" -t "$(nproc)" \
          | sed -E 's/^\[[^]]+\]\s*//' \
          | while IFS= read -r line; do
              [ -z "''${line// }" ] && continue
              printf '%s ' "$line" | wl-copy
              wtype --keys ctrl+v
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
          echo "Speak into your microphone now:"
          
          whisper-stream -m "$MODEL" -t "$(nproc)" -c 1 | while IFS= read -r line; do
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
    };
  };
}
