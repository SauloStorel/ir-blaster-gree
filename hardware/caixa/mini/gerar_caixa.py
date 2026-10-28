"""Caixa mini: ESP32 de 52 × 29 mm de cabeça para baixo, ligado ao emissor IR por jumpers Dupont."""
import sys, json, tempfile
from pathlib import Path
sys.path.insert(0, '/usr/lib/freecad/lib')
import FreeCAD as App
import Part, MeshPart, Import
V=App.Vector
OUT=Path(__file__).resolve().parent
T=2.4
# Visual mais quadrado: cantos e bordas com raios pequenos.
R=6.
TOP_ROUND, BOTTOM_ROUND = 2., 1.2
SEAM=8.
GAP=.3
JOINT_GAP=0.
PCB_T, SLOT_CLEARANCE = 1.6, .15
L=64.
# Jumper Dupont fêmea: capa reta de ~14 mm; o fio precisa de ~7 mm além dela
# para dobrar 90° (ponta rígida de ~3 mm e raio de ~4 mm).
DUPONT_LENGTH, DUPONT_SIDE, WIRE_TURN = 14., 2.54, 7.
# Emissor KY-005 preso nos trilhos do teto, com o LED no furo da frente.
# Os pinos em ângulo reto saem para trás, por cima da placa.
EMITTER_PCB_W, EMITTER_PCB_D = 15., 18.5
LED_RADIUS, LED_BODY, LED_CENTER_Y = 2.5, 5.8, 2.7
EMITTER_Y=LED_CENTER_Y+LED_BODY
EMITTER_X=L/2
# Profundidade: LED, PCB do emissor, capa Dupont e a dobra do fio até a parede de trás.
W=round(EMITTER_Y+EMITTER_PCB_D+DUPONT_LENGTH+WIRE_TURN+T,1)
# ESP32 DevKit de 30 pinos de cabeça para baixo: componentes para baixo, pinos para cima.
# O micro-USB fica sob a placa, na ponta esquerda; a placa sobe o suficiente para
# a borracha do plugue (~11 × 7,5 mm) entrar sem tocar o fundo.
BOARD_L, BOARD_W = 52., 29.
BX, BY = (L-BOARD_L)/2, (W-BOARD_W)/2
COMPONENT_HEIGHT=3.5
USB_WIDTH, USB_HEIGHT, USB_UNDER_BOARD = 12., 9., 1.4
PLUG_W, PLUG_H = 11., 7.5
BOARD_Z=T+.3+PLUG_H/2+USB_UNDER_BOARD
BOARD_TOP=BOARD_Z+PCB_T
USB_CENTER_Z=BOARD_Z-USB_UNDER_BOARD
ROW_INSET, PIN_PITCH, PINS_PER_ROW = 1.45, 2.54, 15
HEADER_SPACER, PIN_RISE = 2.5, 8.5
# A fileira de trás tem 3V3, GND e D4 perto do USB: é ela que recebe os jumpers.
JUMPER_PINS=5  # 3V3, GND, D15, D2 e D4, a partir da ponta do USB
# Os jumpers sobem da fileira de trás e dobram rente ao teto.
H=round(BOARD_TOP+HEADER_SPACER+DUPONT_LENGTH+WIRE_TURN+T,1)
# Emissor acima das pontas dos pinos do ESP32, com folga para as soldas sob a sua PCB.
EMITTER_PCB_Z=BOARD_TOP+PIN_RISE+2.
OPTIC_Z=EMITTER_PCB_Z+PCB_T+LED_RADIUS

def rr(l,w,h,r,x=0,y=0,z=0):
    b=Part.makeBox(l,w,h,V(x,y,z))
    return b.makeFillet(r,[e for e in b.Edges if e.BoundBox.ZLength>h-.001])

def edge_round(s,z,r):
    return s.makeFillet(r,[e for e in s.Edges if abs(e.BoundBox.ZMin-z)<1e-5 and abs(e.BoundBox.ZMax-z)<1e-5])

