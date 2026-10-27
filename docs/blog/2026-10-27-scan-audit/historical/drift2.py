import numpy as np, glob, re, statistics, json

def load_ipac(path):
    hdr={}
    lines=open(path).read().splitlines()
    for ln in lines:
        if ln.startswith('\\'):
            m=re.match(r'\\(\w+)\s*=\s*(.*)',ln)
            if m: hdr[m.group(1)]=m.group(2).strip()
    di=[i for i,ln in enumerate(lines) if ln.startswith('|')]
    start=max(di)+1 if di else 0
    rows=[]
    for ln in lines[start:]:
        try: rows.append([float(p) for p in ln.split()][:4])
        except: pass
    return hdr, np.array(rows)

def template(band):
    _,arr=load_ipac(f'{band}_coadd_median.tbl')
    m=np.abs(arr[:,0])<=3.0
    x,t=arr[m,0].copy(),arr[m,1].copy()
    t-=t[np.abs(x)>2.0].mean(); t/=t.max()
    return x,t

def refit_arr(x,y,sig,tx,tt):
    m=np.abs(x)<=4.0
    x,y=x[m],y[m]
    best=None
    for x0 in np.arange(-2.0,2.0001,0.01):
        tm=np.interp(x-x0,tx,tt,left=0,right=0); w=tm>0.01
        if w.sum()<10: continue
        A=(y[w]*tm[w]).sum()/(tm[w]**2).sum()
        chi2=(((y[w]-A*tm[w])/sig)**2).sum()
        if best is None or chi2<best[0]: best=(chi2,x0,A)
    chi2,x0,A=best
    tm=np.interp(x-x0,tx,tt,left=0,right=0); w=tm>0.01
    sA=sig/np.sqrt((tm[w]**2).sum())
    return A,sA,x0,chi2,int(w.sum())

# --- parallax machinery ---
eps=np.radians(23.4392911)
ra,dec=np.radians(35.74075),np.radians(-48.5125)
Rv=np.array([[1,0,0],[0,np.cos(eps),np.sin(eps)],[0,-np.sin(eps),np.cos(eps)]])
e=Rv@np.array([np.cos(dec)*np.cos(ra),np.cos(dec)*np.sin(ra),np.sin(dec)])
lam,beta=np.arctan2(e[1],e[0]),np.arcsin(e[2])
def sun_lon(y,mo,d,ut):
    yy,mm=y,mo
    if mm<=2: yy-=1; mm+=12
    A=yy//100; B=2-A+A//4
    JD=int(365.25*(yy+4716))+int(30.6001*(mm+1))+d+B-1524.5+ut/24.
    T=(JD-2451545.0)/36525.
    L0=(280.46646+36000.76983*T)%360; M=357.52911+35999.05029*T
    Mr=np.radians(M)
    return np.radians((L0+(1.914602-0.004817*T)*np.sin(Mr)+0.019993*np.sin(2*Mr))%360)
def apparent(y,mo,d,ut,dist):
    ls=sun_lon(y,mo,d,ut)
    earth=np.array([np.cos(ls+np.pi),np.sin(ls+np.pi),0.])
    obj=dist*np.array([np.cos(beta)*np.cos(lam),np.cos(beta)*np.sin(lam),np.sin(beta)])
    v=obj-earth; return v/np.linalg.norm(v)
east=np.array([-np.sin(ra),np.cos(ra),0.])
north=np.array([-np.sin(dec)*np.cos(ra),-np.sin(dec)*np.sin(ra),np.cos(dec)])
def pred_x0(y,mo,d,ut,pa_deg,dist):
    vref=np.linalg.inv(Rv)@apparent(1983,6,26,16.38,dist)
    v=np.linalg.inv(Rv)@apparent(y,mo,d,ut,dist)
    dvec=v-vref
    dE=float(dvec@east)*180/np.pi*60; dN=float(dvec@north)*180/np.pi*60
    pa=np.radians(pa_deg)
    return dE*np.sin(pa)+dN*np.cos(pa)
