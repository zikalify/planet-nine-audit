import os
from p9paths import DISP
from response_lib import *
import numpy as np, glob, os, json

for p in ['sep1_c','aug28_c','aug28_q4']:
    d=os.path.join(DISP,p)
    files=sorted(glob.glob(f'{d}/b3_[0-9]*_srcfit.tbl'))
    rows=[]
    for f in files:
        hdr,res=refit(f)
        cs=float(hdr.get('cross_scan','nan'))
        dt=scan_date(hdr)
        if res is None:
            rows.append(dict(scan=os.path.basename(f)[:-11],date=dt,cross=cs,A=None)); continue
        A,sA,x0,mad,Aoff=res
        rows.append(dict(scan=os.path.basename(f)[:-11],date=dt,cross=cs,A=A,sA=sA,mad=mad,det=int(hdr['jdet'])))
    late=[r for r in rows if r['date'] and r['date']>='1983-08-01']
    tight=[r for r in late if abs(r['cross'])<1.7 and r['A'] is not None]
    print(f"\n-- {p}: {len(files)} srcfit ({len(late)} late-epoch)")
    for r in sorted(late,key=lambda r:abs(r['cross'])):
        if r['A'] is None:
            print(f"   {r['scan']:18s} {r['date']} cross={r['cross']:+.3f}  fit FAILED"); continue
        tag=' <== tight' if abs(r['cross'])<1.7 else ''
        print(f"   {r['scan']:18s} {r['date']} cross={r['cross']:+.3f}  A={r['A']:+.3f}+-{r['sA']:.3f} (formal) MADbg={r['mad']:.3f}{tag}")
    if tight:
        As=np.array([r['A'] for r in tight]); mads=np.array([r['mad'] for r in tight])
        print(f"   tight: n={len(tight)}, mean A={As.mean():+.3f}+-{As.std(ddof=1)/np.sqrt(len(As)):.3f} Jy; bg MAD {mads.min():.3f}-{mads.max():.3f}; required>=0.19")
    else:
        print("   WARNING: no tight late-epoch crossing")
