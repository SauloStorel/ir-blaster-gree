"""Prévias das malhas STL reais, com renderização independente da GPU do FreeCAD."""
import os,sys,json
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/ir-gree-matplotlib')
sys.path.insert(0,'/usr/lib/freecad/lib')
import FreeCAD,Mesh
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
out=Path(__file__).resolve().parent
L,W,H=json.loads((out/'validacao.json').read_text())['dimensoes_externas_mm']
for filename,azimuth,label,parts,elev in [
 ('previa.png',-45,'Sensores + micro-USB na lateral direita',('base','tampa'),30),
 ('previa_traseira.png',45,'Ventilação traseira',('base','tampa'),30),
 ('previa_apoio.png',-45,'Berço interno do ESP32 · quatro apoios e guias',('base',),55)]:
 fig=plt.figure(figsize=(12,8),facecolor='#f7f4f0')
 ax=fig.add_subplot(111,projection='3d')
 ax.set_facecolor('#f7f4f0')
 camera=np.array([np.cos(np.deg2rad(elev))*np.cos(np.deg2rad(azimuth)),np.cos(np.deg2rad(elev))*np.sin(np.deg2rad(azimuth)),np.sin(np.deg2rad(elev))])
 light=np.array([-.5,-.5,1]);light=light/np.linalg.norm(light)
 for name in parts:
  mesh=Mesh.Mesh(str(out/(name+'.stl')))
  vertices=np.array([[tuple(p) for p in f.Points] for f in mesh.Facets])
  normals=np.array([tuple(f.Normal) for f in mesh.Facets])
  if name=='tampa':
   vertices[:,:,1]=W-vertices[:,:,1];vertices[:,:,2]=H-vertices[:,:,2]
   normals[:,1:]*=-1
  visible=normals@camera>0
  shade=.62+.38*np.clip(normals@light,0,1)
  colors=shade[:,None]*np.array([.68,.055,.19])[None,:]
  ax.add_collection3d(Poly3DCollection(vertices[visible],facecolors=colors[visible],edgecolors='none',linewidths=0,antialiased=False))
 zmax=H+9 if len(parts)>1 else 16
 ax.set(xlim=(-5,L+5),ylim=(-5,W+5),zlim=(0,zmax))
 ax.set_box_aspect((L+10,W+10,zmax))
 ax.view_init(elev=elev,azim=azimuth)
 ax.set_axis_off()
 fig.text(.07,.90,'IR / GREE',fontsize=25,weight='bold',color='#521329')
 fig.text(.07,.845,label+(' · topo liso' if len(parts)>1 else ''),fontsize=14,color='#6b6063')
 measures=' × '.join(f'{n:g}'.replace('.',',') for n in (L,W,H))
 fig.text(.07,.08,measures+' mm · PLA carmesim · prévia das malhas reais',fontsize=12,color='#6b6063')
 plt.subplots_adjust(left=0,right=1,bottom=.10,top=.85)
 fig.savefig(out/filename,dpi=140,facecolor=fig.get_facecolor())
 plt.close(fig)
