from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.patches import Rectangle
import geopandas as gpd

import argparse
PACKAGE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description="Recreate this figure from bundled, offline assets.")
parser.add_argument("--out-dir", type=Path, default=PACKAGE / "reproduced")
args = parser.parse_args()
out = args.out_dir.resolve()
out.mkdir(parents=True, exist_ok=True)
SOURCE = PACKAGE
OUT = out
base = gpd.read_file(SOURCE / 'route_baseline.geojson').to_crs(2193)
route = gpd.read_file(SOURCE / 'route_pinzgauer.geojson').to_crs(2193)
heavy = gpd.read_file(SOURCE / 'route_mhov.geojson').to_crs(2193)
assert len(route) == len(heavy) and all(a.equals_exact(b, 0.01) for a,b in zip(route.geometry,heavy.geometry))
assert (route.status_pinzgauer.values == heavy.status_mhov.values).all()
colors = {'unverified':'#D17A00','yes':'#006D77','unknown':'#AD3647'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.5,'axes.labelsize':9,
                     'axes.titlesize':10.5,'xtick.labelsize':8,'ytick.labelsize':8,
                     'pdf.fonttype':42,'ps.fonttype':42})
fig = plt.figure(figsize=(6.9,4.4),facecolor='white')
gs = fig.add_gridspec(1,2,left=.09,right=.985,bottom=.25,top=.91,wspace=.26,width_ratios=[1.42,1])
axes = [fig.add_subplot(gs[0,i]) for i in range(2)]
start=route.geometry.iloc[0].coords[0]
end=route.geometry.iloc[-1].coords[-1]
zoom=(1647200,1657600,5304000,5311700)

def furniture(ax,scale,scale_x=.07):
    xmin,xmax=ax.get_xlim();ymin,ymax=ax.get_ylim();w=xmax-xmin;h=ymax-ymin
    x0=xmin+scale_x*w;y0=ymin+.08*h
    ax.plot([x0,x0+scale],[y0,y0],color='#1B2830',lw=2.0,zorder=10)
    for x in [x0,x0+scale]:ax.plot([x,x],[y0-.012*h,y0+.012*h],color='#1B2830',lw=1,zorder=10)
    ax.text(x0+scale/2,y0+.025*h,f'{scale/1000:g} km',ha='center',va='bottom',fontsize=8.5,zorder=10,
            bbox={'facecolor':'white','edgecolor':'none','pad':.5,'alpha':.9})
    ax.annotate('N',xy=(.92,.82),xytext=(.92,.95),xycoords='axes fraction',ha='center',va='center',
                fontsize=9,fontweight='bold',arrowprops={'arrowstyle':'<-','lw':1.2,'color':'#1B2830'})

for i,ax in enumerate(axes):
    ax.set_facecolor('#FBFCFC')
    base.plot(ax=ax,color='#737D85',lw=1.8 if i else 1.5,linestyle=(0,(3,2)),zorder=2)
    # Saved graph-edge status, not an assertion of full measurement coverage or road safety.
    for status in ['unverified','yes','unknown']:
        part=route[route.status_pinzgauer==status]
        part.plot(ax=ax,color='white',lw=3.5 if i else 3.0,zorder=3)
        part.plot(ax=ax,color=colors[status],lw=2.2 if i else 1.9,zorder=4)
    ax.set_aspect('equal')
    ax.set_anchor('N')
    ax.grid(color='#DDE3E6',lw=.45,zorder=0)
    for s in ax.spines.values():s.set_color('#BFC8CE');s.set_linewidth(.6)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v/1000:.0f}'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v/1000:.0f}'))
    ax.xaxis.set_major_locator(MaxNLocator(4));ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.set_xlabel('Easting (km)');ax.set_ylabel('Northing (km)' if not i else '')
    ax.tick_params(length=2.5,width=.5,pad=2)

axes[0].set_xlim(1581000,1662500);axes[0].set_ylim(5260000,5320500)
axes[1].set_xlim(zoom[0],zoom[1]);axes[1].set_ylim(zoom[2],zoom[3])
axes[0].set_title('(a) Culverden to Kaikōura',loc='left',pad=9,fontweight='bold')
axes[1].set_title('(b) Kaikōura approach',loc='left',pad=9,fontweight='bold')
for ax in axes:
    ax.scatter([end[0]],[end[1]],s=29,facecolor='white',edgecolor='#172D39',lw=1.3,zorder=7)
axes[0].scatter([start[0]],[start[1]],s=27,facecolor='#172D39',edgecolor='white',lw=.7,zorder=7)
axes[0].annotate('Culverden',start,xytext=(0,10),textcoords='offset points',ha='left',fontsize=9,zorder=10)
axes[0].annotate('Kaikōura',end,xytext=(-4,10),textcoords='offset points',ha='right',fontsize=9,zorder=10,
                 bbox={'facecolor':'white','edgecolor':'none','pad':1,'alpha':.9})
axes[1].annotate('Kaikōura',end,xytext=(-5,-15),textcoords='offset points',ha='right',fontsize=9,zorder=10)
axes[0].add_patch(Rectangle((zoom[0],zoom[2]),zoom[1]-zoom[0],zoom[3]-zoom[2],fill=False,
                           ec='#5B6570',lw=.8,ls=(0,(3,2)),zorder=5))
axes[0].text(zoom[0]-700,zoom[3]+600,'b',ha='right',va='bottom',fontsize=9,fontweight='bold')
furniture(axes[0],20000,scale_x=.58);furniture(axes[1],2000)

handles=[Line2D([0],[0],color=colors['unverified'],lw=2.2,label='Unverified edge'),
         Line2D([0],[0],color=colors['yes'],lw=2.2,label='Assessed: no flag'),
         Line2D([0],[0],color=colors['unknown'],lw=2.2,label='Unknown width'),
         Line2D([0],[0],color='#737D85',lw=1.5,ls=(0,(3,2)),label='Fastest, without checks')]
fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.53,.105),frameon=False,
           ncol=2,columnspacing=1.4,handlelength=2.4,fontsize=9.1)
fig.text(.09,.055,'Selected route is identical for both vehicles. Status follows the saved graph edges.',fontsize=8.7,color='#374955')
fig.text(.09,.012,'NZTM2000 / EPSG:2193 · Data: X-Band saved routing output; © OpenStreetMap contributors',fontsize=7.9,color='#5A6670')
fig.savefig(OUT/'Figure3_integrated_route.png',dpi=300)
fig.savefig(OUT/'Figure3_integrated_route.pdf')
fig.savefig(OUT/'Figure3_integrated_route.svg')
print(OUT/'Figure3_integrated_route.png')
