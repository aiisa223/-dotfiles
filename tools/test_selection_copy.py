import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'sway-desktop/.local/bin/sway-selection-copy'


class SelectionCopyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        command = self.root / 'wl-copy'
        command.write_text('#!/usr/bin/python3\nimport json, os, sys\n'
                           'from pathlib import Path\n'
                           'Path(os.environ["TEST_CALL"]).write_text(json.dumps(sys.argv[1:]))\n'
                           'Path(os.environ["TEST_DATA"]).write_bytes(sys.stdin.buffer.read())\n')
        command.chmod(0o755)
        self.call = self.root / 'args.json'
        self.data = self.root / 'data'

    def copy(self, state, data=b''):
        env = dict(os.environ, PATH=f'{self.root}:{os.environ["PATH"]}',
                   CLIPBOARD_STATE=state, TEST_CALL=str(self.call), TEST_DATA=str(self.data))
        subprocess.run(['bash', str(SCRIPT)], input=data, env=env, check=True)

    def test_text_preserves_bytes_and_trailing_newline(self):
        data = 'line one\nλ line two\n'.encode()
        self.copy('data', data)
        self.assertEqual(self.data.read_bytes(), data)
        self.assertEqual(json.loads(self.call.read_text()), ['--type', 'text/plain'])

    def test_cleared_selection_does_not_overwrite_clipboard(self):
        for state in ('nil', 'clear'):
            self.copy(state)
            self.assertFalse(self.call.exists())

    def test_sensitive_hint_is_preserved(self):
        self.copy('sensitive', b'selected text')
        self.assertEqual(json.loads(self.call.read_text()), ['--type', 'text/plain', '--sensitive'])


if __name__ == '__main__':
    unittest.main()
