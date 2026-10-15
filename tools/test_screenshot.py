import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'sway-desktop/.local/bin/sway-screenshot'


class ScreenshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.pictures = self.root / 'Pictures with spaces'
        self.log = self.root / 'calls.jsonl'
        self.env = dict(os.environ, HOME=str(self.root), XDG_RUNTIME_DIR=str(self.root),
                        PATH=f'{self.bin}:{os.environ["PATH"]}',
                        TEST_PICTURES=str(self.pictures), TEST_LOG=str(self.log))
        self.mock('slurp', 'printf "10,20 300x200\\n"')
        self.mock('xdg-user-dir', 'printf "%s\\n" "$TEST_PICTURES"')
        self.mock('swaymsg', 'printf \'[{"name":"eDP-1","focused":true}]\\n\'')
        for command in ('grim', 'notify-send'):
            path = self.bin / command
            path.write_text('#!/usr/bin/python3\nimport json, os, sys\n'
                            'with open(os.environ["TEST_LOG"], "a") as log:\n'
                            '    log.write(json.dumps([sys.argv[0].split("/")[-1], *sys.argv[1:]]) + "\\n")\n')
            path.chmod(0o755)

    def mock(self, command, body):
        path = self.bin / command
        path.write_text('#!/bin/sh\n' + body + '\n')
        path.chmod(0o755)

    def run_capture(self, mode='region'):
        subprocess.run(['bash', str(SCRIPT), mode], env=self.env, check=True)
        return [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_region_geometry_and_path_are_single_arguments(self):
        calls = self.run_capture()
        self.assertEqual(calls[0][:3], ['grim', '-g', '10,20 300x200'])
        self.assertEqual(Path(calls[0][3]).parent, self.pictures / 'Screenshots')
        self.assertEqual(calls[1], ['notify-send', 'Screenshot saved', calls[0][3]])

    def test_cancel_and_empty_selection_never_capture(self):
        for body in ('exit 1', 'exit 0'):
            with self.subTest(body=body):
                self.mock('slurp', body)
                self.assertEqual(self.run_capture(), [])
                self.assertFalse(self.pictures.exists())

    def test_focused_output(self):
        self.assertEqual(self.run_capture('output')[0][:3], ['grim', '-o', 'eDP-1'])

    def test_duplicate_selector_is_suppressed(self):
        import fcntl
        with (self.root / 'sway-screenshot.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertEqual(self.run_capture(), [])


if __name__ == '__main__':
    unittest.main()
