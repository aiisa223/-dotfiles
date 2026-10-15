# Controls and learning reference

Press **Ctrl+Shift+/** (Ctrl+?) to open the existing controls helper. Choose all Sway bindings, resize mode, gaps mode, gestures, or the core Neovim reference. Search by keys or command names. Selecting a reference row never executes its command; Escape returns to the category list, then exits.

The Sway list reads the current user config and its file/glob includes, includes indented mode bindings, labels their modes, and expands the profile's variables. It follows the syntax used by this profile, rather than implementing every form of Sway configuration syntax. It runs only when opened, with no background process.

| Control | Behavior |
| --- | --- |
| Super+H/J/K/L | Focus left/down/up/right |
| Super+Shift+H/J/K/L | Move the container left/down/up/right |
| Super+Ctrl+H/J/K/L | Focus the output left/down/up/right |
| Super+Ctrl+Shift+H/J/K/L | Move the container to that output |
| Super+Alt+H / Super+V | Horizontal / vertical split |
| Super+R, then H/J/K/L | Shrink width / grow height / shrink height / grow width by 10 pixels |
| Resize mode: Shift+H/J/K/L | Same adjustments by 50 pixels |
| Super+G, then H/L | Decrease/increase inner gaps |
| Gaps mode: J/K | Decrease/increase outer gaps |

Arrow equivalents remain available. Hovering focuses a window, while keyboard navigation does not warp the pointer. Horizontal split moved from Super+H to Super+Alt+H to avoid conflicting with directional focus. The old semicolon directional bindings were removed.

Neovim's HJKL motions and Ctrl+W window commands are a core learning reference, not a replacement for its live mappings. Custom mappings may override them. The audited configuration already has terminal Ctrl+H/J/K/L pane mappings and delegates normal-mode navigation to vim-tmux-navigator; this profile does not replace those mappings. Its existing WhichKey configuration owns prefix/plugin help. Use `:verbose map {keys}` to identify a custom mapping's source.

Keyboard backlight persistence remains owned by Fedora's existing `systemd-backlight@leds:dell::kbd_backlight.service`: save at shutdown, restore at boot. No additional brightness startup command or service is installed. The physical backlight at 2/2 and successful boot service completion were observed; restoration of the new level still needs a reboot check. This preserves the last brightness, rather than forcing maximum brightness on every login or preventing firmware idle timeout.

Sources: [Sway commands](https://github.com/swaywm/sway/blob/master/sway/sway.5.scd), [Neovim motions](https://neovim.io/doc/user/motion/), [Neovim windows](https://neovim.io/doc/user/windows/), [WhichKey](https://github.com/folke/which-key.nvim), [systemd-backlight](https://github.com/systemd/systemd/blob/main/man/systemd-backlight%40.service.xml).

Validation: helper tests cover includes, modes, variable expansion, gestures, and duplicate shortcut detection for this profile. Installer/rollback, screenshot, and selection-copy tests also run. The installer validates the configuration with the laptop's installed Fedora Sway before changing links. Hover behavior and menu rendering require laptop acceptance checks.
