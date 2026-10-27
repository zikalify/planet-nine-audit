import numpy as np, glob, re

def load_ipac(path):
    hdr={}
    with open(path) as f:
        lines=f.read().splitlines()
    for ln in lines:
        if ln.startswith('\\'):
            m=re.match(r'\\(\w+)\s*=\s*(.*)',ln)
            if m: hdr[m.group(1)]=m.group(2).strip()
    di=[i for i,ln in enumerate(lines) if ln.startswith('|')]
    start=max(di)+1 if di else 0
    rows=[]
    for ln in lines[start:]:
        parts=ln.split()
        try:
            vals=[float(p) for p in parts]
            rows.append(vals[:4])
        except: pass
    return hdr, np.array(rows) if rows else np.empty((0,4))

def template(band):
    hdr,arr=load_ipac(f'{band}_coadd_median.tbl')
    m=np.abs(arr[:,0])<=3.0
    x,t=arr[m,0],arr[m,1]
    t=t-t[np.abs(x)>2.0].mean()
    t=t/t.max()
    return x,t

def refit(path,tx,tt):
    hdr,arr=load_ipac(path)
    sig=float(hdr.get('sigma',0.1))
    m=np.abs(arr[:,0])<=4.0
    x,y=arr[m,0],arr[m,1]
    best=None
    for x0 in np.arange(-2.0,2.0001,0.01):
        tm=np.interp(x-x0,tx,tt,left=0,right=0)
        w=(tm>0.01)
        if w.sum()<10: continue
        A=(y[w]*tm[w]).sum()/(tm[w]**2).sum()
        chi2=(((y[w]-A*tm[w])/sig)**2).sum()
        if best is None or chi2<best[0]: best=(chi2,x0,A)
    chi2,x0,A=best
    tm=np.interp(x-x0,tx,tt,left=0,right=0); w=tm>0.01
    sA=sig/np.sqrt((tm[w]**2).sum())
    def c2(xx):
        t2=np.interp(x-xx,tx,tt,left=0,right=0); ww=t2>0.01
        A2=(y[ww]*t2[ww]).sum()/(t2[ww]**2).sum()
        return (((y[ww]-A2*t2[ww])/sig)**2).sum()
    curv=(c2(x0+0.05)-2*chi2+c2(x0-0.05))/0.05**2
    sx0=np.sqrt(2/curv) if curv>0 else np.nan
    return hdr.get('utcs_start','?'),sig,A,sA,x0,sx0,chi2,int(w.sum())

for band in ['b3','b4']:
    tx,tt=template(band)
    print(f"== {band} ==")
    print(f"{'scan':16s} {'utc_start':20s} {'sigma':>6s}  {'A(Jy)':>14s}  {'x0(arcmin)':>16s}  chi2/n")
    for f in sorted(glob.glob(f'{band}_[0-9]*_srcfit.tbl')):
        utc,sig,A,sA,x0,sx0,chi2,n=refit(f,tx,tt)
        tag=f.split('_srcfit')[0]
        print(f"{tag:16s} {utc:20s} {sig:6.3f}  {A:6.3f}+-{sA:.3f}  {x0:+6.2f}+-{sx0:5.2f}  {chi2/n:5.2f}")
