#!/usr/bin/env bash
# Install only the selected desktop profile. See docs/SWAY.md.
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
if [[ ${1:-} == --restore ]]; then
    [[ $# == 2 ]] || { echo 'Usage: install-sway.sh --restore BACKUP'; exit 2; }
    exec python3 "$repo/tools/install_sway.py" --restore "$2"
fi
if [[ $# -gt 1 || ( $# == 1 && ${1:-} != --packages ) ]]; then
    echo 'Usage: install-sway.sh [--packages] | --restore BACKUP'; exit 2
fi
[[ $EUID != 0 ]] || { echo 'Run as your normal user, not root.'; exit 1; }
# This profile depends on Fedora paths and the selected upstream config package.
# shellcheck source=/dev/null
source /etc/os-release
[[ $ID == fedora ]] || { echo 'This installer targets Fedora; no files changed.'; exit 1; }
packages=(sway sway-config-upstream sway-systemd kitty waybar rofi dunst
    lxqt-policykit swayidle swaylock brightnessctl grim slurp util-linux wl-clipboard
    xdg-desktop-portal xdg-desktop-portal-gtk xdg-desktop-portal-wlr
    gnome-keyring ibus wireplumber python3 jq libnotify xdg-user-dirs playerctl
    dolphin btop NetworkManager-tui dejavu-sans-mono-fonts)
if [[ ${1:-} == --packages ]]; then
    sudo dnf install "${packages[@]}"
fi
missing=()
for package in "${packages[@]}"; do
    rpm -q "$package" >/dev/null 2>&1 || missing+=("$package")
done
if (( ${#missing[@]} )); then
    printf 'Missing packages. Run: sudo dnf install'; printf ' %q' "${missing[@]}"; printf '\n'
    exit 1
fi
[[ -x /usr/libexec/lxqt-policykit-agent && -f /etc/sway/config.d/10-systemd-session.conf && -f /usr/share/sway-systemd/95-xdg-desktop-autostart.conf ]] || {
    echo 'Expected Fedora session integration is missing; no files changed.'; exit 1;
}
[[ -x "$HOME/.local/bin/autotiling" ]] || {
    echo 'Install the isolated Python tool first: uv tool install --python /usr/bin/python3 autotiling==1.9.3'
    exit 1
}
systemctl --user cat sway-session.target waybar.service >/dev/null
WLR_BACKENDS=headless WLR_RENDERER=pixman sway --validate --config "$repo/sway-desktop/.config/sway/config"
python3 "$repo/tools/install_sway.py"
echo 'Log out, then select Sway in GDM. Do not reload into this profile halfway through a session.'
