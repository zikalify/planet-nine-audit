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

import os
TEMPL=os.environ.get('P9TEMPL', os.path.dirname(os.path.abspath(__file__)))  # bundle dir contains b3_coadd_median.tbl
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
