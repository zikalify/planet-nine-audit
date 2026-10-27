import numpy as np, re, datetime, os

# parse JPL Earth vectors (heliocentric ecliptic J2000, AU)
E={}
txt=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'horizons.txt')).read()
soe=txt.index('$$SOE'); eoe=txt.index('$$EOE')
for ln in txt[soe:eoe].splitlines():
    m=re.match(r'(\d+\.\d+) = A.D. (\d+)-(\w+)-(\d+)',ln)
    if m: curjd=float(m.group(1)); continue
    m=re.match(r'\s*X =\s*([-\d.E+]+) Y =\s*([-\d.E+]+) Z =\s*([-\d.E+]+)',ln)
    if m: E[curjd]=np.array([float(m.group(1)),float(m.group(2)),float(m.group(3))])
print(f"parsed {len(E)} daily vectors, JD {min(E)}..{max(E)}")

def earth(jd):
    jds=sorted(E)
    if jd<=jds[0]: return E[jds[0]]
    if jd>=jds[-1]: return E[jds[-1]]
    for i in range(len(jds)-1):
        if jds[i]<=jd<=jds[i+1]:
            f=(jd-jds[i])/(jds[i+1]-jds[i])
            return E[jds[i]]*(1-f)+E[jds[i+1]]*f

eps=np.radians(23.4392911)
Rv=np.array([[1,0,0],[0,np.cos(eps),np.sin(eps)],[0,-np.sin(eps),np.cos(eps)]])
ra,dec=np.radians(35.74075),np.radians(-48.5125)
n_eq=np.array([np.cos(dec)*np.cos(ra),np.cos(dec)*np.sin(ra),np.sin(dec)])
east=np.array([-np.sin(ra),np.cos(ra),0.])
north=np.array([-np.sin(dec)*np.cos(ra),-np.sin(dec)*np.sin(ra),np.cos(dec)])

def displ_arcmin(jd,jd0,d_au):
    # REJECTED variant (perp-to-line-of-sight in equatorial frame): misses the queried
    # coordinates by ~1 arcmin. Retained for provenance only - use pos_eq (full_eq).
    dE=earth(jd)-earth(jd0)
    perp=dE-np.dot(dE,n_eq)*n_eq
    off=-perp/d_au  # radians, geocentric apparent offset relative to anchor
    dra=np.dot(off,east)/np.cos(dec); ddec=np.dot(off,north)
    return np.degrees(dra)*60, np.degrees(ddec)*60  # arcmin

def jd_of(y,mo,d,ut=0.0):
    dt=datetime.datetime(y,mo,d)+datetime.timedelta(hours=ut)
    return dt.toordinal()+1721424.5-1+ (dt.hour/24+dt.minute/1440)  # proleptic JD approx
# use standard JD calc
def jd2(y,mo,d,ut=0.0):
    if mo<=2: y-=1; mo+=12
    A=y//100; B=2-A+A//4
    return int(365.25*(y+4716))+int(30.6001*(mo+1))+d+B-1524.5+ut/24.

RA0,DEC0=35.74075,-48.5125
def pos(jd,jd0,d_au):
    dra,ddec=displ_arcmin(jd,jd0,d_au)
    return RA0+dra/60, DEC0+ddec/60

# validation against the 7 known points

def pos_eq(jd,jd0,d):
    dE=earth(jd)-earth(jd0)
    off=-np.linalg.inv(Rv)@dE/d
    dra=np.degrees(np.dot(off,east)/np.cos(dec)); ddec=np.degrees(np.dot(off,north))
    return np.array([RA0+dra, DEC0+ddec])

def sky_sep(p,q):
    return np.hypot((p[0]-q[0])*60*np.cos(np.radians((p[1]+q[1])/2)),(p[1]-q[1])*60)

