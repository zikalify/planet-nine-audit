from pathlib import Path
import tempfile
import unittest
from p9audit.caltech import summarize

class Caltech(unittest.TestCase):
    def test_unreviewed_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.csv'; p.write_text('index,ZTF,DES,PS1\n0,1,0,0\n')
            with self.assertRaises(ValueError): summarize(p)
