"""Desenha a seção CAD real do fundo, sem artefatos de renderização 3D."""
import os,sys
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/ir-gree-matplotlib')
sys.path.insert(0,'/usr/lib/freecad/lib')
import FreeCAD as A
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
p=Path(__file__).resolve().parent
doc=A.openDocument(str(p/'caixa_ir_gree_mini.FCStd'))
base=doc.getObject('Base').Shape
wires=sorted(base.slice(A.Vector(0,0,1),.1),key=lambda w:w.BoundBox.XLength*w.BoundBox.YLength,reverse=True)
assert len(wires)==1
fig,ax=plt.subplots(figsize=(10,7),facecolor='#f7f4f0')
ax.set_facecolor('#f7f4f0')
for i,wire in enumerate(wires):
 points=wire.discretize(Deflection=.02)
 ax.add_patch(Polygon([(v.x,v.y) for v in points],closed=True,facecolor='#a80d30' if i==0 else '#f7f4f0',edgecolor='#69132c',linewidth=1.2))
ax.set(xlim=(-5,base.BoundBox.XMax+5),ylim=(-6,base.BoundBox.YMax+6),aspect='equal')
ax.axis('off')
fig.text(.10,.91,'Fundo totalmente fechado · caixa de encaixe',fontsize=18,weight='bold',color='#521329')
fig.text(.10,.075,'Seção real do CAD · sem furos de parafusos, abraçadeiras ou pés',fontsize=11,color='#6b6063')
fig.savefig(p/'previa_fundo.png',dpi=150,facecolor=fig.get_facecolor())