if __name__=='__main__':
    JD_ANCHOR_JUN26=jd2(1983,6,26,16.38)
    JD_ANCHOR_JUL20=jd2(1983,7,20,0.0)
    JD_SEP1=jd2(1983,9,1,0.0)
    JD_AUG28=jd2(1983,8,28,0.0)
    known={
     ('sep1_p1',500,JD_ANCHOR_JUN26,JD_SEP1):(35.7448,-48.6207),
     ('sep1_p2',500,JD_ANCHOR_JUL20,JD_SEP1):(35.7205,-48.5863),
     ('sep1_p3',700,JD_ANCHOR_JUN26,JD_SEP1):(35.7436,-48.5898),
     ('sep1_p4',700,JD_ANCHOR_JUL20,JD_SEP1):(35.7263,-48.5652),
     ('aug28_q1',500,JD_ANCHOR_JUN26,JD_AUG28):(35.7502,-48.6141),
     ('aug28_q2',500,JD_ANCHOR_JUL20,JD_AUG28):(35.7259,-48.5796),
     ('aug28_q3',700,JD_ANCHOR_JUL20,JD_AUG28):(35.7301,-48.5605),
    }
    print("\nvalidation (computed vs known, validated full_eq variant pos_eq):")
    for (name,d,jd0,jd),(ra_k,dec_k) in known.items():
        p=pos_eq(jd,jd0,d); ra_c,dec_c=float(p[0]),float(p[1])
        err=np.hypot((ra_c-ra_k)*60*np.cos(dec),(dec_c-dec_k)*60)
        print(f"  {name}: ({ra_c:.4f},{dec_c:.4f}) vs ({ra_k},{dec_k})  err={err:.3f}'")

    print("\n=== variant tests ===")
    n_ec=Rv@n_eq  # ecliptic unit vector to source
    def variant(jd,jd0,d,mode):
        dE=earth(jd)-earth(jd0)
        if mode=='perp_ecl_eqproj':
            # perp in ecliptic, then rotate to equatorial for RA/Dec
            perp=dE-np.dot(dE,n_ec)*n_ec
            off=-np.linalg.inv(Rv)@perp/d
            return np.degrees(np.dot(off,east)/np.cos(dec))*60, np.degrees(np.dot(off,north))*60
        if mode=='full_eq':
            off=-np.linalg.inv(Rv)@dE/d
            return np.degrees(np.dot(off,east)/np.cos(dec))*60, np.degrees(np.dot(off,north))*60
        if mode=='full_ecl_perp_eq':
            perp=dE-np.dot(dE,n_ec)*n_ec
            off=-perp/d  # stayed in ecliptic, WRONGLY dotted with eq basis
            return np.degrees(np.dot(off,east)/np.cos(dec))*60, np.degrees(np.dot(off,north))*60
    for mode in ['perp_ecl_eqproj','full_eq','full_ecl_perp_eq']:
        errs=[]
        for (name,d,jd0,jd),(ra_k,dec_k) in known.items():
            dra,ddec=variant(jd,jd0,d,mode)
            ra_c=RA0+dra/60; dec_c=DEC0+ddec/60
            errs.append(np.hypot((ra_c-ra_k)*60*np.cos(dec),(dec_c-dec_k)*60))
        print(f"  {mode}: max err {max(errs):.3f}'  mean {np.mean(errs):.3f}'")

    print("\n=== coverage geometry (corrected) ===")
    JD_MID=jd2(1983,7,3,8.0)   # midpoint of anchors Jun26 16:22 .. Jul20 00:00
    for ep_name,jd_ep in [('Sep1',JD_SEP1),('Aug28',JD_AUG28)]:
        corners={}
        for d in [500,700]:
            for an_name,jd0 in [('Jun26',JD_ANCHOR_JUN26),('Jul20',JD_ANCHOR_JUL20)]:
                corners[(d,an_name)]=pos_eq(jd_ep,jd0,d)
        mid=pos_eq(jd_ep,JD_MID,600)
        print(f"\n{ep_name}: corners:")
        for k,v in corners.items(): print(f"   d={k[0]} anchor={k[1]}: {v[0]:.4f} {v[1]:.4f}")
        print(f"   MID d=600 anchor~Jul3: {mid[0]:.4f} {mid[1]:.4f}")
        # dense grid over rectangle, max distance to nearest covered point (corners+mid)
        # parameterize: d in [500,700], anchor epoch in [Jun26 16:22, Jul20 00:00]
        cover_pts=list(corners.values())+[mid]
        worst=0; worst_at=None
        for d in np.linspace(500,700,21):
            for f in np.linspace(0,1,21):
                jd0=JD_ANCHOR_JUN26+f*(JD_ANCHOR_JUL20-JD_ANCHOR_JUN26)
                p=pos_eq(jd_ep,jd0,d)
                dm=min(sky_sep(p,c) for c in cover_pts)
                if dm>worst: worst=dm; worst_at=(d,f)
        print(f"   with corners+center: worst uncovered distance = {worst:.2f}' (at d={worst_at[0]:.0f}, anchor-frac={worst_at[1]:.2f})")
        # corners only
        worst2=0
        for d in np.linspace(500,700,21):
            for f in np.linspace(0,1,21):
                jd0=JD_ANCHOR_JUN26+f*(JD_ANCHOR_JUL20-JD_ANCHOR_JUN26)
                p=pos_eq(jd_ep,jd0,d)
                dm=min(sky_sep(p,c) for c in corners.values())
                if dm>worst2: worst2=dm
        print(f"   corners only:        worst uncovered distance = {worst2:.2f}'")
        # also add d=600 anchor endpoints?
        extra=[pos_eq(jd_ep,JD_ANCHOR_JUN26,600),pos_eq(jd_ep,JD_ANCHOR_JUL20,600)]
        cover2=list(corners.values())+extra
        worst3=0
        for d in np.linspace(500,700,41):
            for f in np.linspace(0,1,41):
                jd0=JD_ANCHOR_JUN26+f*(JD_ANCHOR_JUL20-JD_ANCHOR_JUN26)
                p=pos_eq(jd_ep,jd0,d)
                dm=min(sky_sep(p,c) for c in cover2)
                if dm>worst3: worst3=dm
        print(f"   corners+d600-edges:  worst uncovered distance = {worst3:.2f}'  (d600/Jun26={extra[0][0]:.4f},{extra[0][1]:.4f}  d600/Jul20={extra[1][0]:.4f},{extra[1][1]:.4f})")
