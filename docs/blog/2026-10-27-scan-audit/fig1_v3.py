# fig1 v3: fixed-position diagnostic profiles. Mover markers computed from validated geo.py
# (JPL Horizons vectors; reproduces queried coords to 0.007'), anchor = coadd center Jul 3 08:00 UT,
# d = 600 AU, projected in-scan per scan PA. SUPERSEDES earlier fig1 versions whose markers were
# hardcoded (-1.1/-1.2/-4.9/-5.4/-5.2) and whose script was not archived.
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from p9paths import PROF
from response_lib import *
import numpy as np, json, re
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geo
earth=geo.earth; Rv=geo.Rv; east=geo.east; north=geo.north; dec=geo.dec; RA0=geo.RA0; DEC0=geo.DEC0; jd2=geo.jd2
def pos_eq(jd,jd0,d):
    dE=earth(jd)-earth(jd0)
    off=-np.linalg.inv(Rv)@dE/d
    dra=np.degrees(np.dot(off,east)/np.cos(dec)); ddec=np.degrees(np.dot(off,north))
    return dra,ddec  # arcmin offsets (dRA*cos-dec corrected? dra is degrees*cos? -> see below)
# note: dra from geo.py variant = degrees( off.east/cos(dec) ) -> in arcmin via *60; caller used /60 for degrees
JD_ANCHOR=jd2(1983,7,3,8.0)
panels=[('Jun 26 det32','b3_303_038_32'),('Jul 9 det35','b3_330_019_35'),('Jul 10 det38','b3_330_030_38'),
        ('Aug 28 det13','b3_428_025_13'),('Sep 1 det38','b3_436_031_38'),('Sep 1 det14','b3_436_028_14')]
def utcs_to_jd(s):
    m=re.match(r'(\d+)/(\d+)/(\d+)\s+(\d+):(\d+):([\d.]+)',s)
    return jd2(1983,int(m.group(1)),int(m.group(2)),int(m.group(4))+int(m.group(5))/60+float(m.group(6))/3600)
TX,TT=template('b3')
fits=json.load(open(os.path.join(HERE,'work','per_scan_fits.json')))
markers={}
fig,axes=plt.subplots(2,3,figsize=(13,7))
for ax,(title,scan) in zip(axes.ravel(),panels):
    f=os.path.join(PROF,f'{scan}_srcfit.tbl')
    hdr,arr=load_ipac(f)
    pa=float(hdr['pa']); jd=utcs_to_jd(hdr['utcs_start'])
    dra,ddec=pos_eq(jd,JD_ANCHOR,600.0)  # degrees
    dE_min=dra*60; dN_min=ddec*60
    par=np.radians(pa)
    x0_pred=dE_min*np.sin(par)+dN_min*np.cos(par)  # in-scan projection, drift2 convention
    markers[scan]=round(x0_pred,2)
    x,y=arr[:,0],arr[:,1]
    w=np.hanning(9); w/=w.sum(); ys=np.convolve(y,w,mode='same')
    ax.plot(x,ys,color='gray',lw=0.9,label='scan profile (0.7-arcmin smoothed)')
    fit=[q for q in fits if q['scan']==scan]
    if fit:
        A=fit[0]['A']; x0=fit[0]['x0']
        xs=np.linspace(-4,4,400)
        ax.plot(xs,A*np.interp(xs-x0,TX,TT,left=0,right=0),color='red',lw=1.4,label=f'fit A={A:.2f} Jy')
    ax.axvline(x0_pred,color='blue',ls='--',lw=1.2,label='600 AU mover in-scan proj.')
    mwin=np.abs(x)<=8
    ylo,yhi=ys[mwin].min(),ys[mwin].max()
    fitA=[q for q in fits if q['scan']==scan]
    ax.set_title(title,fontsize=10); ax.set_xlim(-8,8)
    ax.set_ylim(min(ylo,-0.05)-0.12*(yhi-ylo+0.1), yhi+0.15*(yhi-ylo+0.1))
    ax.legend(fontsize=7,loc='upper right')
    ax.set_xlabel('in-scan (arcmin)',fontsize=8); ax.set_ylabel('Jy',fontsize=8)
fig.suptitle('Fixed-position 60um scan profiles with matched-filter fits (diagnostic view only - NOT the displaced-sky\nexclusion test: the mover at the marked in-scan projection also sits at an unmodeled cross-scan offset from these\ncenterlines; the displaced-sky test is fig2). Markers: JPL Horizons geometry, 600 AU, anchor = coadd center.',
             fontsize=9.5)
plt.tight_layout()
plt.savefig(os.path.join(HERE,'fig1_late_epoch_profiles.png'),dpi=110)
print('markers:',json.dumps(markers))
