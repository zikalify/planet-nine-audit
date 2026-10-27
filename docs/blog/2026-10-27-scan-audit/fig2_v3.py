import numpy as np, json, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from p9paths import WORK, HERE

all_tight=json.load(open(os.path.join(WORK,'all_tight.json')))
sens=json.load(open(os.path.join(WORK,'sensitivity.json')))['null']
# map crossing scan -> sensitivity MAD
order=['b3_428_025_13','b3_428_025_32','b3_436_028_14','b3_436_028_33','b3_436_031_15','b3_436_031_34','b3_436_031_38']
labels=['Aug28\ndet13','Aug28\ndet32','Sep1\ndet14','Sep1\ndet33','Sep1\ndet15','Sep1\ndet34','Sep1\ndet38']
fig,ax=plt.subplots(figsize=(11,6.2))
ax.axhspan(0.19,0.30,color='red',alpha=0.12,label='required mover flux if it carried the full\nmeasured Jun/Jul 60um flux (0.19-0.30 Jy)')
for i,(scan,lab) in enumerate(zip(order,labels)):
    mad=sens[scan]['mad']
    ax.fill_between([i-0.42,i+0.42],-2*mad,2*mad,color='gray',alpha=0.18,
                    label='confusion/noise null band (±2xMAD field null; descriptive, not a 95% limit)' if i==0 else None)
    rows=[r for r in all_tight if r['scan']==scan]
    A=np.array([r['A'] for r in rows])
    ax.scatter(np.full(len(A),i)+np.linspace(-0.32,0.32,len(A)),A,s=22,color='steelblue',alpha=0.8,
               label='amplitude at each of 10 grid positions' if i==0 else None)
    ax.axhline(np.median(A),xmin=(i-0.42)/7+0.5/7*0,xmax=0,color='navy',lw=0)  # noop
    ax.plot([i-0.42,i+0.42],[np.median(A)]*2,color='navy',lw=1.5,
            label='crossing median' if i==0 else None)
ax.axhline(0,color='k',lw=0.7)
ax.set_xticks(range(7)); ax.set_xticklabels(labels,fontsize=9)
ax.set_ylabel('matched-filter amplitude (Jy)')
ax.set_title('60um amplitudes at the 10 tested mover positions, grouped by the 7 DISTINCT crossings\n(crossings not independent: common-mode sky; null band = +/-2xMAD, descriptive, not a 95% limit)\nmeasured p95 null amplitudes 0.16-0.34 Jy overlap the required 0.19-0.30 Jy -> test inconclusive at the required flux',fontsize=10)
ax.legend(loc='lower right',fontsize=8)
ax.set_ylim(-0.55,0.75)
plt.tight_layout()
plt.savefig(os.path.join(HERE,'fig2_displaced_position_nulls.png'),dpi=110)
print('fig2 v3 saved')
