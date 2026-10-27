import numpy as np, glob, re, json, os

def load_ipac(path):
    hdr={}
    with open(path) as f: lines=f.read().splitlines()
    for ln in lines:
        if ln.startswith('\\'):
            m=re.match(r'\\(\w+)\s*=\s*(.*)',ln)
            if m: hdr[m.group(1)]=m.group(2).strip()
    di=[i for i,ln in enumerate(lines) if ln.startswith('|')]
    start=max(di)+1 if di else 0
    rows=[]
    for ln in lines[start:]:
        parts=ln.split()
        try: rows.append([float(p) for p in parts][:4])
        except: pass
    return hdr, np.array(rows) if rows else np.empty((0,4))

from p9paths import PROF, WIDE, WORK, TEMPL
def template(band):
    hdr,arr=load_ipac(f'{TEMPL}/{band}_coadd_median.tbl')
    m=np.abs(arr[:,0])<=3.0
    x,t=arr[m,0],arr[m,1]
    t=t-t[np.abs(x)>2.0].mean()
    return x,t/t.max()

TX,TT=template('b3')
def refit(path,x0free=True):
    hdr,arr=load_ipac(path)
    if len(arr)==0: return hdr,None
    sig=float(hdr.get('sigma',0.1))
    m=np.abs(arr[:,0])<=4.0
    x,y=arr[m,0],arr[m,1]
    best=None
    grid=np.arange(-2.0,2.0001,0.01) if x0free else [0.0]
    for x0 in grid:
        tm=np.interp(x-x0,TX,TT,left=0,right=0)
        w=(tm>0.01)
        if w.sum()<10: continue
        A=(y[w]*tm[w]).sum()/((tm[w]**2).sum())
        chi2=(((y[w]-A*tm[w])/sig)**2).sum()
        if best is None or chi2<best[0]: best=(chi2,x0,A)
    if best is None: return hdr,None
    chi2,x0,A=best
    tm=np.interp(x-x0,TX,TT,left=0,right=0); w=tm>0.01
    sA=sig/np.sqrt((tm[w]**2).sum())
    # empirical null: MAD of matched-filter amp over |x|>6
    mo=np.abs(arr[:,0])>6.0
    xo,yo=arr[mo,0],arr[mo,1]
    tmo=np.interp(xo,TX,TT,left=0,right=0); wo=tmo>0.01
    Aoffs=(yo[wo]*tmo[wo]).sum()/((tmo[wo]**2).sum()) if wo.sum()>10 else np.nan
    # scatter: per-point residual-based MAD on off-source fit residuals is complex; use profile MAD
    mad=1.4826*np.median(np.abs(yo-np.median(yo)))
    return hdr,(A,sA,x0,mad,Aoffs)

def scan_date(hdr):
    u=hdr.get('utcs_start','')
    m=re.match(r'(\d+)/(\d+)/(\d+)',u)
    if not m: return None
    mo,dd,yy=int(m.group(1)),int(m.group(2)),int(m.group(3))
    return f"19{yy:02d}-{mo:02d}-{dd:02d}"

rows=[]
for run,pat in [('default',f'{PROF}/b3_[0-9]*_srcfit.tbl'),('wide',f'{WIDE}/b3_[0-9]*_srcfit.tbl')]:
    for f in sorted(glob.glob(pat)):
        hdr,res=refit(f)
        if res is None: continue
        A,sA,x0,mad,Aoff=res
        cs=float(hdr.get('cross_scan','nan'))
        rows.append(dict(run=run,scan=os.path.basename(f).replace('_srcfit.tbl',''),
            sop=int(hdr['sop']),obs=int(hdr['obs']),det=int(hdr['jdet']),
            date=scan_date(hdr),cross=cs,A=A,sA=sA,x0=x0,mad=mad,Aoff=Aoff))
# per-SOP reference amplitude from |cross|<1.0 crossings
import collections
sops=collections.defaultdict(list)
for r in rows:
    if abs(r['cross'])<1.0: sops[(r['sop'],r['obs'])].append(r['A'])
ref={k:np.median(v) for k,v in sops.items() if v}
print("SOP reference amplitudes (|cross|<1', 60um):")
for k,v in sorted(ref.items()): print(f"  SOP{k[0]} OBS{k[1]}: A_ref={v:.3f} Jy (n={len(sops[k])})")
print(f"\n{'scan':18s} {'date':10s} {'det':>3s} {'cross':>7s} {'A(Jy)':>8s} {'sA':>6s} {'R':>6s}")
out=[]
for r in sorted(rows,key=lambda r:(r['date'],abs(r['cross']))):
    k=(r['sop'],r['obs']); R=r['A']/ref[k] if k in ref and ref[k]>0.05 else np.nan
    r['R']=R; out.append(r)
    print(f"{r['scan']:18s} {r['date']:10s} {r['det']:3d} {r['cross']:+7.3f} {r['A']:+8.3f} {r['sA']:6.3f} {R:6.2f}" if R==R else
          f"{r['scan']:18s} {r['date']:10s} {r['det']:3d} {r['cross']:+7.3f} {r['A']:+8.3f} {r['sA']:6.3f}    n/a")
json.dump(out,open(os.path.join(WORK,'response_rows.json'),'w'),indent=1)
# binned response
big=[r for r in out if r.get('R')==r.get('R') and abs(r['cross'])>1.0]
print(f"\nlarge-offset crossings (|cross|>1'): {len(big)}")
for lo,hi in [(1.0,1.5),(1.5,2.0),(2.0,2.5),(2.5,3.0)]:
    sel=[r['R'] for r in big if lo<=abs(r['cross'])<hi]
    if sel: print(f"  {lo:.1f}-{hi:.1f}': median R={np.median(sel):.2f}  n={len(sel)}  values={['%.2f'%v for v in sel]}")
