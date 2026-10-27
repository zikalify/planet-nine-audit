"""Shared path config for the Planet Nine audit pipeline.
Defaults assume the shipped bundle layout (all data inside this directory).
Override any root with env vars: P9WORK P9PROF P9WIDE P9DISP P9TEMPL."""
import os
HERE=os.path.dirname(os.path.abspath(__file__))
WORK=os.environ.get('P9WORK', os.path.join(HERE,'work'))      # regenerated intermediates
PROF=os.environ.get('P9PROF', os.path.join(HERE,'profiles'))  # default-run srcfit tables
WIDE=os.environ.get('P9WIDE', os.path.join(HERE,'wide'))      # wide re-run srcfit tables
DISP=os.environ.get('P9DISP', os.path.join(HERE,'disp'))      # displaced-point query dirs (10 subdirs)
TEMPL=os.environ.get('P9TEMPL', HERE)                          # b3/b4_coadd_median.tbl location
os.makedirs(WORK, exist_ok=True)
