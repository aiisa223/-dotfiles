# Fedora Workstation Dotfiles

User configuration managed with Git + GNU Stow.

## Ownership

- User configuration: this repository + GNU Stow
- System packages: DNF/RPM
- Sandboxed applications: Flatpak
- Node runtimes: fnm
- Python runtimes: uv
- Containers: Podman
- Project dependencies: individual project repositories

Stow target: `$HOME`.

Do not commit credentials, authentication state, caches, databases, or generated runtime state.
