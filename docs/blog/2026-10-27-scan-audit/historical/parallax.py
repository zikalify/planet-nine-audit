import numpy as np, glob, re

# --- accurate-enough solar position (low-precision formula, ~0.01 deg) ---
def sun_ecl_lon(y,m,d,ut):
    # Julian day
    if m<=2: y-=1; m+=12
    A=y//100; B=2-A+A//4
    JD=int(365.25*(y+4716))+int(30.6001*(m+1))+d+B-1524.5+ut/24.
    T=(JD-2451545.0)/36525.
    L0=(280.46646+36000.76983*T)%360
    M=357.52911+35999.05029*T
    Mr=np.radians(M)
    C=(1.914602-0.004817*T)*np.sin(Mr)+0.019993*np.sin(2*Mr)+0.000289*np.sin(3*Mr)
    return np.radians((L0+C)%360)

# object: ecliptic (lon,lat) of 35.74075,-48.5125 J2000 equatorial -> ecliptic
eps=np.radians(23.4392911)
ra,dec=np.radians(35.74075),np.radians(-48.5125)
x0v=np.array([np.cos(dec)*np.cos(ra),np.cos(dec)*np.sin(ra),np.sin(dec)])
# rotate about x by -eps to go equatorial->ecliptic
R=np.array([[1,0,0],[0,np.cos(eps),np.sin(eps)],[0,-np.sin(eps),np.cos(eps)]])
e=R@x0v
lam,beta=np.arctan2(e[1],e[0]),np.arcsin(e[2])
print(f"object ecliptic: lon={np.degrees(lam):.3f} lat={np.degrees(beta):.3f}")

def apparent(y,m,d,ut,dist_au):
    ls=sun_ecl_lon(y,m,d,ut)
    earth=np.array([np.cos(ls+np.pi),np.sin(ls+np.pi),0.0])  # earth opposite sun, r=1 AU
    obj=dist_au*np.array([np.cos(beta)*np.cos(lam),np.cos(beta)*np.sin(lam),np.sin(beta)])
    v=obj-earth; v/=np.linalg.norm(v)
    return v  # apparent unit vector in ecliptic frame

def to_eq(v):
    return np.linalg.inv(R)@v

epochs={'Jun26':(1983,6,26,16.38),'Jul09':(1983,7,9,22.13),'Jul10':(1983,7,10,1.57),'Aug22':(1983,8,22,5.48),'Aug28':(1983,8,28,0.58),'Sep01':(1983,9,1,0.74)}
ref=apparent(*epochs['Jun26'],600)
for dist in [500,600,700]:
    print(f"--- d={dist} AU: apparent displacement rel Jun26 (arcmin, equatorial dRA*cos/dDec) ---")
    vref=to_eq(apparent(*epochs['Jun26'],dist))
    raref=np.arctan2(vref[1],vref[0]); decref=np.arcsin(vref[2])
    for k,e_ in epochs.items():
        v=to_eq(apparent(*e_,dist))
        ra2=np.arctan2(v[1],v[0]); dec2=np.arcsin(v[2])
        dE=np.degrees((ra2-raref+np.pi)%(2*np.pi)-np.pi)*np.cos(decref)*60
        dN=np.degrees(dec2-decref)*60
        print(f"  {k}: dE={dE:+6.2f} dN={dN:+6.2f}  total={np.hypot(dE,dN):5.2f}")
