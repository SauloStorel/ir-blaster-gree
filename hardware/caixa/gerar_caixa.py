"""Execute com Python do sistema ou como macro no FreeCAD. Dimensões em mm."""
import sys
from pathlib import Path
import json

sys.path.insert(0, '/usr/lib/freecad/lib')
import FreeCAD as App
import Part
import MeshPart
import Import

OUT = Path(__file__).resolve().parent
# Ajuste estas medidas após medir o conjunto real e execute novamente.
L, W, H = 120.0, 90.0, 38.0
WALL, FLOOR, ROOF, RADIUS = 2.4, 2.4, 2.4, 9.0
CLEARANCE = 0.3  # folga por lado da saia de encaixe
V = App.Vector


def rounded(l, w, h, r, x=0, y=0, z=0):
    box = Part.makeBox(l, w, h, V(x, y, z))
    vertical = [e for e in box.Edges if e.BoundBox.ZLength > h - 0.001]
    return box.makeFillet(r, vertical)


doc = App.newDocument('Caixa_IR_Gree')
params = doc.addObject('Spreadsheet::Sheet', 'Dimensoes')
params.Label = 'Medidas de referência — editar no gerador Python'
for row, (label, value) in enumerate([
    ('Comprimento externo', L), ('Largura externa', W), ('Altura base', H),
    ('Espessura parede', WALL), ('Espessura fundo', FLOOR),
    ('Espessura tampa', ROOF), ('Raio externo', RADIUS),
    ('Folga encaixe por lado', CLEARANCE),
], 1):
    params.set(f'A{row}', label)
    params.set(f'B{row}', str(value) + ' mm')
params.setColumnWidth('A', 290)

base = rounded(L, W, H, RADIUS).cut(
    rounded(L-2*WALL, W-2*WALL, H, RADIUS-WALL, WALL, WALL, FLOOR))
# Torres nos cantos: piloto cego para parafuso autoatarraxante de ~2,9 mm.
centers = [(x, y) for x in (8, L-8) for y in (8, W-8)]
for x, y in centers:
    base = base.fuse(Part.makeCylinder(4.8, H-FLOOR, V(x, y, FLOOR)))
    base = base.cut(Part.makeCylinder(1.2, 13, V(x, y, H-12)))

# Abertura traseira em U: permite acomodar o cabo sem presumir a posição USB.
base = base.cut(Part.makeBox(18, WALL+2, 13, V(L/2-9, W-WALL-1, H-12)))
# Receptor IR e LED ficam expostos; não dependem da transparência do PLA.
base = base.cut(Part.makeBox(18, WALL+2, 12, V(L/2-22, -1, H-11)))
base = base.cut(Part.makeCylinder(2.7, WALL+2, V(L/2+13, -1, H-9), V(0, 1, 0)))
# Passagens para abraçadeiras: fixação flexível de placa/adaptador, sem furação presumida.
for x in (30, L-30):
    for y in (19, W-19):
        base = base.cut(rounded(8, 3, FLOOR+2, 1, x-4, y-1.5, -1))
base = base.removeSplitter()

# A tampa é construída já na orientação de impressão: face externa sobre a mesa.
lid = rounded(L, W, ROOF, RADIUS)
inset = WALL+CLEARANCE
lip = rounded(L-2*inset, W-2*inset, 3, RADIUS-inset, inset, inset, ROOF)
lip = lip.cut(rounded(L-2*(inset+1.5), W-2*(inset+1.5), 4,
                      RADIUS-inset-1.5, inset+1.5, inset+1.5, ROOF))
for x, y in centers:
    lip = lip.cut(Part.makeCylinder(5.2, 5, V(x, y, ROOF-0.1)))
for x, y, width in [(L/2-10, W-6, 20), (L/2-23, -1, 20)]:
    lip = lip.cut(Part.makeBox(width, 7, 5, V(x, y, ROOF-0.1)))
lid = lid.fuse(lip)
for x, y in centers:
    lid = lid.cut(Part.makeCylinder(1.65, 8, V(x, y, -1)))
    lid = lid.cut(Part.makeCone(3.1, 1.65, 1.45, V(x, y, 0)))
# Sete fendas arredondadas criam um desenho discreto e ventilam a eletrônica.
for index, length in enumerate((22, 30, 38, 44, 38, 30, 22)):
    lid = lid.cut(rounded(length, 2.4, ROOF+2, 1.19,
                          (L-length)/2, W/2+(index-3)*6-1.2, -1))
lid = lid.removeSplitter()

checks = {}
for name, shape in [('Base', base), ('Tampa', lid)]:
    assert shape.isValid() and len(shape.Solids) == 1, name
    obj = doc.addObject('PartDesign::Feature', name)
    obj.Shape = shape
    obj.addProperty('App::PropertyString', 'Observacao')
    obj.Observacao = 'Geometria gerada por gerar_caixa.py; ajuste as constantes para regenerar.'
    if App.GuiUp:
        obj.ViewObject.ShapeColor = (0.58, 0.035, 0.14)
        obj.ViewObject.LineColor = (0.22, 0.025, 0.055)
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.08,
                                  AngularDeflection=0.15, Relative=False)
    assert mesh.isSolid(), f'Malha aberta: {name}'
    mesh.write(str(OUT / f'{name.lower()}.stl'))
    checks[name] = {'solido_valido': True, 'malha_fechada': mesh.isSolid(),
                    'triangulos': mesh.CountFacets, 'volume_mm3': round(shape.Volume, 2)}

# Verifica encaixe real na posição fechada, incluindo saia e torres.
assembled = lid.copy()
assembled.rotate(V(0, W/2, 0), V(1, 0, 0), 180)
assembled.translate(V(0, 0, H+ROOF))
checks['interferencia_tampa_mm3'] = base.common(assembled).Volume
assert checks['interferencia_tampa_mm3'] < 0.001
# No documento CAD, exibir tampa afastada para facilitar inspeção.
doc.getObject('Tampa').Placement.Base = V(L+16, 0, 0)
doc.recompute()
Import.export([doc.getObject('Base'), doc.getObject('Tampa')], str(OUT/'caixa_ir_gree.step'))
if App.GuiUp:
    import FreeCADGui as Gui
    Gui.activeDocument().activeView().viewAxonometric()
    Gui.activeDocument().activeView().fitAll()
doc.recompute()
doc.saveAs(str(OUT/'caixa_ir_gree.FCStd'))
(OUT/'validacao.json').write_text(json.dumps(checks, indent=2)+'\n')
print(json.dumps(checks, indent=2))