# Todos os sólidos são construídos primeiro na posição de montagem.
outer=edge_round(rr(L,W,H-SEAM,R,z=SEAM),H,TOP_ROUND)
outer=edge_round(outer,SEAM,.05)
shell=outer.cut(rr(L-2*T,W-2*T,H-T+1,R-T,T,T,-1))
tray=edge_round(rr(L,W,SEAM-JOINT_GAP,R),0,BOTTOM_ROUND)
tray=edge_round(tray,SEAM-JOINT_GAP,.05)
tray=tray.cut(rr(L-2*T,W-2*T,H,R-T,T,T,T))
# As bordas externas encostam em z=8; a folga de 0,3 mm fica só na saia interna.
inset=T+GAP
lip=rr(L-2*inset,W-2*inset,3.3,R-inset,inset,inset,SEAM-.2)
lip=lip.cut(rr(L-2*(inset+1.6),W-2*(inset+1.6),5,R-inset-1.6,inset+1.6,inset+1.6,SEAM-1))
# Degrau interno desce até o fundo: sem balanço sob a saia na impressão.
shoulder=rr(L-3.8,W-3.8,SEAM-.05-T,R-1.9,1.9,1.9,T)
shoulder=shoulder.cut(rr(L-2*(inset+1.6),W-2*(inset+1.6),SEAM,R-inset-1.6,inset+1.6,inset+1.6,T-1))
lip=lip.fuse(shoulder)
tray=tray.fuse(lip)
# Quatro linguetas horizontais flexíveis na saia, com dentes rampados.
# Sem torres ou furos de parafuso. Cavidades ficam ocultas na parede interna.
SNAP_LENGTH, SNAP_THICKNESS, SNAP_PROJECTION = 12., 1., .6
snap_teeth=[]
snap_pockets=[]
for rear in (False,True):
    for x in (20.,42.):
        # Cada lingueta fica presa somente pela extremidade x+12.
        outer_y=inset if not rear else W-inset-1.6
        bottom_slot=Part.makeBox(SNAP_LENGTH+.5,1.8,.95,V(x-.5,outer_y-.1,7.25))
        tip_slot=Part.makeBox(.55,1.8,4,V(x-.55,outer_y-.1,7.2))
        relief_y=inset+SNAP_THICKNESS if not rear else W-inset-1.7
        inner_relief=Part.makeBox(SNAP_LENGTH,.7,3.2,V(x,relief_y,8.15))
        tray=tray.cut(bottom_slot).cut(tip_slot).cut(inner_relief)
        # Rampas superior e inferior permitem encaixar e soltar com cuidado.
        profile=[(inset,8.8),(inset-SNAP_PROJECTION,9.2),
                 (inset-SNAP_PROJECTION,9.5),(inset,10.7)]
        points=[V(x+1,W-y if rear else y,z) for y,z in profile]
        points.append(points[0])
        tooth=Part.Face(Part.makePolygon(points)).extrude(V(4,0,0))
        tray=tray.fuse(tooth)
        snap_teeth.append(tooth)
        pocket_y=W-2.5 if rear else 1.6
        pocket=Part.makeBox(4.6,.9,2.7,V(x+.7,pocket_y,8.5))
        shell=shell.cut(pocket)
        snap_pockets.append(pocket)
# Frente: rebaixo externo raso com um único furo circular, o do emissor.
# Cápsulas no plano XZ, extrudadas em Y.
def front_slot(width,height,depth,x,z,y=-1):
    s=rr(width,height,depth,height/2-.01)
    s.rotate(V(),V(1,0,0),90)
    s.translate(V(x,y+depth,z))
    return s
shell=shell.cut(front_slot(38,8,1.5,(L-38)/2,OPTIC_Z-4))
EMITTER_DIAMETER=5.2
shell=shell.cut(Part.makeCylinder(EMITTER_DIAMETER/2,5,V(EMITTER_X,-1,OPTIC_Z),V(0,1,0)))
# Transição suave somente no contorno do rebaixo; o furo continua simples.
panel_edges=[e for e in shell.Edges if abs(e.BoundBox.YMin-.5)<1e-6
             and abs(e.BoundBox.YMax-.5)<1e-6
             and (e.BoundBox.XMin<(L-38)/2+.01
                  or e.BoundBox.XMax>(L+38)/2-.01
                  or e.BoundBox.ZMin<OPTIC_Z-3.99 or e.BoundBox.ZMax>OPTIC_Z+3.99)]
