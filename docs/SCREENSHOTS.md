# Screenshots

Press **Print Screen** (or **Super+Shift+S**), drag a rectangle, then release the mouse to save it. **Escape** cancels without taking a screenshot. **Shift+Print Screen** captures the focused display.

Images are saved in `Screenshots/` under your XDG Pictures directory, with a notification showing the path. Repeated shortcuts while selecting do not open another selector.

The installer supplies `slurp` for region selection, `grim` for capture, and `flock` from `util-linux` for the single-selector guard. No background screenshot service is needed.

References: [slurp manual](https://github.com/emersion/slurp/blob/master/slurp.1.scd), [grim manual](https://github.com/emersion/grim/blob/master/grim.1.scd), [Sway bindings and reload](https://github.com/swaywm/sway/blob/master/sway/sway.5.scd), [Fedora slurp package](https://packages.fedoraproject.org/pkgs/slurp/slurp/).
