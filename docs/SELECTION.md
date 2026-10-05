# Automatic text copying

Selecting text in applications that publish a primary selection copies it to the normal clipboard. Paste with Ctrl+V, or Ctrl+Shift+V in Kitty. Middle-click primary-selection paste continues to work.

One service, `sway-selection-clipboard.service`, watches primary text selections. It starts with `sway-session.target` and stops when that target stops. It does not watch the normal clipboard, so its own writes cannot feed back into the watcher. There is no clipboard history or storage on disk.

Clearing a selection preserves the last clipboard item. Selecting new text replaces the clipboard, including an image copied earlier. Dragging a screenshot rectangle does not publish a text selection and does not replace the clipboard. Applications that do not publish a primary selection still need their own copy command.

Kitty's `copy_on_select` remains at its default: the session bridge owns automatic copying. Do not add another primary-to-clipboard synchronizer or an application-specific auto-copy setting for this same behavior.

After installing into an existing Sway session:

```sh
systemctl --user start sway-selection-clipboard.service
```

For later sessions, the installer creates the target dependency automatically.

References: [wl-clipboard manual](https://github.com/bugaevc/wl-clipboard/blob/master/data/wl-clipboard.1), [sway-systemd session ownership](https://github.com/alebastr/sway-systemd#session-targets), [Kitty copy_on_select](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.copy_on_select).