assert len(panel_edges)==8
shell=shell.makeFillet(.2,panel_edges)
optic_edges=[e for e in shell.Edges if abs(e.BoundBox.YMin-.5)<1e-6
             and abs(e.BoundBox.YMax-.5)<1e-6
             and abs(e.BoundBox.XLength-EMITTER_DIAMETER)<1e-5]
assert len(optic_edges)==1
shell=shell.makeFillet(.15,optic_edges)
# Passagem do micro-USB na lateral esquerda: atravessa parede, junta e saia da base,
# para a borracha do plugue entrar até a ponta da placa.
USB_CENTER_Y=W/2
USB_BOTTOM=USB_CENTER_Z-USB_HEIGHT/2
usb_cut=rr(USB_WIDTH,USB_HEIGHT,BX-.3+1,1.5)
usb_cut.rotate(V(),V(1,1,1),120)
usb_cut.translate(V(-1,USB_CENTER_Y-USB_WIDTH/2,USB_BOTTOM))
def round_usb_mouth(part):
    edges=[e for e in part.Edges if abs(e.BoundBox.XMin)<1e-6
           and abs(e.BoundBox.XMax)<1e-6
           and e.BoundBox.YMin>USB_CENTER_Y-USB_WIDTH/2-.01
           and e.BoundBox.YMax<USB_CENTER_Y+USB_WIDTH/2+.01
           and e.BoundBox.ZMin>USB_BOTTOM-.01
           and e.BoundBox.ZMax<USB_BOTTOM+USB_HEIGHT+.01
           and e.BoundBox.ZLength+e.BoundBox.YLength>.5]
    assert edges
    return part.makeFillet(.2,edges)
shell=round_usb_mouth(shell.cut(usb_cut))
# Topo inteiramente liso; sete fendas verticais na parede traseira, acima da saia.
VENT_WIDTH, VENT_HEIGHT, VENT_BOTTOM, VENT_PITCH = 2.4, 8., 12., 3.8
vent_centers=[]
for i in range(7):
    x=L/2+(i-3)*VENT_PITCH
    vent_centers.append(x)
    vent=rr(VENT_WIDTH,VENT_HEIGHT,5,1.19)
    vent.rotate(V(),V(1,0,0),90)
    vent.translate(V(x-VENT_WIDTH/2,W+1,VENT_BOTTOM))
    shell=shell.cut(vent)
# Trilhos no teto para a PCB do emissor deitada: ela entra por trás até a aba
# do LED encostar no furo frontal. Crescem a partir do teto, sem suportes na impressão.
# Folga lateral de 1 mm e apoio de 1 mm por borda: servem placas de 14 a 16 mm.
RAIL_WIDTH, RAIL_OVERLAP, RAIL_PLAY, RAIL_Y = 1.2, 1., 1., EMITTER_Y+.5
RAIL_LENGTH=EMITTER_PCB_D-3
RAIL_BOTTOM=EMITTER_PCB_Z-1.2
for side in (-1,1):
    edge=EMITTER_X+side*EMITTER_PCB_W/2
    inner=edge-side*RAIL_OVERLAP
    groove_bottom=edge+side*RAIL_PLAY
    outer_face=groove_bottom+side*RAIL_WIDTH
    rail=Part.makeBox(abs(outer_face-inner),RAIL_LENGTH,H-T-RAIL_BOTTOM+.5,
                      V(min(inner,outer_face),RAIL_Y,RAIL_BOTTOM))
    groove=Part.makeBox(abs(groove_bottom-inner),RAIL_LENGTH+2,PCB_T+2*SLOT_CLEARANCE,
                        V(min(inner,groove_bottom),RAIL_Y-1,EMITTER_PCB_Z-SLOT_CLEARANCE))
    shell=shell.fuse(rail.cut(groove))
