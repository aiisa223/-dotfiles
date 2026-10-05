
```sh
gh repo clone aiisa223/-dotfiles "$HOME/sway-dotfiles" -- --branch codex/sway-desktop
cd "$HOME/sway-dotfiles"
uv tool install --python /usr/bin/python3 autotiling==1.9.3
bash install-sway.sh --packages
```
