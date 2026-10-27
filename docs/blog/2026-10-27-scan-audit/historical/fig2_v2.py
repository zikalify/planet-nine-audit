import sys; sys.path.insert(0,'/tmp/p9work')
import numpy as np, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

all_tight=json.load(open('/tmp/p9work/all_tight.json'))
order=['sep1_p1','sep1_p2','sep1_p3','sep1_p4','sep1_c','aug28_q1','aug28_q2','aug28_q3','aug28_c','aug28_q4']
labels=['Sep1\nd500/A','Sep1\nd500/B','Sep1\nd700/A','Sep1\nd700/B','Sep1\nd600/mid','Aug28\nd500/A','Aug28\nd500/B','Aug28\nd700/B','Aug28\nd600/mid','Aug28\nd700/A']
fig,ax=plt.subplots(figsize=(11,6.1))
ax.axhspan(0.19,0.30,color='red',alpha=0.15,label='mover-required 60um flux (Jun/Jul measured range)')
for i,(p,lab) in enumerate(zip(order,labels)):
    rows=[r for r in all_tight if r['point']==p]
    A=np.array([r['A'] for r in rows])
    ax.scatter(np.full(len(A),i)+np.linspace(-0.18,0.18,len(A)),A,s=18,color='steelblue',alpha=0.75)
    m=A.mean(); s=A.std(ddof=1)/np.sqrt(len(A))
    ax.errorbar([i],[m],yerr=[s],fmt='ks',capsize=4,markersize=7,label='mean±sem' if i==0 else None)
ax.axhline(0,color='gray',lw=0.8)
ax.set_xticks(range(len(order))); ax.set_xticklabels(labels,fontsize=8)
ax.set_ylabel('matched-filter amplitude (Jy)')
ax.set_title('60um amplitude at predicted 500-700 AU mover positions (10-point grid, 51 tight-crossing measurements)')
ax.legend(loc='lower right',fontsize=8)
plt.tight_layout()
plt.savefig('/downloads/scanpi_profiles/analysis/fig2_displaced_position_nulls.png',dpi=110)
print("fig2 updated")