# Fundo contínuo: sem passagens de abraçadeira ou rebaixos para pés.
# Berço do ESP32: quatro apoios sob os cantos da placa, fora das fileiras de pinos
# e dos componentes, com guias em L de 1,5 mm acima da placa. Sem travas.
PAD_L, PAD_W, GUIDE_WALL, GUIDE_CLEARANCE, GUIDE_RISE = 2.5, 2.2, 1.2, .35, 1.5
for x_end,x_in in ((BX,1),(BX+BOARD_L,-1)):
    for y_end,y_in in ((BY,1),(BY+BOARD_W,-1)):
        outside=GUIDE_CLEARANCE+GUIDE_WALL
        x0,x1=sorted((x_end-x_in*outside,x_end+x_in*PAD_L))
        y0,y1=sorted((y_end-y_in*outside,y_end+y_in*PAD_W))
        pad=Part.makeBox(x1-x0,y1-y0,BOARD_Z-T,V(x0,y0,T))
        gx0,gx1=sorted((x_end-x_in*outside,x_end-x_in*GUIDE_CLEARANCE))
        gy0,gy1=sorted((y_end-y_in*outside,y_end-y_in*GUIDE_CLEARANCE))
        guide_x=Part.makeBox(gx1-gx0,y1-y0,GUIDE_RISE,V(gx0,y0,BOARD_Z))
        guide_y=Part.makeBox(x1-x0,gy1-gy0,GUIDE_RISE,V(x0,gy0,BOARD_Z))
        tray=tray.fuse(pad).fuse(guide_x).fuse(guide_y)
tray=tray.cut(usb_cut)
tray=tray.removeSplitter()
shell=shell.removeSplitter()
checks={'interferencia_mm3':tray.common(shell).Volume,'dimensoes_externas_mm':[L,W,H],
        'microusb_lateral_esquerda':{'face':'x=0','centro_y_mm':USB_CENTER_Y,
        'largura_mm':USB_WIDTH,'altura_mm':USB_HEIGHT,'altura_inferior_mm':round(USB_BOTTOM,2),
        'centro_z_mm':round(USB_CENTER_Z,2),'usb_nativo_esp32':True},
        'topo_liso':True,'ventilacao_traseira':{'quantidade':7,'largura_mm':VENT_WIDTH,
        'altura_mm':VENT_HEIGHT,'altura_inferior_mm':VENT_BOTTOM},
        'aberturas_ir_frontais':{'quantidade':1,'receptor':False,
        'profundidade_rebaixo_mm':.5,'emissor_diametro_mm':EMITTER_DIAMETER,
        'emissor_centro_x_mm':EMITTER_X,'altura_eixo_mm':round(OPTIC_Z,2)},
        'acabamento':{'raio_cantos_mm':R,'raio_borda_superior_mm':TOP_ROUND,
        'raio_borda_inferior_mm':BOTTOM_ROUND,'raio_rebaixo_mm':.2,'junta_mm':JOINT_GAP,
        'raio_bordas_junta_mm':.05,'raio_boca_furo_ir_mm':.15,'raio_boca_usb_mm':.2}}
checks['fundo']={'furos_parafusos':0,'passagens_abracadeiras':0,'rebaixos_pes':0,
 'espessura_mm':T}
checks['fechamento']={'tipo':'encaixe com linguetas rampadas','travas':4,
 'comprimento_flexivel_mm':SNAP_LENGTH,'espessura_lingueta_mm':SNAP_THICKNESS,
 'projecao_dente_mm':SNAP_PROJECTION,'deflexao_nominal_montagem_mm':SNAP_PROJECTION-GAP,
 'ensaio_fisico_realizado':False}
# A seção próxima da face externa deve ser um único contorno sem furos.
bottom_wires=tray.slice(V(0,0,1),.1)
assert len(bottom_wires)==1 and bottom_wires[0].isClosed()
for tooth,pocket in zip(snap_teeth,snap_pockets):
    assert tooth.common(shell).Volume<.001
    assert tooth.common(pocket).Volume>.01
# Comprova a folga nominal de entrada dos dentes com deslocamento radial.
for i,tooth in enumerate(snap_teeth):
    flexed=tooth.copy()
    flexed.translate(V(0,-.31 if i>=2 else .31,0))
    for offset in (-4.,-2.,0.):
        moved=flexed.copy()
        moved.translate(V(0,0,offset))
        assert moved.common(shell).Volume<.001
