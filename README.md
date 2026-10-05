# Ali's workstation dotfiles

The Fedora Sway desktop is a complete, independently installable profile in `sway-desktop/`, adapted from this repository's existing i3 workflow and the selected Kitty/Rofi/Waybar/Dunst/LXQt PolicyKit/swayidle/swaylock stack. The desktop uses a restrained warm-grey/gruvbox palette with readable DejaVu Sans Mono text and native CPU/RAM/temperature indicators.

See **[installation](docs/SWAY.md)** and **[tiling controls](docs/TILING.md)**, and **[theme and status metrics](docs/THEME.md)**. Install the documented isolated autotiling tool with uv, then run `bash install-sway.sh --packages` as your normal user on Fedora. The installer backs up existing desktop files and links this checkout; log out and select Sway in GDM afterward.

The original Stow packages and developer configuration remain available. Do not Stow legacy desktop packages over the new profile. Shell, Git, development tools, and services are not installed or changed by the Sway installer.

Ownership: dotfiles in Git, distro software through DNF, applications through Flatpak where appropriate, JavaScript through fnm, Python tools through uv, and containers through Podman. Never commit secrets, caches, or downloaded tool binaries.
