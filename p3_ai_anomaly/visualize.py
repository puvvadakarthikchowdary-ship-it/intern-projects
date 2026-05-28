import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('results.csv')
normal  = df[df['predicted'] == 0]
anomaly = df[df['predicted'] == 1]

fig, axes = plt.subplots(2, 2, figsize=(13, 8))
fig.patch.set_facecolor('#0a0a0f')
fig.suptitle('CPU Performance Anomaly Detection', color='white', fontsize=15)

for ax in axes.flat:
    ax.set_facecolor('#111118')
    ax.tick_params(colors='#888')
    for sp in ax.spines.values():
        sp.set_color('#2a2a3a')

ax = axes[0,0]
ax.plot(df.index, df['anomaly_score'], color='#534AB7', lw=0.7, alpha=0.8)
ax.scatter(anomaly.index, anomaly['anomaly_score'], color='#f97316', s=20, zorder=5, label='Anomaly')
thresh = df[df['predicted']==1]['anomaly_score'].min()
ax.axhline(thresh, color='#f59e0b', linestyle='--', lw=1, label='Threshold')
ax.set_title('Anomaly Score Timeline', color='white')
ax.set_xlabel('Sample index', color='#888')
ax.set_ylabel('Score', color='#888')
ax.legend(facecolor='#1a1a24', labelcolor='white', fontsize=9)

ax = axes[0,1]
ax.scatter(normal['ipc'], normal['l2_miss_rate'], c='#14b8a6', s=8, alpha=0.4, label='Normal')
ax.scatter(anomaly['ipc'], anomaly['l2_miss_rate'], c='#f97316', s=25, alpha=0.9, label='Anomaly', zorder=5)
ax.set_title('IPC vs L2 Miss Rate', color='white')
ax.set_xlabel('IPC', color='#888')
ax.set_ylabel('L2 Miss Rate', color='#888')
ax.legend(facecolor='#1a1a24', labelcolor='white', fontsize=9)

ax = axes[1,0]
ax.scatter(normal['branch_miss'], normal['ipc'], c='#8b5cf6', s=8, alpha=0.4, label='Normal')
ax.scatter(anomaly['branch_miss'], anomaly['ipc'], c='#f97316', s=25, alpha=0.9, label='Anomaly')
ax.set_title('Branch Miss vs IPC', color='white')
ax.set_xlabel('Branch Miss Rate', color='#888')
ax.set_ylabel('IPC', color='#888')
ax.legend(facecolor='#1a1a24', labelcolor='white', fontsize=9)

ax = axes[1,1]
true_an  = df[df['label']==1]
detected = df[(df['predicted']==1) & (df['label']==1)]
cats = ['Total anomalies', 'Detected', 'Missed']
vals = [len(true_an), len(detected), len(true_an)-len(detected)]
clrs = ['#8b5cf6', '#14b8a6', '#f97316']
bars = ax.bar(cats, vals, color=clrs, edgecolor='none', width=0.5)
ax.set_title('Detection Summary', color='white')
ax.tick_params(colors='#888')
for bar, v in zip(bars, vals):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            str(v), ha='center', color='white', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('anomaly_detection.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0f')
print("Chart saved: anomaly_detection.png")