assert checks['interferencia_mm3']<.001, checks
# Fechamento assentado: faces de apoio em contato, contornos exteriores alinhados.
contact=tray.common(shell)
def seating_faces(part):
    return [f for f in part.Faces if abs(f.BoundBox.ZMin-SEAM)<1e-6
            and abs(f.BoundBox.ZMax-SEAM)<1e-6]
contact_area=sum(a.common(b).Area for a in seating_faces(tray) for b in seating_faces(shell))
assert contact_area>100 and contact.Volume<.001
footprints=[]
for part,z in ((tray,SEAM-.3),(shell,SEAM+.3)):
    wire=max(part.slice(V(0,0,1),z),key=lambda w:w.BoundBox.XLength*w.BoundBox.YLength)
    b=wire.BoundBox
    footprint=[b.XMin,b.YMin,b.XMax,b.YMax]
    assert max(abs(a-b) for a,b in zip(footprint,(0,0,L,W)))<1e-5
    footprints.append(footprint)
checks['assentamento']={'area_contato_mm2':round(contact_area,2),
 'folga_vertical_bordas_mm':JOINT_GAP,'folga_lateral_saia_mm':GAP,
 'contornos_externos_alinhados':True}
box=tray.fuse(shell)
assert not shell.isInside(V(T/2,USB_CENTER_Y,SEAM+1),1e-6,True)
assert not tray.isInside(V(T/2,USB_CENTER_Y,USB_CENTER_Z),1e-6,True)
# Plugue micro-USB encaixado: borracha encostada na ponta da placa, acima do fundo.
plug=Part.makeBox(15,PLUG_W,PLUG_H,V(BX-.5-15,USB_CENTER_Y-PLUG_W/2,USB_CENTER_Z-PLUG_H/2))
assert plug.common(box).Volume<.001, 'Plugue micro-USB não alcança o ESP32'
assert shell.isInside(V(L-T/2,W/2,12),1e-6,True), 'Lateral direita deve estar fechada'
# Confere a continuidade do topo plano e a abertura efetiva das fendas traseiras.
roof_probe=Part.makeBox(L-2*R,W-2*R,.3,V(R,R,H-.3))
assert abs(roof_probe.common(shell).Volume-roof_probe.Volume)<.001
for x in vent_centers:
    assert not shell.isInside(V(x,W-T/2,VENT_BOTTOM+VENT_HEIGHT/2),1e-6,True)
# Referências: PCB do ESP32, componentes por baixo (fora dos cantos), barras de pinos,
# jumpers com a dobra do fio, emissor e LED. Nenhuma pode tocar a caixa ou outra.
esp_pcb=Part.makeBox(BOARD_L,BOARD_W,PCB_T,V(BX,BY,BOARD_Z))
components=Part.makeBox(BOARD_L,BOARD_W-2*(PAD_W+.6),COMPONENT_HEIGHT,
                        V(BX,BY+PAD_W+.6,BOARD_Z-COMPONENT_HEIGHT))
header_x=BX+(BOARD_L-PINS_PER_ROW*PIN_PITCH)/2
row_y={'frente':BY+ROW_INSET,'tras':BY+BOARD_W-ROW_INSET}
pin_rows={side:Part.makeBox(PINS_PER_ROW*PIN_PITCH,PIN_PITCH,PIN_RISE,V(header_x,y-PIN_PITCH/2,BOARD_TOP))
          for side,y in row_y.items()}
jumper_top=BOARD_TOP+HEADER_SPACER+DUPONT_LENGTH
esp_jumpers=Part.makeBox(JUMPER_PINS*PIN_PITCH,DUPONT_SIDE,DUPONT_LENGTH,
                         V(header_x,row_y['tras']-DUPONT_SIDE/2,BOARD_TOP+HEADER_SPACER))
# Os fios dos jumpers do ESP32 dobram para trás, rente ao teto.
esp_wire_turn=Part.makeBox(JUMPER_PINS*PIN_PITCH,DUPONT_SIDE+WIRE_TURN,WIRE_TURN,
                           V(header_x,row_y['tras']-DUPONT_SIDE/2,jumper_top))