def parse_utcs(s):
    m=re.match(r'(\d+)/(\d+)/(\d+)\s+(\d+):(\d+):([\d.]+)',s)
    return 1983,int(m.group(1)),int(m.group(2)),int(m.group(4))+int(m.group(5))/60+float(m.group(6))/3600

# collect fits from srcfit (same as before)
FACS={'b3':0.64,'b4':0.48}
rows=[]
for band in ['b3','b4']:
    tx,tt=template(band)
    for f in sorted(glob.glob(f'{band}_[0-9]*_srcfit.tbl')):
        hdr,arr=load_ipac(f)
        sig=float(hdr.get('sigma',0.1)); pa=float(hdr.get('pa',0))
        A,sA,x0,chi2,n=refit_arr(arr[:,0],arr[:,1],sig,tx,tt)
        yy,mo,dd,ut=parse_utcs(hdr['utcs_start'])
        sAe=sA*FACS[band]
        rows.append(dict(band=band,scan=f.split('_srcfit')[0],pa=pa,A=A,sA=sAe,x0=x0,Asig=A/sAe,yy=yy,mo=mo,dd=dd,ut=ut,det=hdr.get('jdet')))

# extra crossings from scan.tbl (raw scans); estimate sig from |x|>8 arcmin rms
print("== EXTRA crossings (scan.tbl, control) ==")
for f in sorted(glob.glob('b[34]_[0-9]*_scan.tbl')):
    band=f[:2]; hdr,arr=load_ipac(f)
    x,y=arr[:,0],arr[:,1]
    far=np.abs(x)>8.0
    sig=far.sum() and np.std(y[far]-np.median(y[far])) or 0.1
    tx,tt=template(band)
    A,sA,x0,chi2,n=refit_arr(x,y,sig,tx,tt)
    sAe=sA*FACS[band]
    print(f"{f.split('_scan')[0]:18s} off={float(hdr.get('dist',0))/60:+5.2f}'  A={A:6.3f}+-{sAe:.3f} (A/sig={A/sAe:5.1f})  x0={x0:+5.2f}")

# drift test on detected scans
print("\n== DRIFT TEST (detected scans A/sig>3) ==")
det=[r for r in rows if r['Asig']>3]
# x0 uncertainty: use per-scan curvature approx = sA/|A|*0.8? use simpler: sx0 ~ sA/A * template width scale 0.8
for r in det:
    r['sx0']=r['sA']/abs(r['A'])*0.8
    r['pred600']=pred_x0(r['yy'],r['mo'],r['dd'],r['ut'],r['pa'],600)
    r['pred500']=pred_x0(r['yy'],r['mo'],r['dd'],r['ut'],r['pa'],500)
    r['pred700']=pred_x0(r['yy'],r['mo'],r['dd'],r['ut'],r['pa'],700)
# static model: x0 = const (weighted mean)
w=np.array([1/r['sx0']**2 for r in det]); xs=np.array([r['x0'] for r in det])
c=(w*xs).sum()/w.sum()
chi2_static=(w*(xs-c)**2).sum()
print(f"static: weighted mean x0={c:+.3f}'  chi2={chi2_static:.1f} on {len(det)-1} dof")
for dist in (500,600,700):
    pr=np.array([r[f'pred{dist}'] for r in det])
    chi2_m=(w*(xs-pr)**2).sum()
    print(f"mover {dist} AU: chi2={chi2_m:.1f} on {len(det)} dof   (delta-chi2 vs static = {chi2_m-chi2_static:.0f})")
print(f"\ndetected scans: {len(det)} of {len(rows)}; sx0 typ {np.median([r['sx0'] for r in det]):.3f}'")

# what distance gives predicted RMS = observed scatter? solve pred(d) amplitude < 0.5'
p600=np.array([r['pred600'] for r in det])
print(f"predicted |x0| range at 600 AU: {np.abs(p600).min():.2f}..{np.abs(p600).max():.2f}'; scales as 600/d")
