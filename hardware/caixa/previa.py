"""Renderiza as malhas reais dos STL sem precisar abrir a interface do FreeCAD."""
import os
import sys
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/tmp/ir-gree-matplotlib')
sys.path.insert(0, '/usr/lib/freecad/lib')
import FreeCAD
import Mesh
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

out = Path(__file__).resolve().parent
fig = plt.figure(figsize=(14, 8), facecolor='#f5f1ed')
ax = fig.add_subplot(111, projection='3d', computed_zorder=False)
ax.set_facecolor('#f5f1ed')
light = np.array([-0.4, -0.6, 1.0])
light /= np.linalg.norm(light)
for filename, offset in [('base.stl', 0), ('tampa.stl', 136)]:
    mesh = Mesh.Mesh(str(out / filename))
    vertices = np.array([[tuple(p) for p in f.Points] for f in mesh.Facets])
    vertices[:, :, 0] += offset
    normals = np.array([tuple(f.Normal) for f in mesh.Facets])
    shade = 0.55 + 0.45 * np.clip(normals @ light, 0, 1)
    colors = shade[:, None] * np.array([0.68, 0.055, 0.19])[None, :]
    camera = np.array([np.cos(np.deg2rad(37))*np.cos(np.deg2rad(-61)),
                       np.cos(np.deg2rad(37))*np.sin(np.deg2rad(-61)), np.sin(np.deg2rad(37))])
    visible = normals @ camera > 0
    ax.add_collection3d(Poly3DCollection(vertices[visible], facecolors=colors[visible],
                                        edgecolors='none', linewidths=0, antialiased=False))
ax.set(xlim=(-5, 261), ylim=(-8, 98), zlim=(0, 65))
ax.set_box_aspect((266, 106, 65))
ax.view_init(elev=37, azim=-61)
ax.set_axis_off()
fig.text(0.07, 0.9, 'IR / GREE', fontsize=30, weight='bold', color='#521329')
fig.text(0.07, 0.85, 'Caixa em PLA carmesim · base + tampa', fontsize=15, color='#6b6063')
fig.text(0.07, 0.10, '120 × 90 × 40,4 mm fechada   /   cantos R9   /   tampa ventilada', fontsize=12, color='#6b6063')
fig.text(0.07, 0.055, 'Prévia das malhas reais. Medidas das peças eletrônicas ainda precisam ser confirmadas.', fontsize=10, color='#6b6063')
plt.subplots_adjust(left=0, right=1, bottom=0.10, top=0.84)
fig.savefig(out / 'previa.png', dpi=160, facecolor=fig.get_facecolor())
