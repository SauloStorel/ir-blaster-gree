"""Caixa compacta para ESP32 de 52 × 29 mm. Dimensões em milímetros."""
import sys, json
from pathlib import Path
sys.path.insert(0, '/usr/lib/freecad/lib')
import FreeCAD as App
import Part, MeshPart, Import
V=App.Vector
OUT=Path(__file__).resolve().parent
L,W,H=82.,58.,30.4
T=2.4
R=9.
SEAM=8.
GAP=.3

def rr(l,w,h,r,x=0,y=0,z=0):
    b=Part.makeBox(l,w,h,V(x,y,z))
    return b.makeFillet(r,[e for e in b.Edges if e.BoundBox.ZLength>h-.001])

def edge_round(s,z,r):
    return s.makeFillet(r,[e for e in s.Edges if abs(e.BoundBox.ZMin-z)<1e-5 and abs(e.BoundBox.ZMax-z)<1e-5])

# Todos os sólidos são construídos primeiro na posição de montagem.
outer=edge_round(rr(L,W,H-SEAM,R,z=SEAM),H,2.)
shell=outer.cut(rr(L-2*T,W-2*T,H-T+1,R-T,T,T,-1))
tray=edge_round(rr(L,W,SEAM-.35,R),0,1.2)
tray=tray.cut(rr(L-2*T,W-2*T,H,R-T,T,T,T))
# Saia inferior encaixada por dentro da carcaça: vão visual de 0,35 mm.
inset=T+GAP
lip=rr(L-2*inset,W-2*inset,3.35,R-inset,inset,inset,SEAM-.35)
lip=lip.cut(rr(L-2*(inset+1.6),W-2*(inset+1.6),5,R-inset-1.6,inset+1.6,inset+1.6,SEAM-1))
shoulder=rr(L-3.8,W-3.8,2.1,R-1.9,1.9,1.9,SEAM-2.35)
shoulder=shoulder.cut(rr(L-2*(inset+1.6),W-2*(inset+1.6),3,R-inset-1.6,inset+1.6,inset+1.6,SEAM-2.5))
lip=lip.fuse(shoulder)
centers=[(x,y) for x in (9,L-9) for y in (9,W-9)]
for x,y in centers:
    lip=lip.cut(Part.makeCylinder(5.4,7,V(x,y,SEAM-3)))
tray=tray.fuse(lip)
# Parafusos entram pelo fundo e prendem torres integradas na carcaça superior.
for x,y in centers:
    shell=shell.fuse(Part.makeCylinder(4.8,H-T-(T+.3),V(x,y,T+.3)))
    shell=shell.cut(Part.makeCylinder(1.2,12,V(x,y,T+.3)))
    tray=tray.cut(Part.makeCylinder(1.65,T+2,V(x,y,-1)))
    tray=tray.cut(Part.makeCone(3.1,1.65,1.45,V(x,y,0)))
# Cabo na traseira, acessível quando a bandeja é removida.
shell=shell.cut(rr(16,9,12,2,L/2-8,W-5,SEAM-1))
lip_cut=Part.makeBox(18,7,6,V(L/2-9,W-6,SEAM-1))
tray=tray.cut(lip_cut)
# Frente: nicho raso alongado agrupa as duas aberturas ópticas.
# Cápsulas no plano XZ, extrudadas em Y.
def front_slot(width,height,depth,x,z,y=-1):
    s=rr(width,height,depth,height/2-.01)
    s.rotate(V(),V(1,0,0),90)
    s.translate(V(x,y+depth,z))
    return s
shell=shell.cut(front_slot(42,13,1.65,L/2-21,13))
shell=shell.cut(front_slot(16,8,5,L/2-17,15.5))
shell=shell.cut(Part.makeCylinder(2.7,5,V(L/2+12,-1,19.5),V(0,1,0)))
# Ventilação em uma faixa traseira, deixando o topo principal limpo.
for i in range(9):
    length=9+5*(1-abs(i-4)/4)
    shell=shell.cut(rr(2.4,length,5,1.19,L/2-19.2+i*4.5,W*.68-length/2,H-T-1))
# Símbolo discreto de três ondas, gravado 0,45 mm no topo.
for radius in (3,5.5,8):
    ring=Part.makeCylinder(radius,.6,V(L-21,17,H-.45)).cut(Part.makeCylinder(radius-.8,.8,V(L-21,17,H-.55)))
    sector=Part.makeBox(10,20,1,V(L-21,7,H-.55))
    shell=shell.cut(ring.common(sector))
