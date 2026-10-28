"""Renderização 3D das malhas reais com profundidade e iluminação de estúdio."""
import json,os
from pathlib import Path
os.environ.setdefault('EGL_PLATFORM','surfaceless')
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkRenderingCore import vtkRenderer,vtkPolyDataMapper,vtkActor,vtkLight,vtkWindowToImageFilter,vtkTextActor
from vtkmodules.vtkRenderingOpenGL2 import vtkEGLRenderWindow
from vtkmodules.vtkIOImage import vtkPNGWriter
import vtkmodules.vtkRenderingFreeType
p=Path(__file__).resolve().parent
L,W,H=json.loads((p/'validacao.json').read_text())['dimensoes_externas_mm']
for filename,side,parts,label in [
 ('previa.png','front',('base','tampa'),'Cantos retos · micro-USB do ESP32 na lateral esquerda'),
 ('previa_traseira.png','back',('base','tampa'),'Topo liso · ventilação traseira'),
 ('previa_apoio.png','inside',('base',),'Berço do ESP32 de cabeça para baixo · quatro travas'),
 ('previa_interna.png','layout',('base','esp32','jumpers_esp32','emissor_pcb','emissor_led','jumpers_emissor'),
  'Proposta interna · ESP32 invertido, emissor no teto e jumpers')]:
 renderer=vtkRenderer();renderer.SetBackground(.968,.956,.94)
 window=vtkEGLRenderWindow();window.SetOffScreenRendering(1)
 window.SetSize(1600,1100);window.SetMultiSamples(8);window.AddRenderer(renderer)
 # Mantém referências dos pipelines até finalizar cada imagem.
 pipelines=[]
 for name in parts:
  mesh_path=p/(name+'.stl') if name in ('base','tampa') else Path('/tmp')/('ir_visual_'+name+'.stl')
  reader=vtkSTLReader();reader.SetFileName(str(mesh_path));reader.Update()
  trans=vtkTransform()
  if name=='tampa':
   trans.Translate(0,W,H);trans.RotateX(180)
  filt=vtkTransformFilter();filt.SetInputConnection(reader.GetOutputPort());filt.SetTransform(trans)
  normals=vtkPolyDataNormals();normals.SetInputConnection(filt.GetOutputPort())
  normals.SetFeatureAngle(35);normals.ConsistencyOn();normals.AutoOrientNormalsOn();normals.SplittingOn()
  mapper=vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort());mapper.ScalarVisibilityOff()
  actor=vtkActor();actor.SetMapper(mapper)
  colors={'esp32':(.035,.12,.09),
          'emissor_pcb':(.06,.18,.11),'emissor_led':(.04,.06,.11),
          'jumpers_esp32':(.08,.08,.09),'jumpers_emissor':(.08,.08,.09)}
  prop=actor.GetProperty();prop.SetColor(*colors.get(name,(.58,.025,.12)))
  prop.SetAmbient(.22);prop.SetDiffuse(.72);prop.SetSpecular(.25);prop.SetSpecularPower(55)
  prop.SetInterpolationToPhong();renderer.AddActor(actor)
  pipelines.append((reader,trans,filt,normals,mapper,actor))
 renderer.RemoveAllLights()
 for pos,power in [((L*1.4,-W*1.7,H*5),.85),((-L,W,H*2),.5),((L,W*3,H*4),.7)]:
  light=vtkLight();light.SetPosition(*pos);light.SetFocalPoint(L/2,W/2,H/2)
  light.SetIntensity(power);light.SetLightTypeToSceneLight();renderer.AddLight(light)
 cam=renderer.GetActiveCamera();cam.ParallelProjectionOn()
 target=(L/2,W/2,H*.5 if len(parts)>1 else 5)
 cam.SetFocalPoint(*target)
 cam.SetPosition(L*2.4,-W*2.4,H*2.4) if side in ('front','layout') else cam.SetPosition(L*2.4,W*3.4,H*2.4)
 if side=='inside':cam.SetPosition(L*1.8,-W*1.8,H*4)
 cam.SetViewUp(0,0,1);cam.SetParallelScale(46 if len(parts)>1 else 40)
 renderer.ResetCameraClippingRange()
 def text_actor(text,x,y,size,color):
  actor=vtkTextActor();actor.SetInput(text);actor.SetPosition(x,y)
  prop=actor.GetTextProperty();prop.SetFontFamilyToArial();prop.SetFontSize(size)
  prop.SetColor(*color);renderer.AddViewProp(actor);return actor
 heading=text_actor('IR / GREE',95,980,42,(.32,.075,.16))
 subtitle=text_actor(label,95,930,25,(.42,.38,.39))
 measures=' × '.join(f'{n:g}'.replace('.',',') for n in (L,W,H))
 footer_text=measures+' mm · PLA carmesim · render das malhas reais'
 if side=='layout':footer_text='Referências ilustrativas · medidas das placas e pinos a conferir'
 footer=text_actor(footer_text,95,70,20 if side=='layout' else 23,(.42,.38,.39))
 window.Render()
 capture=vtkWindowToImageFilter();capture.SetInput(window);capture.ReadFrontBufferOff();capture.Update()
 writer=vtkPNGWriter();writer.SetFileName(str(p/filename));writer.SetInputConnection(capture.GetOutputPort());writer.Write()
 window.Finalize()
 print(filename)
