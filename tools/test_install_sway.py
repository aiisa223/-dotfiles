import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import install_sway as installer


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.unit = self.home / 'packaged-waybar.service'
        self.unit.write_text('[Unit]\nDescription=Test fixture\n')
        self.patches = [patch.object(installer, 'HOME', self.home),
                        patch.object(installer.subprocess, 'check_output', return_value=str(self.unit)),
                        patch.object(installer.subprocess, 'run')]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def install(self):
        with contextlib.redirect_stdout(io.StringIO()):
            installer.install()
        return next((self.home / '.local/state/sway-dotfiles/backups').iterdir())

    def test_existing_directory_and_broken_link_restore_exactly(self):
        kitty = self.home / '.config/kitty'
        kitty.mkdir(parents=True)
        (kitty / 'custom.conf').write_text('keep me')
        rofi = self.home / '.config/rofi'
        rofi.symlink_to('missing-old-checkout')
        backup = self.install()
        self.assertTrue(kitty.is_symlink())
        self.assertEqual(os.readlink(rofi), str(installer.PROFILE / '.config/rofi'))
        with contextlib.redirect_stdout(io.StringIO()):
            installer.restore(backup)
        self.assertEqual((kitty / 'custom.conf').read_text(), 'keep me')
        self.assertEqual(os.readlink(rofi), 'missing-old-checkout')
        self.assertFalse(os.path.lexists(self.home / '.config/sway'))
        self.assertFalse(os.path.lexists(self.home / installer.WAYBAR))

    def test_idempotent_install(self):
        backup = self.install()
        with contextlib.redirect_stdout(io.StringIO()):
            installer.install()
        self.assertEqual(list(backup.parent.iterdir()), [backup])

    def test_refuse_parent_symlink_without_modification(self):
        external = self.home / 'other-dotfiles'
        external.mkdir()
        (self.home / '.config').symlink_to(external)
        with self.assertRaises(RuntimeError):
            installer.install()
        self.assertEqual(list(external.iterdir()), [])

    def test_restore_refuses_changed_destination_before_any_changes(self):
        backup = self.install()
        sway = self.home / '.config/sway'
        sway.unlink()
        sway.mkdir()
        (sway / 'config').write_text('new user work')
        with self.assertRaises(RuntimeError):
            installer.restore(backup)
        self.assertTrue((self.home / '.config/kitty').is_symlink())
        self.assertEqual((sway / 'config').read_text(), 'new user work')

    def test_failed_daemon_reload_rolls_back(self):
        with patch.object(installer.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'systemctl')):
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(subprocess.CalledProcessError):
                installer.install()
        for relative in installer.TARGETS + [installer.WAYBAR]:
            self.assertFalse(os.path.lexists(self.home / relative))


if __name__ == '__main__':
    unittest.main()
