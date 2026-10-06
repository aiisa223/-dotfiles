# Restrained Unix grey/gruvbox desktop

The selected desktop profile uses warm charcoal, grey text, and subdued gruvbox-inspired borders. Sway, Waybar, Rofi, Dunst, and Kitty share the palette. Normal interface labels have no accent hue. Terminal ANSI colors retain muted semantic differences for tools that emit colored output; even the bright slots are subdued rather than neon. Application themes outside these components remain application-controlled; no global GNOME/GTK/Qt settings are changed.

| Element | Value |
| --- | --- |
| Desktop/terminal background | `#282828` |
| Bar background | `#242424` |
| Raised surfaces | `#32302f` |
| Selected surface | `#504945` |
| Normal text | `#c8c3b7` |
| Secondary text | `#aaa69b` |
| Unfocused borders | `#3c3836` |
| Focus edge | `#928374` |

The installer includes Fedora's `dejavu-sans-mono-fonts`. Waybar uses DejaVu Sans Mono at 14 px with a 34-pixel bar. Sway and Dunst use that font at 11 pt, Rofi at 12 pt, and Kitty at its preserved 14 pt size with normal cell geometry. The previous 90% height/110% width overrides in Kitty are removed. The selected Rofi file is now `unix-grey.rasi`; the power helper follows that reference.

## Status metrics and cost

| Native Waybar module | Display | Update interval |
| --- | --- | --- |
| CPU | Overall `CPU 17%` | 3 seconds |
| Memory | Used `RAM 8.2 GiB`; used/total in tooltip | 5 seconds |
| Temperature | Intel package `CPU 122°F`; both °F/°C in tooltip | 5 seconds |

Memory is accurately labelled GiB: the module's default unit is binary gibibytes, not decimal GB. There are no external statistics scripts, `sensors` loops, animations, transitions, shadows, transparency effects, or decorative graphs. Hardware status still needs periodic reads; these modest intervals favor low overhead over instantaneous sampling. This configuration has not been benchmarked as a performance improvement.

Temperature uses the temperature module's stable `hwmon-path-abs` path `/sys/devices/platform/coretemp.0/hwmon` and `input-filename: temp1_input`, rather than a boot-dependent `hwmonN` number or an arbitrary ACPI thermal zone. This is the expected Intel coretemp package sensor on the Precision 5570; its existence and label have not been observed on this laptop yet. No unrelated temperature is used as a silent fallback. If this module is unavailable, send the Waybar error and this compact sensor inventory:

```sh
for dir in /sys/class/hwmon/hwmon*; do
    [ "$(cat "$dir/name" 2>/dev/null)" = coretemp ] || continue
    printf '%s\n' "$(readlink -f "$dir")"
    cat "$dir"/temp*_label
 done
```

The configured HOT indicator begins at 90°C / 194°F. It is a UI warning threshold, not a thermal-control policy or a claim about the CPU's maximum rating. Critical temperature/battery status uses bold text and a neutral background, without flashing. No NVIDIA temperature query is added.

## Apply to the existing linked profile

```sh
cd "$HOME/sway-dotfiles" &&
uv tool install --python /usr/bin/python3 autotiling==1.9.3 &&
git pull --ff-only &&
bash install-sway.sh --packages
```

Log out and select Sway again to apply all components together, then open a new Kitty window. The checkout remains the source for the existing symlinks. All layout bindings and bounded autotiling from `TILING.md` remain. Preserve local edits if Git rejects the fast-forward update; do not force a reset.

Sources: [Waybar CPU](https://github.com/Alexays/Waybar/blob/master/man/waybar-cpu.5.scd), [Waybar memory units](https://github.com/Alexays/Waybar/blob/master/man/waybar-memory.5.scd), [Waybar Fahrenheit/hwmon options](https://github.com/Alexays/Waybar/blob/master/man/waybar-temperature.5.scd), [Waybar GTK styling](https://github.com/Alexays/Waybar/blob/master/man/waybar-styles.5.scd), [Fedora font package](https://packages.fedoraproject.org/pkgs/dejavu-fonts/dejavu-sans-mono-fonts/), [Kitty configuration](https://sw.kovidgoyal.net/kitty/conf/), and [Linux coretemp driver](https://docs.kernel.org/hwmon/coretemp.html).

Validation: native Waybar JSON, GTK 3 stylesheet parsing, ShellCheck, Sway parse-only validation (same isolated harness and limits as the initial profile), five installer/rollback tests, and whitespace checks passed. The Fedora installer validates the real Sway config on the laptop. Font rendering, module fit, and the selected temperature sensor still require that runtime check.