emitter_pcb=Part.makeBox(EMITTER_PCB_W,EMITTER_PCB_D,PCB_T,
                         V(EMITTER_X-EMITTER_PCB_W/2,EMITTER_Y,EMITTER_PCB_Z))
emitter_led=Part.makeCylinder(LED_RADIUS,LED_BODY,V(EMITTER_X,LED_CENTER_Y,OPTIC_Z),V(0,1,0)).fuse(
    Part.makeSphere(LED_RADIUS,V(EMITTER_X,LED_CENTER_Y,OPTIC_Z)))
emitter_jumpers=Part.makeBox(3*PIN_PITCH,DUPONT_LENGTH,DUPONT_SIDE,
                             V(EMITTER_X-1.5*PIN_PITCH,EMITTER_Y+EMITTER_PCB_D,EMITTER_PCB_Z+PCB_T))
# Os fios do emissor dobram de lado, na mesma altura, antes da parede de trás.
emitter_wire_turn=Part.makeBox(3*PIN_PITCH,WIRE_TURN,DUPONT_SIDE,
                               V(EMITTER_X-1.5*PIN_PITCH,EMITTER_Y+EMITTER_PCB_D+DUPONT_LENGTH,
                                 EMITTER_PCB_Z+PCB_T))
references={'esp32':esp_pcb,'componentes_esp32':components,'pinos_frente':pin_rows['frente'],
            'pinos_tras':pin_rows['tras'],'jumpers_esp32':esp_jumpers,'dobra_fios_esp32':esp_wire_turn,
            'emissor_pcb':emitter_pcb,'emissor_led':emitter_led,'jumpers_emissor':emitter_jumpers,
            'dobra_fios_emissor':emitter_wire_turn}
for name,shape in references.items():
    assert shape.common(box).Volume<.001, f'{name} encosta na caixa'
# Peças que se tocam de propósito; todo o resto precisa ficar separado.
TOUCHING={('esp32','componentes_esp32'),('esp32','pinos_frente'),('esp32','pinos_tras'),
          ('pinos_tras','jumpers_esp32'),('jumpers_esp32','dobra_fios_esp32'),
          ('emissor_pcb','emissor_led'),('emissor_pcb','jumpers_emissor'),
          ('jumpers_emissor','dobra_fios_emissor')}
names=list(references)
for i,a in enumerate(names):
    for b in names[i+1:]:
        if (a,b) not in TOUCHING:
            assert references[a].common(references[b]).Volume<.001, f'{a} colide com {b}'
# As placas ficam presas: qualquer deslocamento de 0,4 mm encontra guia ou trilho.
def held(pcb,part,axis):
    for offset in (-.4,.4):
        moved=pcb.copy()
        moved.translate(axis*offset)
        assert moved.common(part).Volume>.01
held(esp_pcb,tray,V(1,0,0))
held(esp_pcb,tray,V(0,1,0))
held(emitter_pcb,shell,V(0,0,1))
for width in (EMITTER_PCB_W-1,EMITTER_PCB_W+1):
    pcb=Part.makeBox(width,EMITTER_PCB_D,PCB_T,V(EMITTER_X-width/2,EMITTER_Y,EMITTER_PCB_Z))
    assert pcb.common(shell).Volume<.001, f'PCB de {width} mm não entra nos trilhos'
    held(pcb,shell,V(0,0,1))
checks['esp32_invertido']={'dimensao_nominal_placa_mm':[BOARD_L,BOARD_W],
 'componentes':'para baixo','pinos':'para cima','altura_pcb_sobre_fundo_mm':round(BOARD_Z-T,2),
 'apoios_nos_cantos_mm':[PAD_L,PAD_W],'altura_componentes_suposta_mm':COMPONENT_HEIGHT,
 'folga_componentes_ate_fundo_mm':round(BOARD_Z-COMPONENT_HEIGHT-T,2),
 'folga_pinos_ate_pcb_emissor_mm':round(EMITTER_PCB_Z-(BOARD_TOP+PIN_RISE),2),
 'encaixe_livre_sem_trava':True}
checks['jumpers']={'tipo':'Dupont fêmea','capa_suposta_mm':DUPONT_LENGTH,'dobra_do_fio_mm':WIRE_TURN,
 'fileira_esp32':'de trás: 3V3, GND e D4 perto do USB','medida_confirmada':False}
