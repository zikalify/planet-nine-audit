import os
from p9paths import PROF, WIDE, DISP, WORK
from response_lib import *
import numpy as np, glob, os, json

print("=== fixed-position small-offset response controls (deduped) ===")
seen={}
for run,pat in [('default',f'{PROF}/b3_[0-9]*_srcfit.tbl'),('wide',f'{WIDE}/b3_[0-9]*_srcfit.tbl')]:
    for f in sorted(glob.glob(pat)):
        name=os.path.basename(f).replace('_srcfit.tbl','')
        if name in seen: continue
        hdr,res=refit(f)
        if res is None: continue
        A,sA,x0,mad,Aoff=res
        cs=float(hdr.get('cross_scan','nan'))
        seen[name]=dict(scan=name,date=scan_date(hdr),det=int(hdr['jdet']),cross=cs,A=A,sA=sA,mad=mad,sop=int(hdr['sop']),obs=int(hdr['obs']))
ctrl=[v for v in seen.values() if 1.0<abs(v['cross'])<1.7]
for v in sorted(ctrl,key=lambda r:abs(r['cross'])):
    print(f"  {v['scan']:18s} {v['date']} det{v['det']:2d} cross={v['cross']:+.3f}  A={v['A']:+.3f}+-{v['sA']:.3f}")

print("\n=== displaced-point coverage (60um) ===")
pts=['sep1_p1','sep1_p2','sep1_p3','sep1_p4','aug28_q1','aug28_q2','aug28_q3']
REQ=0.19
allcov={}
for p in pts:
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
    allcov[p]=dict(late=late,tight=tight)
    print(f"\n-- {p}: {len(files)} srcfit ({len(late)} late-epoch)")
    for r in sorted(late,key=lambda r:abs(r['cross'])):
        if r['A'] is None:
            print(f"   {r['scan']:18s} {r['date']} cross={r['cross']:+.3f}  fit FAILED"); continue
        tag=' <== tight' if abs(r['cross'])<1.7 else ''
        print(f"   {r['scan']:18s} {r['date']} cross={r['cross']:+.3f}  A={r['A']:+.3f}+-{r['sA']:.3f} (formal) MADbg={r['mad']:.3f}{tag}")
    if tight:
        As=np.array([r['A'] for r in tight]); mads=np.array([r['mad'] for r in tight])
        print(f"   tight: n={len(tight)}, mean A={As.mean():+.3f}+-{As.std(ddof=1)/np.sqrt(len(As)):.3f} Jy; bg MAD {mads.min():.3f}-{mads.max():.3f}; required>={REQ}")
    else:
        print("   WARNING: no tight late-epoch crossing")
json.dump(allcov,open(os.path.join(WORK,'disp_coverage.json'),'w'),indent=1,default=str)
