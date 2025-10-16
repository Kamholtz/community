# Optimising windows for audio

These notes highlight which Focusrite “Optimising Windows for Audio” style tweaks are most likely to improve Talon voice recognition (lower latency, fewer dropouts, more consistent CPU). The original Focusrite page could not be fetched automatically (403), so this is distilled from common Focusrite/DAW optimisation guidance.

## High impact for Talon

- Power plan: High/Ultimate Performance (CPU unthrottled)
  - Why: Prevents CPU frequency scaling and sleep states that add latency.
  - Steps: `Settings > System > Power & sleep > Additional power settings` → choose High performance/Ultimate; `Change plan settings > Change advanced power settings`:
    - `Processor power management`: Minimum/Maximum processor state = 100%
    - `USB settings`: USB selective suspend = Disabled
    - `PCI Express`: Link State Power Management = Off
    - `Power buttons and lid`: Hibernate/Sleep = Never while working

- Disable USB device power saving (interfaces/mics/webcams)
  - Why: Stops Windows from suspending USB audio devices, preventing input cutouts.
  - Steps: `Device Manager` → expand `Universal Serial Bus controllers` → for each `USB Root Hub (USB 3.0)` and relevant hubs: Properties → `Power Management` → uncheck “Allow the computer to turn off this device to save power”. Repeat for your USB audio device if the tab exists.

- Update chipset, USB, GPU, and audio drivers; update BIOS/UEFI
  - Why: Outdated drivers/firmware are common DPC latency sources affecting real‑time audio.
  - Steps: Install latest motherboard/chipset, USB controller, GPU drivers from vendor; update BIOS/UEFI; install your audio interface/mic drivers/firmware if applicable.

- Reduce background activity (startup apps, scheduled tasks)
  - Why: Background CPU/disk spikes disrupt real‑time audio capture/recognition.
  - Steps: `Settings > Apps > Startup` → disable non‑essentials. In Task Manager → Startup → disable unneeded. Pause heavy updaters/launchers while using Talon.

- Network-related DPC: disable Wi‑Fi/Bluetooth when not needed
  - Why: Network and BT drivers are frequent DPC offenders; disabling can smooth latency.
  - Steps: Toggle flight mode or disable specific adapters in `Device Manager` during Talon sessions if you observe issues in LatencyMon.

## Medium impact for Talon

- Disable Windows “audio enhancements” for the microphone device
  - Why: Avoids OS-level DSP that can add latency or alter mic signal.
  - Steps: `Sound settings` → `More sound settings` → `Recording` tab → select mic → `Properties` → `Advanced`/`Enhancements` → disable enhancements; set default format to a stable rate (e.g., 48000 Hz) and uncheck “Allow applications to take exclusive control” if other apps interfere.

- Disable Fast Startup
  - Why: Ensures drivers fully reinitialize on boot; can resolve odd audio/device states.
  - Steps: `Control Panel > Power Options > Choose what the power buttons do` → `Change settings that are currently unavailable` → uncheck “Turn on fast startup”.

- Turn off Windows Game Mode, Game Bar, and Xbox DVR
  - Why: Prevents capture/overlay services from adding overhead or seizing audio devices.
  - Steps: `Settings > Gaming` → disable Game Bar, Game DVR; `Settings > Gaming > Game Mode` → Off (or test which is better on your system).

- Disable system sounds and reduce visual effects
  - Why: Avoids sudden audio interruptions; frees a little CPU/GPU headroom.
  - Steps: `Sound` → Sound Scheme = “No Sounds”; `System > Advanced system settings > Performance` → “Adjust for best performance” or custom minimal.

- Pause OneDrive/Indexing/Cloud sync while dictating
  - Why: Disk/CPU spikes from sync and indexing can cause recognition hiccups.
  - Steps: Pause OneDrive/Dropbox; in `Indexing Options`, limit or pause indexing during sessions.

## Advanced/BIOS (only if needed, and with care)

- Disable deep CPU C‑states / EIST / Cool’n’Quiet; consider disabling Turbo Boost if unstable
  - Why: Stabilizes CPU latency at the cost of higher power/thermals.
  - Steps: BIOS/UEFI settings vary by vendor; only change if you are comfortable and revert if thermals/noise worsen.

## Likely low/neutral for Talon (DAW‑specific)

- Processor scheduling set to “Background services”
  - DAW guides recommend this for ASIO; for Talon (WASAPI/shared), “Programs” is usually fine. Only change if LatencyMon suggests scheduler contention.

## Verification tips

- Use LatencyMon to confirm improvements
  - Run LatencyMon during a typical Talon session; look for high DPC/ISR times and offending drivers (often network, storage, or GPU). Address those drivers first.

## Suggested Talon‑focused checklist

- High/Ultimate performance plan with processor 100%, USB suspend disabled.
- USB hubs/interfaces: power saving off; prefer direct motherboard ports.
- Up‑to‑date chipset/USB/GPU/audio drivers; BIOS current.
- Wi‑Fi/BT off (if problematic); Game Bar/Mode off; Fast Startup off.
- Mic device: enhancements off; stable sample rate (e.g., 48 kHz); exclusive mode off if contention.
- Minimal background apps; pause cloud sync/indexing during long dictation.
