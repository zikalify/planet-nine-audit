import json
from pathlib import Path
import shutil
import tempfile
import unittest
from p9audit.cli import run

class CLI(unittest.TestCase):
    def test_example(self):
        r=run(Path('examples'),['archive-a','archive-b'])
        self.assertTrue(r['metadata']['synthetic'])
        self.assertEqual(r['followup_rank'][0]['search'],'south-field')
        self.assertEqual(len(r['inputs_sha256']),4)
        self.assertIn('SYNTHETIC',r['warning'])
    def test_reproducible(self):
        self.assertEqual(run(Path('examples'),['archive-a']),run(Path('examples'),['archive-a']))
    def test_missing_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'data'; shutil.copytree('examples',dest)
            (dest/'metadata.json').write_text('{}')
            with self.assertRaises(ValueError): run(dest,[])
    def test_bad_header(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'data'; shutil.copytree('examples',dest)
            (dest/'particles.csv').write_text('wrong\n1\n')
            with self.assertRaises(ValueError): run(dest,[])
