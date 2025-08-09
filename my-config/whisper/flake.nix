{
  description = "Dictation via whisper.cpp with paste injection";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05"; # or unstable

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
          stream -m "$MODEL" -t "$(nproc)" \
          | stdbuf -oL sed -E 's/^\[[^]]+\]\s*//' \
          | while IFS= read -r line; do
              [ -z "''${line// }" ] && continue
              printf '%s ' "$line" | xclip -selection clipboard
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
          stream -m "$MODEL" -t "$(nproc)" \
          | stdbuf -oL sed -E 's/^\[[^]]+\]\s*//' \
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
          stream -m "$MODEL" -t "$(nproc)" \
          | stdbuf -oL sed -E 's/^\[[^]]+\]\s*//' \
          | awk 'NF' >> "$OUT"
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
    };
  };
}