shell=shell.cut(Part.makeCylinder(1.,.6,V(L-21,17,H-.45)))
# Passagens para abraçadeiras e apoios isolantes de 1 mm sob a eletrônica.
for x in (25,L-25):
    for y in (11,W-11):
        tray=tray.cut(rr(8,3,T+2,1,x-4,y-1.5,-1))
    for y in (20,W-20):
        tray=tray.fuse(rr(10,5,1,2,x-5,y-2.5,T))
# Rebaixos para pés autoadesivos de 8 mm: opcionais, não fazem parte do STL.
for x in (20,L-20):
    for y in (15,W-15):
        tray=tray.cut(Part.makeCylinder(4.2,.8,V(x,y,0)))
tray=tray.removeSplitter()
shell=shell.removeSplitter()
checks={'interferencia_mm3':tray.common(shell).Volume,'dimensoes_externas_mm':[L,W,H]}
assert checks['interferencia_mm3']<.001, checks
# Envelope retangular acima dos apoios. Só comprimento/largura foram medidos.
# A altura é a capacidade disponível, não uma medida informada do ESP32.
board_z=T+1+.01
board_height=H-T-board_z-.01
board_envelope=Part.makeBox(52,29,board_height,V((L-52)/2,(W-29)/2,board_z))
checks['esp32_mm']=[52,29]
checks['altura_disponivel_sobre_apoios_mm']=round(board_height,2)
checks['interferencia_envelope_esp32_mm3']=board_envelope.common(tray.fuse(shell)).Volume
assert checks['interferencia_envelope_esp32_mm3']<.001, checks
# STLs orientados para impressão: exterior de cada peça na mesa.
print_shell=shell.copy()
print_shell.rotate(V(0,W/2,0),V(1,0,0),180)
print_shell.translate(V(0,0,H))
for name,shape in [('base',tray),('tampa',print_shell)]:
    assert shape.isValid() and len(shape.Solids)==1,name
    mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.05,AngularDeflection=.12,Relative=False)
    assert mesh.isSolid(),name
    mesh.write(str(OUT/(name+'.stl')))
    checks[name]={'solido_valido':True,'malha_fechada':True,'volume_mm3':round(shape.Volume,2),'triangulos':mesh.CountFacets}
# Documento em montagem fechada e uma vista explodida para inspecionar.
name='Caixa_IR_Gree_Compacta'
if name in App.listDocuments():
    raise RuntimeError('Feche o documento compacto antes de regenerar para não perder alterações.')
doc=App.newDocument(name)
for name,label,shape in [('Base','Bandeja inferior · parafusos ocultos',tray),('Tampa','Carcaça superior · PLA carmesim',shell)]:
    obj=doc.addObject('PartDesign::Feature',name)
    obj.Label=label
    obj.Shape=shape.cleaned()
    obj.addProperty('App::PropertyString','Fonte').Fonte='gerar_caixa.py — dimensões ajustáveis no script'
    if App.GuiUp:
        obj.Visibility=True
        obj.ViewObject.ShapeColor=(.62,.035,.13)
        obj.ViewObject.LineColor=(.22,.025,.05)
        obj.ViewObject.DisplayMode='Flat Lines'
        obj.ViewObject.LineWidth=1.
        obj.ViewObject.AngularDeflection=10
        obj.ViewObject.Deviation=.1
sheet=doc.addObject('Spreadsheet::Sheet','Medidas')
for i,(key,val) in enumerate([('Comprimento',L),('Largura',W),('Altura',H),('Parede',T),('Raio',R),('Junta inferior',SEAM),('Folga por lado',GAP)],1):
    sheet.set(f'A{i}',key);sheet.set(f'B{i}',str(val)+' mm')
sheet.setColumnWidth('A',180)
footprint=doc.addObject('PartDesign::Feature','ReferenciaESP32')
footprint.Label='Referência 52 × 29 mm · altura real não informada · não imprimir'
footprint.Shape=Part.makeBox(52,29,1.6,V((L-52)/2,(W-29)/2,T+1)).cleaned()
if App.GuiUp:
    footprint.ViewObject.ShapeColor=(.1,.45,.25)
    footprint.Visibility=False
doc.recompute()
Import.export([doc.getObject('Base'),doc.getObject('Tampa')],str(OUT/'caixa_ir_gree_compacta.step'))
if App.GuiUp:
    import FreeCADGui as Gui
    Gui.activeDocument().activeView().viewAxonometric()
    Gui.activeDocument().activeView().fitAll()
doc.recompute()
doc.saveAs(str(OUT/'caixa_ir_gree_compacta.FCStd'))
(OUT/'validacao.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
