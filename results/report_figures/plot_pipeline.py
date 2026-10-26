from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import argparse
PACKAGE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description="Recreate this figure from bundled, offline assets.")
parser.add_argument("--out-dir", type=Path, default=PACKAGE / "reproduced")
args = parser.parse_args()
out = args.out_dir.resolve()
out.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'ps.fonttype':42,'text.color':'#17212b'})
fig=plt.figure(figsize=(6.9,3.2),facecolor='white')
ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,6.9);ax.set_ylim(0,3.2);ax.axis('off')
navy='#216A97';teal='#237A78';edge='#7C8894';gray='#5A6570'
def box(x,y,w,h,text,fill='#F3F6F8',ec=edge,size=10,weight='normal',ls='solid'):
 p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.06',facecolor=fill,edgecolor=ec,linewidth=.85,linestyle=ls)
 ax.add_patch(p);ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=size,fontweight=weight,linespacing=1.2)
 return x,y,w,h
def arrow(a,b,color=gray,dashed=False):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=10,linewidth=.9,color=color,linestyle='--' if dashed else '-'))
A=(.10,1.28);B=(1.65,1.72);C=(3.64,1.28);R=(5.22,1.56)
# Satellite-derived candidates.
ax.text(.10,3.02,'LANDSLIDE ASSESSMENT',ha='left',va='center',color=navy,fontsize=10,fontweight='bold')
box(A[0],2.22,A[1],.59,'Sentinel-2\n+ SRTM',fill='#EDF4F8',ec=navy)
box(B[0],2.22,B[1],.59,'RF / U-Net training\nGNS labels; validation',fill='#EDF4F8',ec=navy,size=9.7)
box(C[0],2.22,C[1],.59,'Frozen RF\nroad overlap',fill='#EDF4F8',ec=navy)
arrow((A[0]+A[1]+.02,2.515),(B[0]-.03,2.515),navy)
arrow((B[0]+B[1]+.02,2.515),(C[0]-.03,2.515),navy)
ax.text(B[0]+B[1]/2,2.04,'U-Net: comparison only',ha='center',va='center',fontsize=9.5,color=gray)
# Terrain-derived width screen.
ax.text(.10,1.88,'WIDTH ASSESSMENT',ha='left',va='center',color=teal,fontsize=10,fontweight='bold')
box(A[0],1.15,A[1],.59,'Historic 1 m DEM\n+ OSM roads',fill='#ECF5F3',ec=teal,size=9.7)
box(B[0],1.15,B[1],.59,'Cross-sections\nNZTA calibration',fill='#ECF5F3',ec=teal)
box(C[0],1.15,C[1],.59,'Vehicle-width\nscreen',fill='#ECF5F3',ec=teal)
arrow((A[0]+A[1]+.02,1.445),(B[0]-.03,1.445),teal)
arrow((B[0]+B[1]+.02,1.445),(C[0]-.03,1.445),teal)
# Common graph join and cost.
box(R[0],1.28,R[1],1.45,'',fill='#F5F6F7',ec='#344553')
ax.text(R[0]+R[1]/2,2.54,'Join by OSM way ID',ha='center',va='center',fontsize=9.5)
ax.text(R[0]+R[1]/2,2.24,'A* road routing',ha='center',va='center',fontsize=10.5,fontweight='bold')
ax.text(R[0]+R[1]/2,1.96,'Drive time + penalties',ha='center',va='center',fontsize=9.5)
ax.text(R[0]+R[1]/2,1.56,'Missing assessment:\nunpenalized',ha='center',va='center',fontsize=9.5,linespacing=1.15)
arrow((C[0]+C[1]+.02,2.515),(R[0]-.03,2.515),navy)
arrow((C[0]+C[1]+.02,1.445),(R[0]-.03,1.445),teal)
box(R[0],.45,R[1],.57,'Route + unknown\ncoverage',fill='#F5F6F7',ec='#344553',size=10)
arrow((R[0]+R[1]/2,1.25),(R[0]+R[1]/2,1.05))
# Optional off-road branch: physically distinct, no claim of validated clearance.
ax.text(.10,.91,'OPTIONAL OFF-ROAD BRANCH',ha='left',va='center',color=gray,fontsize=9.5,fontweight='bold')
box(A[0],.13,A[1],.60,'DEM +\nWorldCover',fill='white',ec=gray,ls='dashed')
box(B[0],.13,B[1],.60,'20 m grid\nShort connecting links',fill='white',ec=gray,size=9.7,ls='dashed')
box(C[0],.13,C[1],.60,'A* with grid links\nCandidate routes\nWidth unvalidated',fill='white',ec=gray,size=9.5,ls='dashed')
arrow((A[0]+A[1]+.02,.43),(B[0]-.03,.43),dashed=True)
arrow((B[0]+B[1]+.02,.43),(C[0]-.03,.43),dashed=True)
arrow((C[0]+C[1]+.02,.43),(R[0]-.03,.64),dashed=True)
fig.savefig(out/'figure1_pipeline.png',dpi=300)
fig.savefig(out/'figure1_pipeline.pdf')
fig.savefig(out/'figure1_pipeline.svg')
print(out/'figure1_pipeline.png')
