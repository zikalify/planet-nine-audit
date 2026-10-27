import os
from p9paths import DISP, WORK
from response_lib import *
import numpy as np, json

TX,TT=template('b3')  # real coadd-median template, peak-normalized

def fit_at(x,y,sig,x0,base_ann=(4.0,8.0),fitwin=4.0):
    m=np.abs(x-x0)<=base_ann[1]
    xa,ya=x[m],y[m]
    ann=(np.abs(xa-x0)>=base_ann[0])
    base=np.median(ya[ann]) if ann.sum()>5 else np.median(ya)
    f=(np.abs(xa-x0)<=fitwin)
    xf,yf=xa[f],ya[f]-base
    tm=np.interp(xf-x0,TX,TT,left=0,right=0)
    w=tm>0.01
    if w.sum()<10: return None
    A=(yf[w]*tm[w]).sum()/((tm[w]**2).sum())
    return A

def sliding_null(path, exclude):
    hdr,arr=load_ipac(path)
    x,y=arr[:,0],arr[:,1]
    sig=float(hdr.get('sigma',0.1))
    xs=np.arange(-30,30.001,0.2)
    amps=[]
    for x0 in xs:
        if any(a<=x0<=b for a,b in exclude):
            amps.append(np.nan); continue
        A=fit_at(x,y,sig,x0)
        amps.append(A if A is not None else np.nan)
    return x,y,sig,xs,np.array(amps)

# the 7 unique late crossings, profiles from a displaced query whose center is source-free
# (use aug28_q2/sep1_p2 dirs; each crossing's profile is the same physical scan whatever the query center,
#  but the srcfit extraction window is centered on the query position - use the p2/q2 versions)
CROSS={
 'b3_428_025_13':os.path.join(DISP,'aug28_q2','b3_428_025_13_srcfit.tbl'),
 'b3_428_025_32':os.path.join(DISP,'aug28_q2','b3_428_025_32_srcfit.tbl'),
 'b3_436_028_14':os.path.join(DISP,'sep1_p2','b3_436_028_14_srcfit.tbl'),
 'b3_436_028_33':os.path.join(DISP,'sep1_p2','b3_436_028_33_srcfit.tbl'),
 'b3_436_031_15':os.path.join(DISP,'sep1_p2','b3_436_031_15_srcfit.tbl'),
 'b3_436_031_34':os.path.join(DISP,'sep1_c','b3_436_031_34_srcfit.tbl'),
 'b3_436_031_38':os.path.join(DISP,'sep1_p2','b3_436_031_38_srcfit.tbl'),
}
results={}
for name,path in CROSS.items():
    x,y,sig,xs,amps=sliding_null(path,exclude=((-3,3),))
    good=~np.isnan(amps)
    a=amps[good]
    mad=1.4826*np.median(np.abs(a-np.median(a)))
    results[name]=dict(n=int(good.sum()),median=float(np.median(a)),std=float(a.std()),mad=float(mad),
                       p95=float(np.percentile(np.abs(a-np.median(a)),95)))
    print(f"{name}: n={good.sum()} median={np.median(a):+.3f} std={a.std():.3f} MAD={mad:.3f} p95|a-med|={np.percentile(np.abs(a-np.median(a)),95):.3f}")

# injection-recovery with the REAL template at several fluxes and positions
print("\ninjection-recovery (real template, same pipeline):")
inj_results=[]
for name,path in CROSS.items():
    hdr,arr=load_ipac(path)
    x,y=arr[:,0],arr[:,1]
    sig=float(hdr.get('sigma',0.1))
    for flux in [0.1,0.2,0.3]:
        rec=[]
        for xinj in np.arange(-25,25.001,5.0):
            y2=y+flux*np.interp(x-xinj,TX,TT,left=0,right=0)
            A=fit_at(x,y2,sig,xinj)
            if A is not None: rec.append(A)
        rec=np.array(rec)
        inj_results.append(dict(scan=name,flux=flux,n=len(rec),bias=float(rec.mean()-flux),rms=float(rec.std()),min=float(rec.min()),max=float(rec.max())))
        print(f"  {name} inj={flux:.1f} Jy: n={len(rec)} recovered mean={rec.mean():.3f} (bias {rec.mean()-flux:+.3f}) rms={rec.std():.3f} range=[{rec.min():.3f},{rec.max():.3f}]")

json.dump(dict(null=results,inj=inj_results),open(os.path.join(WORK,'sensitivity.json'),'w'),indent=1)
