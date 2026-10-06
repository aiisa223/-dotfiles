from pathlib import Path
import runpy
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTROLS = runpy.run_path(str(ROOT / 'sway-desktop/.local/bin/sway-controls'))


class ControlsTests(unittest.TestCase):
    def test_mode_bindings_includes_variables_and_gestures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'extra.conf').write_text('bindgesture swipe:3:left workspace next\n')
            (root / 'config').write_text('set $mod Mod4\nset $ws "1:code"\n'
                'bindsym $mod+1 workspace $ws\nmode "resize" {\n'
                '    bindsym h resize shrink width 10 px\n}\n'
                'include extra.conf\ninclude extra.conf\n')
            rows = CONTROLS['bindings'](root / 'config')
            self.assertEqual(rows, ['[default] bindsym: Super+1 workspace 1:code',
                '[resize] bindsym: h resize shrink width 10 px',
                '[default] bindgesture: swipe:3:left workspace next'])

    def test_profile_has_no_duplicate_chords_within_modes(self):
        rows = CONTROLS['bindings'](ROOT / 'sway-desktop/.config/sway/config')
        identities = []
        for row in rows:
            if 'bindsym:' not in row:
                continue
            mode, rest = row.split(' bindsym: ', 1)
            fields = rest.split()
            flags = []
            while fields[0].startswith('--'):
                flags.append(fields.pop(0))
            chord = tuple(sorted(fields[0].split('+')))
            identity = (mode, tuple(sorted(flags)), chord)
            self.assertNotIn(identity, identities, row)
            identities.append(identity)
        for key, direction in zip('hjkl', ('left', 'down', 'up', 'right')):
            self.assertIn(f'[default] bindsym: Super+{key} focus {direction}', rows)
            self.assertIn(f'[default] bindsym: Super+Shift+{key} move {direction}', rows)
        self.assertIn('[default] bindsym: Super+Alt+h splith', rows)
        self.assertTrue(any(row.startswith('[gaps] bindsym: h ') for row in rows))
        self.assertTrue(any(row.startswith('[resize] bindsym: h ') for row in rows))


if __name__ == '__main__':
    unittest.main()
