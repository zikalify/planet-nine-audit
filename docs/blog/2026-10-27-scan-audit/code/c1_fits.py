# c1_fits.py - regenerate the core C1 per-scan 60um fit table (A, sA, x0) from the shipped
# srcfit profiles, using the pipeline's own fitter (response_lib.refit). This makes the
# C1 amplitude/stability numbers independently regenerable inside the runnable bundle.
# The richer historical fields (Asig, fac, parallax predictions) remain provenance-only
# in historical/ (drift2.py) - this script covers exactly what C1 claims.
import os, glob, json
from p9paths import PROF, WIDE, WORK
from response_lib import refit, scan_date, load_ipac

rows=[]
for run,pat in [('default',os.path.join(PROF,'b3_[0-9]*_srcfit.tbl')),
                ('wide',os.path.join(WIDE,'b3_[0-9]*_srcfit.tbl'))]:
    for f in sorted(glob.glob(pat)):
        hdr,res=refit(f)
        if res is None: continue
        A,sA,x0,mad,Aoff=res
        rows.append(dict(run=run,scan=os.path.basename(f).replace('_srcfit.tbl',''),
                         date=scan_date(hdr),det=int(hdr['jdet']),
                         cross=float(hdr.get('cross_scan','nan')),
                         A=A,sA=sA,x0=x0,mad=mad))
json.dump(rows,open(os.path.join(WORK,'c1_b3_fits.json'),'w'),indent=1)
As=[r['A'] for r in rows if abs(r['cross'])<1.7]
import numpy as np
print(f"n={len(rows)} fits ({len(As)} tight |cross|<1.7)")
print(f"A range: {min(As):.3f}..{max(As):.3f} Jy")
x0s=[r['x0'] for r in rows if abs(r['cross'])<1.7]
print(f"x0 range: {min(x0s):+.2f}..{max(x0s):+.2f} arcmin")
