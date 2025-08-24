# --- System / OS info ---
cat /etc/os-release                      # Distro and version
uname -a                                 # Kernel and architecture
lsb_release -a                           # Distribution release info (if available)

# --- Hardware info ---
lscpu                                    # CPU details
nvidia-smi || glxinfo -B                 # GPU details (if NVIDIA/Intel GPU)
free -h                                  # Memory usage / total RAM
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT       # Disk layout

# --- Package managers ---
dpkg -l | grep pop-os                    # Core Pop!_OS packages
apt list --installed 2>/dev/null | head -50   # First 50 APT packages (for context)
nix --version                            # Nix version
home-manager --version                   # Home Manager version
nix-channel --list                       # Configured Nix channels
nix-env -q                               # Installed Nix packages in user profile
nix profile list                         # Installed packages in new-style Nix profiles
nix-store --gc --print-roots             # What is actively being used in the Nix store

# --- NixOS/Home Manager configs ---
find ~/.config/nixpkgs -type f           # Location of Home Manager configs
find ~/.config/home-manager -type f      # Alternate config path (if used)

# --- Services / Drivers ---
systemctl list-unit-files --type=service --state=enabled   # Enabled services
systemctl status nvidia-driver.service 2>/dev/null || true # NVIDIA driver service (if exists)

# --- Networking ---
nmcli device status                      # Network interfaces status
ip a                                     # IP + interfaces
