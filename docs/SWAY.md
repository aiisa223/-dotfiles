# Fedora Sway desktop

This is Ali's existing workstation configuration adapted to the chosen Sway stack. The complete desktop profile lives in `sway-desktop/`. Its files become symlinks in your home directory, so edits to this checkout immediately become your dotfiles. Keep the checkout at its installation path.

## Install

Run as your normal user from GNOME or a terminal. The installer validates the Sway configuration before changing desktop files. `--packages` installs missing RPMs through DNF; omit it if all dependencies are installed.

```sh
gh repo clone aiisa223/-dotfiles "$HOME/sway-dotfiles" -- --branch codex/sway-desktop
cd "$HOME/sway-dotfiles"
bash install-sway.sh --packages
```

Log out, then choose Sway in GDM. A fresh login starts the selected agent and idle daemon exactly once. Do not start an additional session for the same user concurrently with GNOME: the user service manager and D-Bus activation environment are shared. Shell, Git, development services, NVIDIA drivers, PAM, GDM, and old i3 files are outside the installer's managed paths.

The installer backs up the existing Sway, swayidle, swaylock, Waybar, Rofi, Kitty, and Dunst directories, including symlinks, before linking the complete replacement directories. It also backs up the Sway portal preference, NVIDIA-settings autostart override, eight `sway-*` desktop helpers, and Waybar target dependency if those paths change. Existing extra files inside the replaced directories stay in the backup. Installation refuses parent directory symlinks that would redirect writes into another Stow checkout. Do not also Stow the old Kitty/Rofi/Dunst packages over this profile.

The installer prints the exact rollback command and backup path. Rollback restores prior files and links and removes newly installed links; it refuses to overwrite a destination you replaced after installation. It does not uninstall RPMs. It does not revert edits you made to the checkout itself. Log out and back in after restoring. A repeated install from the same checkout does nothing when all links already match.

## Component ownership

| Component | Owner and configuration |
| --- | --- |
| Sway | GDM session; one `~/.config/sway/config`, upstream-style commands and Fedora includes |
| Session environment and cgroups | Packaged `sway-systemd` config under `/etc/sway/config.d/` |
| XDG autostart | Packaged `/usr/share/sway-systemd/95-xdg-desktop-autostart.conf`, included once |
| Waybar | Packaged `waybar.service`; symlink in `sway-session.target.wants`, equivalent to `systemctl --user add-wants sway-session.target waybar.service`; no `exec waybar` |
| Notifications | Dunst's packaged D-Bus activation; no second startup command |
| PolicyKit agent | One initial Sway `exec /usr/libexec/lxqt-policykit-agent`; the packaged desktop entry only admits LXQt |
| Idle/lock | One initial `exec swayidle -w`; password authentication through existing swaylock PAM |
| Portals | GTK default, wlr ScreenCast/Screenshot, gnome-keyring Secret, matching the accepted preference |
| Secret Service | Existing GNOME Keyring; Bitwarden remains independent |

The NVIDIA-settings desktop override preserves the previously accepted `Hidden=true` change. It suppresses that user's saved-setting autostart in **all** desktops, including GNOME; it does not disable NVIDIA drivers or offload. Fedora's installed default snippets remain authoritative: the installer checks the expected integration paths and validates against the actual installed snippets rather than inventing services.

## What carries over and improves

- Super is the modifier. J/K/L/semicolon and arrows retain your left/down/up/right navigation. Super+H/V split, Super+F fullscreen, Super+R resize, Super+W tabs, Super+S stacking. Both old reload/restart bindings now reload Sway.
- Workspace names remain `1:code`, `2:agent`, `3:term`, `4:web`, `5:ops`, then 6–10. Existing unambiguous XWayland PyCharm/Codex routing remains; native PyCharm also has an app_id rule. Native Codex routing is deliberately left for its actual app_id to be observed.
- Super+D opens Rofi applications. Alt+Tab lists actual Sway windows by container ID, including native Wayland and XWayland clients. Super+Shift+D preserves the Indicant palette. Super+grave opens/toggles the dedicated Kitty scratchpad on demand, with your project directory when it exists.
- Super+Shift+P and Waybar's Session button open the power/session menu; logout, reboot, and shutdown ask for confirmation. Ctrl+Alt+L locks with swaylock. Five idle minutes and logind lock/before-sleep events lock through the accepted swayidle policy. There is **no automatic suspend or screen-power-off timer**. Existing PAM is untouched.
- Print and Super+Shift+S save the **focused output** to `Pictures/Screenshots` (using the XDG Pictures location). Region selection from the old Flameshot binding is not preserved: the selected stack includes grim, but no region selector. No additional screenshot daemon is installed.
- Audio keys and Waybar scrolling use `wpctl` and cap raising volume at 100%. Brightness chooses a backlight device rather than a keyboard LED and avoids setting its raw brightness to zero. Both have replacing Dunst OSD notifications.
- Touchpad tap and clickfinger are retained. Drag lock is explicitly disabled, disable-while-typing is enabled, and two-finger scrolling is selected. Clicking changes window focus; workspace navigation no longer warps the pointer. Mouse acceleration and speed remain device defaults.
- The existing Kitty/Rofi purple palette now also supplies Sway, Waybar, and Dunst accents. The original font preference is retained; install your existing Terminus TTF separately if needed, or replace the font with `monospace` in those configurations. No bundled binaries, global toolkit backend variables, or GPU tuning are added.

**Selection sticking is not diagnosed yet.** Drag lock is already disabled by default in Sway, so spelling it out may make no difference on your machine. The focus/warping changes remove two potential interruptions. If sticking persists, distinguish external mouse vs touchpad, physical drag vs tap-and-drag, and Kitty vs another application before changing further libinput settings. At the edge of a touchpad, libinput can briefly auto-lock a drag even with drag lock disabled; disabling `drag` would change that gesture, so this profile keeps it enabled.

