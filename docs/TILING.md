# Tiling and movement refinement

Session reconciliation: the user's fresh-login results show `sway-session.target` and `waybar.service` active, one swayidle process, one LXQt PolicyKit agent, and zero failed user units. Lock/suspend, logout cleanup, and portal functional acceptance remain outstanding.

The layout model is still a container tree, much like i3. Sway does not document an animation setting in its 1.11 configuration manual. This refinement improves layout choices and access to controls; it does not claim to diagnose renderer stutter or enable animations. Rendering deadlines, tearing, and adaptive sync require separate measurements and hardware support; no speculative values are applied to the 59.95 Hz laptop display.

Autotiling is the upstream `nwg-piotr/autotiling` tool, pinned to its published 1.9.3 release. It reacts to IPC events, rather than polling or animating windows, and chooses split orientation from the focused window's aspect ratio. Its README recommends `--limit 2` as a starting point and warns about tabbed/stacked interactions. It is enabled on numeric workspaces 1–8 (including the existing named workspaces). Workspaces 9 and 10 retain full manual layout control. Manual Super+Alt+H / Super+V split choices on automatic workspaces can be overwritten by later helper events; use a manual workspace when exact tree construction matters. Existing deep trees are not automatically flattened or rebuilt.

| Control | Behavior |
| --- | --- |
| Super + left drag | Move floating windows or drag/drop tiled containers into a new place |
| Super + right drag | Resize with the existing modifier behavior |
| Super + R, then H/J/K/L or arrows | Fine resize in 10-pixel steps; Shift+arrows uses 50-pixel steps; Escape exits |
| Super + A / Shift+A | Select parent group / return to its focused child; subsequent move/layout commands act on the selected group |
| Super + Ctrl+Space | Cycle horizontal split, vertical split, tabs, and stacking for the selected container |
| Super + Ctrl+M, then focus another window, Super + Ctrl+S | Mark the first container and swap it with the second; Ctrl+Shift+M clears the swap mark |
| Super + Ctrl+arrows | Focus the output in that direction |
| Super + Ctrl+Shift+arrows | Move the selected container to that output |
| Super + Shift+F | Toggle fullscreen across all outputs; Super+F retains ordinary fullscreen |
| Three-finger swipe left/right | Next/previous existing workspace on the current output, if the input device supports swipe gestures |
| Super + G, then Right / Left | Increase/decrease inner gaps for this workspace by 2 pixels |
| In gaps mode: Up / Down | Increase/decrease outer gaps by 2 pixels |
| In gaps mode: 0 / D / Escape | Zero gaps / restore 6-inner and 0-outer defaults / exit mode |

Two-pixel warm-grey focus borders distinguish adjacent windows. Smart gaps remove gaps on single-child workspaces; smart borders hide borders with only one visible child. Split layouts omit titlebars while tabbed/stacked containers retain their tab/title controls. Directional focus no longer wraps at a container edge. These dimensions and focus behavior are chosen preferences, not Fedora-mandated values. The native tiled-drag feature is made explicit but was already enabled by Sway's default; its titlebar threshold is retained at the documented default 9, and does not affect modifier dragging.

Update an existing linked installation:

```sh
cd "$HOME/sway-dotfiles" &&
uv tool install --python /usr/bin/python3 autotiling==1.9.3 &&
git pull --ff-only &&
bash install-sway.sh
```

Then log out and select Sway again. A fresh session starts the helper once and creates workspaces with the new default gaps/borders. Keep local dotfile edits committed before pulling; if Git refuses the update, preserve and reconcile those edits instead of forcing a reset. Check `pgrep -a -u "$USER" -f '(^|/)autotiling([[:space:]]|$)'` afterward: expect one process. On workspace 1, open four ordinary windows to assess the shallow automatic split behavior; use workspace 9 to compare manual layout. Test Super-drag separately from text-selection dragging. Neither the listener's runtime behavior nor pointer fluidity has been tested on the laptop yet.

Sources: [Sway 1.11 commands](https://github.com/swaywm/sway/blob/1.11/sway/sway.5.scd) (dragging, gestures, focus, resize, marks/swaps, borders/gaps, output movement), [autotiling README](https://github.com/nwg-piotr/autotiling), [published release](https://pypi.org/project/autotiling/1.9.3/), [uv isolated tools](https://docs.astral.sh/uv/guides/tools/), and [Sway output timing](https://github.com/swaywm/sway/blob/1.11/sway/sway-output.5.scd).

Validation: the updated configuration passed the same Sway 1.9 parse-only harness used for the initial profile (socket registration stubbed; Fedora snippets absent), ShellCheck, and whitespace checks. The five installer/rollback tests remain green. The pinned autotiling tool installed with system Python in a temporary isolated uv environment and its CLI options were verified. Fedora's actual Sway validation runs before installation; live IPC layout behavior remains a laptop acceptance check.
