import sys, os
BUNDLE=os.environ.get('P9BUNDLE', os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BUNDLE)
from response_lib import *
import numpy as np, json
DISP=os.environ.get('P9DISP', os.path.join(BUNDLE,'disp'))  # displaced-point dirs ship in disp/
WORK=os.environ.get('P9WORK', os.path.join(BUNDLE,'work'))
os.makedirs(WORK, exist_ok=True)

TX,TT=template('b3')
# broadened/narrowed template variants for mismatch injection
def stretched(txfac):
    return TX*txfac, TT

def fit_at(x,y,sig,x0,base_ann=(4.0,8.0),fitwin=4.0,tx=TX,tt=TT):
    m=np.abs(x-x0)<=base_ann[1]
    xa,ya=x[m],y[m]
    ann=(np.abs(xa-x0)>=base_ann[0])
    base=np.median(ya[ann]) if ann.sum()>5 else np.median(ya)
    f=(np.abs(xa-x0)<=fitwin)
    xf,yf=xa[f],ya[f]-base
    tm=np.interp(xf-x0,tx,tt,left=0,right=0)
    w=tm>0.01
    if w.sum()<10: return None
    return (yf[w]*tm[w]).sum()/((tm[w]**2).sum())

CROSS={
 'b3_428_025_13': os.path.join(DISP,'aug28_q2','b3_428_025_13_srcfit.tbl'),
 'b3_428_025_32': os.path.join(DISP,'aug28_q2','b3_428_025_32_srcfit.tbl'),
 'b3_436_028_14': os.path.join(DISP,'sep1_p2','b3_436_028_14_srcfit.tbl'),
 'b3_436_028_33': os.path.join(DISP,'sep1_p2','b3_436_028_33_srcfit.tbl'),
 'b3_436_031_15': os.path.join(DISP,'sep1_p2','b3_436_031_15_srcfit.tbl'),
 'b3_436_031_34': os.path.join(DISP,'sep1_c','b3_436_031_34_srcfit.tbl'),
 'b3_436_031_38': os.path.join(DISP,'sep1_p2','b3_436_031_38_srcfit.tbl'),
}
out={}
print("=== A. null in the ACTUAL tested window |x0|<=2' (annulus contains static-source wing at ~4-5') ===")
for name,path in CROSS.items():
    hdr,arr=load_ipac(path); x,y=arr[:,0],arr[:,1]; sig=float(hdr.get('sigma',0.1))
    amps=[]
    for x0 in np.arange(-2,2.001,0.05):
        A=fit_at(x,y,sig,x0)
        if A is not None: amps.append(A)
    a=np.array(amps)
    out[name]=dict(win_null_med=float(np.median(a)),win_null_mad=float(1.4826*np.median(np.abs(a-np.median(a)))),
                   win_null_p95=float(np.percentile(np.abs(a-np.median(a)),95)),win_min=float(a.min()),win_max=float(a.max()))
    print(f"{name}: n={len(a)} med={np.median(a):+.3f} MAD={1.4826*np.median(np.abs(a-np.median(a))):.3f} p95={np.percentile(np.abs(a-np.median(a)),95):.3f} range=[{a.min():+.3f},{a.max():+.3f}]")

print("\n=== B. injection at the ACTUAL mover offsets (xinj in [-1.5,+1.5], real profile incl. source wing) ===")
for name,path in CROSS.items():
    hdr,arr=load_ipac(path); x,y=arr[:,0],arr[:,1]; sig=float(hdr.get('sigma',0.1))
    for flux in [0.2,0.3]:
        rec=[]
        for xinj in np.arange(-1.5,1.5001,0.3):
            y2=y+flux*np.interp(x-xinj,TX,TT,left=0,right=0)
            A=fit_at(x,y2,sig,xinj)
            if A is not None: rec.append(A)
        rec=np.array(rec)
        print(f"  {name} inj={flux:.1f}: n={len(rec)} mean={rec.mean():.3f} bias={rec.mean()-flux:+.3f} rms={rec.std():.3f} min={rec.min():+.3f}")

print("\n=== C. template-mismatch injection (inject 1.5x and 0.67x broadened source, recover with nominal) ===")
for name in ['b3_428_025_32','b3_436_031_15','b3_436_031_38']:
    path=CROSS[name]
    hdr,arr=load_ipac(path); x,y=arr[:,0],arr[:,1]; sig=float(hdr.get('sigma',0.1))
    for fac in [1.5,0.67]:
        tx2,tt2=stretched(fac)
        rec=[]
        for xinj in np.arange(-1.5,1.5001,0.3):
            y2=y+0.2*np.interp(x-xinj,tx2,tt2,left=0,right=0)
            A=fit_at(x,y2,sig,xinj)  # recover with NOMINAL template
            if A is not None: rec.append(A)
        rec=np.array(rec)
        print(f"  {name} inject 0.2 Jy x width*{fac}: recovered mean={rec.mean():.3f} (recovered fraction {rec.mean()/0.2:.2f}) rms={rec.std():.3f}")

json.dump(out,open(os.path.join(WORK,'sensitivity2_window.json'),'w'),indent=1)