## Reconciled state and remaining work

The submitted machine evidence establishes a running Sway environment, imported session variables, live GTK/wlr portals, an unlocked Login keyring collection, notifications, and a single swayidle process. It does **not** establish a complete lock/suspend/logout acceptance test or successful portal screen sharing. The repo was an i3/X11 snapshot, so the new profile supplies the missing desktop conversion while preserving those machine decisions.

After your fresh login, one compact status batch is sufficient:

```sh
systemctl --user is-active sway-session.target waybar.service
pgrep -a -u "$USER" -x swayidle
pgrep -a -u "$USER" -f '^/usr/libexec/lxqt-policykit-agent'
systemctl --user --failed --no-pager
```

Then use Ctrl+Alt+L and unlock with your password. Suspend from the Session menu only after that succeeds; verify the screen remains locked on resume. Portal screen-sharing and logout lifecycle still need their runtime acceptance checks. The earlier imsettings/IBus GLib crash remains unresolved; this configuration does not claim to repair it or globally disable input methods. Scaling/output tuning, legacy package cleanup, and performance changes remain later stages. Do not mass-remove GNOME or NVIDIA packages as part of this installation.

## Documentation behind the configuration

The Sway wiki was reviewed as migration guidance, including its i3 migration, systemd, native Wayland, add-ons, environment, GTK, and portal pages. Distribution-specific and obsolete workarounds are not copied into this Fedora setup. Component manuals are authoritative for command syntax.

| Area | Official/component-upstream reference |
| --- | --- |
| Sway wiki and migration | [Wiki](https://github.com/swaywm/sway/wiki), [i3 migration](https://github.com/swaywm/sway/wiki/i3-Migration-Guide), [add-ons](https://github.com/swaywm/sway/wiki/Useful-add-ons-for-sway) |
| Sway commands, bindings, focus, includes | [sway(5)](https://github.com/swaywm/sway/blob/master/sway/sway.5.scd) |
| Touchpad configuration | [sway-input(5)](https://github.com/swaywm/sway/blob/master/sway/sway-input.5.scd), [libinput tapping/drag lock](https://wayland.freedesktop.org/libinput/doc/latest/tapping.html) |
| Window IDs, tree, outputs | [sway-ipc(7)](https://github.com/swaywm/sway/blob/master/sway/sway-ipc.7.scd) |
| Fedora upstream baseline | [Fedora sway-config-upstream package](https://packages.fedoraproject.org/pkgs/sway/sway-config-upstream/) |
| Session and autostart | [sway-systemd](https://github.com/alebastr/sway-systemd), [systemd XDG autostart generator](https://www.freedesktop.org/software/systemd/man/latest/systemd-xdg-autostart-generator.html), [systemctl add-wants](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) |
| PolicyKit binary/desktop entry | [Fedora LXQt PolicyKit](https://packages.fedoraproject.org/pkgs/lxqt-policykit/lxqt-policykit/fedora-44.html), [LXQt upstream](https://github.com/lxqt/lxqt-policykit) |
| Idle and locker | [swayidle(1)](https://github.com/swaywm/swayidle/blob/master/swayidle.1.scd), [swaylock(1)](https://github.com/swaywm/swaylock/blob/master/swaylock.1.scd) |
| Waybar and modules | [waybar(5)](https://github.com/Alexays/Waybar/blob/master/man/waybar.5.scd), [module manuals](https://github.com/Alexays/Waybar/tree/master/man) |
| Rofi configuration and dmenu index | [rofi(1)](https://github.com/davatorium/rofi/blob/next/doc/rofi.1.markdown), [rofi-dmenu(5)](https://github.com/davatorium/rofi/blob/next/doc/rofi-dmenu.5.markdown) |
| Portal preferences | [portals.conf(5)](https://flatpak.github.io/xdg-desktop-portal/docs/portals.conf.html), [Sway portal guidance](https://github.com/swaywm/sway/wiki/XDG-Desktop-Portal-configuration) |
| Audio/brightness | [wpctl](https://pipewire.pages.freedesktop.org/wireplumber/man/wpctl.html), [brightnessctl](https://github.com/Hummer12007/brightnessctl) |
| Notifications | [Dunst documentation](https://dunst-project.org/documentation/), [dunstify](https://dunst-project.org/documentation/dunstify/) |
| Screenshots | [grim manual](https://gitlab.freedesktop.org/emersion/grim/-/blob/master/grim.1.scd) |
| Hidden autostart override | [freedesktop autostart specification](https://specifications.freedesktop.org/autostart-spec/latest/) |
| Kitty class and configuration | [Kitty invocation](https://sw.kovidgoyal.net/kitty/invocation/), [Kitty configuration](https://sw.kovidgoyal.net/kitty/conf/) |

## Validation

The repository checks are `python3 -m unittest discover -s tools -p 'test_*.py' -v`, `bash -n install-sway.sh`, Bash syntax checks on each profile helper, `jq empty sway-desktop/.config/waybar/config.jsonc`, and `git diff --check`. The installer performs Fedora's installed `sway --validate` before applying changes. Runtime hardware/session behavior requires the laptop acceptance steps above.

Local checks passed: five installer/rollback tests, ShellCheck, embedded jq programs, JSON, GTK 3 stylesheet parsing, and whitespace checks. Sway 1.9 accepted the configuration in a parse-only headless harness (the scratch environment blocks listening sockets, so its socket-registration call was stubbed). This did not test Fedora 1.11 integration snippets, which are absent here, or a real session; the installer validates against those on your laptop.
