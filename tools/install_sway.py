#!/usr/bin/env python3
"""Link the desktop profile; retain exact old files/symlinks for restoration."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parents[1]
HOME = Path.home()
PROFILE = REPO / 'sway-desktop'
TARGETS = [f'.config/{name}' for name in
           ('sway', 'swayidle', 'swaylock', 'waybar', 'rofi', 'kitty', 'dunst')]
TARGETS += ['.config/xdg-desktop-portal/sway-portals.conf',
            '.config/autostart/nvidia-settings-user.desktop',
            '.config/autostart/org.freedesktop.IBus.Panel.Wayland.Gtk3.desktop',
            '.config/systemd/user/sway-selection-clipboard.service',
            '.config/systemd/user/sway-session.target.wants/sway-selection-clipboard.service']
TARGETS += [str(p.relative_to(PROFILE)) for p in sorted((PROFILE / '.local/bin').iterdir())]
WAYBAR = '.config/systemd/user/sway-session.target.wants/waybar.service'
IMSETTINGS = Path('/etc/xdg/autostart/imsettings-start.desktop')
IMSETTINGS_TARGET = '.config/autostart/imsettings-start.desktop'


def exclude_sway(text):
    """Preserve the packaged desktop entry, excluding only Sway."""
    lines = text.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.strip() == '[Desktop Entry]')
    end = next((i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith('[')), len(lines))
    for key in ('OnlyShowIn', 'NotShowIn'):
        for i in range(start + 1, end):
            if lines[i].startswith(key + '='):
                desktops = [name for name in lines[i].split('=', 1)[1].strip().split(';') if name]
                if key == 'OnlyShowIn':
                    desktops = [name for name in desktops if name != 'sway']
                elif 'sway' not in desktops:
                    desktops.append('sway')
                lines[i] = key + '=' + ';'.join(desktops) + ';\n'
                return ''.join(lines)
    if end and not lines[end - 1].endswith('\n'):
        lines[end - 1] += '\n'
    lines.insert(end, 'NotShowIn=sway;\n')
    return ''.join(lines)


def exists(path):
    return os.path.lexists(path)


def check_parents(target):
    # Never follow a parent Stow link and write into another checkout.
    for parent in target.parents:
        if parent == HOME:
            break
        if parent.is_symlink():
            raise RuntimeError(f'Parent is a symlink: {parent}. Resolve its ownership first.')
        if exists(parent) and not parent.is_dir():
            raise RuntimeError(f'Parent is not a directory: {parent}')


def restore(backup):
    manifest = json.loads((backup / 'manifest.json').read_text())
    if manifest['home'] != str(HOME):
        raise RuntimeError('Backup belongs to a different home directory.')
    # Check every destination before changing anything; preserve subsequent edits.
    for entry in manifest['entries']:
        target = HOME / entry['path']
        check_parents(target)
        if exists(target) and (not target.is_symlink() or os.readlink(target) != entry['link']):
            raise RuntimeError(f'{target} changed after installation; move it aside before restoring.')
        saved = backup / 'previous' / entry['path']
        if entry['previous'] and not exists(saved):
            raise RuntimeError(f'Backup file missing: {saved}')
    for entry in reversed(manifest['entries']):
        target = HOME / entry['path']
        if exists(target):
            target.unlink()
        if entry['previous']:
            os.replace(backup / 'previous' / entry['path'], target)
    (backup / 'manifest.json').rename(backup / 'restored-manifest.json')
    print('Previous desktop files restored. Log out and back in.')


def install():
    generated = None
    if IMSETTINGS.is_file():
        text = exclude_sway(IMSETTINGS.read_text())
        digest = hashlib.sha256(text.encode()).hexdigest()
        generated = HOME / '.local/state/sway-dotfiles/generated' / f'imsettings-{digest}.desktop'
    # Preflight all ancestors before making backups or links.
    for relative in TARGETS + [WAYBAR] + ([IMSETTINGS_TARGET] if generated else []):
        check_parents(HOME / relative)
    if generated:
        check_parents(generated)
        if exists(generated) and (generated.is_symlink() or generated.read_text() != text):
            raise RuntimeError(f'Generated desktop entry was modified: {generated}')
    # Ask systemd which packaged unit it will actually use.
    unit = subprocess.check_output(
        ['systemctl', '--user', 'show', '-p', 'FragmentPath', '--value', 'waybar.service'],
        text=True).strip()
    if not unit or not Path(unit).is_file():
        raise RuntimeError('Packaged Waybar unit was not found.')
    links = [(relative, str(PROFILE / relative)) for relative in TARGETS]
    links += [(WAYBAR, unit)]
    if generated:
        links += [(IMSETTINGS_TARGET, str(generated))]
    pending = [(rel, link) for rel, link in links
               if not ((HOME / rel).is_symlink() and os.readlink(HOME / rel) == link)
               or (rel == IMSETTINGS_TARGET and generated and not generated.exists())]
    if not pending:
        print('Sway profile is already linked; no files changed.')
        return
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    backup = HOME / '.local/state/sway-dotfiles/backups' / stamp
    check_parents(backup)
    backup.mkdir(parents=True, mode=0o700)
    manifest = {'home': str(HOME), 'repo': str(REPO), 'entries': []}
    try:
        if generated and not generated.exists():
            generated.parent.mkdir(parents=True, exist_ok=True)
            generated.write_text(text)
        for relative, link in pending:
            target = HOME / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            previous = exists(target)
            if previous:
                saved = backup / 'previous' / relative
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(target, saved)
            # Record the move before linking, so a failed link also rolls back.
            manifest['entries'].append({'path': relative, 'link': link, 'previous': previous})
            (backup / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
            target.symlink_to(link)
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
    except BaseException:
        restore(backup)
        raise
    print(f'Installed {len(pending)} links. Backup: {backup}')
    print(f'Rollback: bash {REPO / "install-sway.sh"} --restore {backup}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--restore', type=Path)
    args = parser.parse_args()
    if args.restore:
        restore(args.restore.expanduser().resolve())
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
    else:
        install()


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f'Installation stopped: {error}', file=sys.stderr)
        sys.exit(1)
