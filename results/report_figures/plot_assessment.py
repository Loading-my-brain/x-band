from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import argparse
PACKAGE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description="Recreate this figure from bundled, offline assets.")
parser.add_argument("--out-dir", type=Path, default=PACKAGE / "reproduced")
args = parser.parse_args()
out = args.out_dir.resolve()
out.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.5,'axes.titlesize':10.5,'axes.labelsize':9.5,'xtick.labelsize':9.5,'ytick.labelsize':9.5,'legend.fontsize':9.5,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#6b7280','axes.linewidth':.6,'xtick.color':'#303740','ytick.color':'#303740','text.color':'#17212b','axes.labelcolor':'#17212b'})
fig=plt.figure(figsize=(6.9,3.0),facecolor='white')
a=fig.add_axes([.075,.24,.395,.49]);b=fig.add_axes([.585,.24,.395,.49])
colors=['#216A97','#CA7523'];barw=.34
x=np.arange(4)
data=json.loads((PACKAGE/'assessment_metrics.json').read_text())
unet=[data['landslide_reference_agreement']['U-Net'][k] for k in ['precision','recall','f1','iou']]
rf=[data['landslide_reference_agreement']['Random Forest'][k] for k in ['precision','recall','f1','iou']]
a.bar(x-barw/2,unet,barw,color=colors[0],label='U-Net',zorder=3)
a.bar(x+barw/2,rf,barw,color=colors[1],label='Random Forest',zorder=3)
a.set_xticks(x,['Precision','Recall','F1','IoU']);a.set_ylim(0,.65);a.set_ylabel('Pixel agreement score');a.set_xlim(-.55,3.55)
a.yaxis.set_major_locator(MultipleLocator(.2));a.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
a.legend(loc='lower left',bbox_to_anchor=(-.03,1.005),frameon=False,ncol=2,handlelength=1.0,columnspacing=.9,handletextpad=.4,borderaxespad=0)
meta=data['accuracy_width_vs_nzta']
old=meta[0];cal=meta[1]
x=np.arange(3)
vals1=[old[k] for k in ['mae_m','rmse_m','bias_m']]
vals2=[cal[k] for k in ['mae_m','rmse_m','bias_m']]
b1=b.bar(x-barw/2,vals1,barw,color=colors[0],label='Slope only',zorder=3)
b2=b.bar(x+barw/2,vals2,barw,color=colors[1],label='Calibrated',zorder=3)
b.set_xticks(x,['MAE','RMSE','Bias']);b.set_ylim(0,6.75);b.set_ylabel('Width error (m)');b.set_xlim(-.55,2.55);b.yaxis.set_major_locator(MultipleLocator(2))
b.legend(loc='lower left',bbox_to_anchor=(-.03,1.005),frameon=False,ncol=2,handlelength=1.0,columnspacing=.9,handletextpad=.4,borderaxespad=0)
for bars in [b1,b2]:
 for bar in bars:
  b.text(bar.get_x()+bar.get_width()/2,bar.get_height()+.14,f'{bar.get_height():.2f}',ha='center',va='bottom',fontsize=9.5)
for ax in [a,b]:
 ax.grid(axis='y',color='#D9DEE4',linewidth=.6,zorder=0)
 ax.tick_params(axis='x',length=0,pad=6)
 ax.tick_params(axis='y',length=3,pad=3)
fig.text(.075,.95,'(a) Landslide reference agreement',ha='left',va='top',weight='bold',fontsize=10.5)
fig.text(.585,.95,'(b) Carriageway width validation',ha='left',va='top',weight='bold',fontsize=10.5)
fig.text(.075,.10,'Road-selected pixels; not an independent test.',ha='left',va='center',fontsize=9.5)
fig.text(.585,.10,'n = 36 vs 41; different validation samples.',ha='left',va='center',fontsize=9.5)
fig.savefig(out/'figure2_assessment.png',dpi=300)
fig.savefig(out/'figure2_assessment.pdf')
fig.savefig(out/'figure2_assessment.svg')
print(out/'figure2_assessment.png')