checks['suporte_emissor']={'tipo':'trilhos no teto da carcaça, entrada por trás',
 'pcb_catalogo_mm':[EMITTER_PCB_W,EMITTER_PCB_D],'apoio_por_borda_mm':RAIL_OVERLAP,
 'larguras_aceitas_mm':[EMITTER_PCB_W-1,EMITTER_PCB_W+1],'altura_pcb_mm':round(EMITTER_PCB_Z,2),
 'folga_vertical_mm':SLOT_CLEARANCE,'comprimento_trilhos_mm':RAIL_LENGTH,'medida_confirmada':False}
checks['referencias_sem_interferencia']=True
# Malhas das referências para render_vtk.py; não são peças de impressão.
VISUAL_REFERENCES=('esp32','emissor_pcb','emissor_led','jumpers_esp32','jumpers_emissor')
visual_dir=Path(tempfile.gettempdir())
for name in VISUAL_REFERENCES:
    MeshPart.meshFromShape(Shape=references[name],LinearDeflection=.05,AngularDeflection=.12,
                           Relative=False).write(str(visual_dir/f'ir_visual_{name}.stl'))
# STLs orientados para impressão: exterior de cada peça na mesa.
print_shell=shell.copy()
print_shell.rotate(V(0,W/2,0),V(1,0,0),180)
print_shell.translate(V(0,0,H))
for name,shape in [('base',tray),('tampa',print_shell)]:
    assert shape.isValid() and len(shape.Solids)==1,name
    mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.025,AngularDeflection=.08,Relative=False)
    assert mesh.isSolid(),name
    mesh.write(str(OUT/(name+'.stl')))
    checks[name]={'solido_valido':True,'malha_fechada':True,'volume_mm3':round(shape.Volume,2),'triangulos':mesh.CountFacets}
# Duas amostras pequenas para conferir a tolerância de uma trava antes da caixa.
crop=Part.makeBox(17,8.5,12,V(18,0,0))
for name,shape in [('teste_encaixe_base',tray.common(crop)),
                   ('teste_encaixe_parede',shell.common(crop))]:
    shape=shape.removeSplitter()
    assert shape.isValid() and len(shape.Solids)==1,name
    shape.translate(V(-18,0,-shape.BoundBox.ZMin))
    mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.05,AngularDeflection=.12,Relative=False)
    assert mesh.isSolid(),name
    mesh.write(str(OUT/(name+'.stl')))
checks['amostras_encaixe_stl']=['teste_encaixe_base.stl','teste_encaixe_parede.stl']
# Documento em montagem fechada para inspecionar.
name='Caixa_IR_Gree_Mini'
if name in App.listDocuments():
    raise RuntimeError('Feche o documento mini antes de regenerar para não perder alterações.')
doc=App.newDocument(name)
for name,label,shape in [('Base','Base · berço do ESP32 invertido e quatro travas',tray),('Tampa','Carcaça superior · trilhos do emissor, encaixe sem parafusos',shell)]:
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
# Referências verdes ocultas: ESP32, emissor e jumpers, para examinar a montagem interna.
for name in VISUAL_REFERENCES:
    obj=doc.addObject('PartDesign::Feature','Referencia_'+name)
    obj.Label=name.replace('_',' ')+' · não imprimir'
    obj.Shape=references[name].cleaned()
    obj.addProperty('App::PropertyString','Observacao').Observacao='Referência ilustrativa; medidas das placas e dos jumpers a conferir.'
    if App.GuiUp:
        obj.ViewObject.ShapeColor=(.15,.35,.2)
        obj.Visibility=False
doc.recompute()
Import.export([doc.getObject('Base'),doc.getObject('Tampa')],str(OUT/'caixa_ir_gree_mini.step'))
if App.GuiUp:
    import FreeCADGui as Gui
    Gui.activeDocument().activeView().viewAxonometric()
    Gui.activeDocument().activeView().fitAll()
doc.recompute()
doc.saveAs(str(OUT/'caixa_ir_gree_mini.FCStd'))
(OUT/'validacao.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
