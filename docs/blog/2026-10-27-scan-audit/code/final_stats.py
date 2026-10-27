import os
from p9paths import DISP, WORK
from response_lib import *
import numpy as np, glob, os, json

_names=['sep1_p1','sep1_p2','sep1_p3','sep1_p4','aug28_q1','aug28_q2','aug28_q3','sep1_c','aug28_c','aug28_q4']
pts={p: os.path.join(DISP,p) for p in _names}
all_tight=[]
per_point={}
for p,d in pts.items():
    rows=[]
    for f in sorted(glob.glob(f'{d}/b3_[0-9]*_srcfit.tbl')):
        hdr,res=refit(f)
        if res is None: continue
        A,sA,x0,mad,Aoff=res
        cs=float(hdr.get('cross_scan','nan')); dt=scan_date(hdr)
        det=int(hdr['jdet'])
        if dt and dt>='1983-08-01' and abs(cs)<1.7:
            rows.append(dict(scan=os.path.basename(f)[:-11],date=dt,det=det,cross=cs,A=A,mad=mad))
    per_point[p]=rows
    all_tight+= [dict(point=p,**r) for r in rows]

print(f"total tight late-epoch crossings across 10 points: {len(all_tight)}")
As=np.array([r['A'] for r in all_tight])
print(f"ALL:  mean={As.mean():+.4f}  SEM={As.std(ddof=1)/np.sqrt(len(As)):.4f}  median={np.median(As):+.4f}")
no33=[r['A'] for r in all_tight if not (r['det']==33 and r['date']=='1983-09-01')]
print(f"excl det33-Sep1: n={len(no33)}  mean={np.mean(no33):+.4f}  SEM={np.std(no33,ddof=1)/np.sqrt(len(no33)):.4f}")
no33_15=[r['A'] for r in all_tight if not (r['det']==33 and r['date']=='1983-09-01') and not (r['det']==15 and r['date']=='1983-09-01')]
print(f"excl det33+det15-Sep1: n={len(no33_15)}  mean={np.mean(no33_15):+.4f}  SEM={np.std(no33_15,ddof=1)/np.sqrt(len(no33_15)):.4f}")
# unique scan-date-det combos (same crossing queried at multiple points are correlated; note it)
uniq=set((r['scan'],r['date']) for r in all_tight)
print(f"unique crossings (scan,date): {len(uniq)}")
# per-point means
print("\nper-point tight means:")
for p,rows in per_point.items():
    a=np.array([r['A'] for r in rows])
    print(f"  {p}: n={len(a)} mean={a.mean():+.3f}+-{a.std(ddof=1)/np.sqrt(len(a)):.3f}")
json.dump(all_tight,open(os.path.join(WORK,'all_tight.json'),'w'),indent=1,default=str)
