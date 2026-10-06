# Sway input-method ownership

Sway uses IBus's native Wayland input-method v2 startup, `ibus start --type wayland`, through one Sway-only XDG autostart entry. Do not add another IBus `exec`, user service, or global input-module variable.

Fedora's `imsettings-start.desktop` otherwise launches `imsettings-boot.sh`, which started the legacy IBus panel on this machine. The installer derives a user override from the installed Fedora entry, preserving its keys and other desktop settings while excluding `sway`. It leaves `/etc/xdg/autostart` untouched and backs up any existing user override. Re-running the installer refreshes the derived entry when the packaged entry changes.

The generated entry lives under `~/.local/state/sway-dotfiles/generated/`; its content hash gives each packaged version a stable path. `~/.config/autostart/imsettings-start.desktop` links to it. Removing IBus or IMSettings, masking their services globally, or setting `DISABLE_IMSETTINGS` globally is unnecessary.

The existing Super+Space and Super+Shift+Space bindings remain owned by Sway. Use the IBus tray menu for input-method selection; IBus's default Super+Space switcher is not an available shortcut in this profile.

After installation, log out of Sway and log back in. A config reload does not replace already running input-method processes. Verify:

```sh
pgrep -a -u "$USER" -f '[i]bus|[i]msettings'
systemctl --user --failed --no-pager
```

Expect the IBus panel with `--enable-wayland-im --exec-daemon`, its daemon with `--panel disable`, and no `imsettings-daemon`. `--xim` may still appear in IBus's native startup for XWayland compatibility; it is not itself a failure.

References: [IBus Sway guidance](https://github.com/ibus/ibus/wiki/WaylandDesktop#sway), [IBus startup implementation](https://github.com/ibus/ibus/blob/main/tools/main.vala), [XDG autostart overrides and desktop exclusions](https://specifications.freedesktop.org/autostart/latest/), [Fedora IBus input-method v2 support](https://fedoraproject.org/wiki/Changes/IBus_1.5.32).
