from ovito.io import import_file
from ovito.modifiers import SelectTypeModifier, DeleteSelectedModifier, AssignColorModifier
from ovito.vis import Viewport, TachyonRenderer
Renderer = TachyonRenderer(ambient_occlusion_brightness = 0.6, direct_light_intensity = 0.7, depth_of_field = True)
selector0 = SelectTypeModifier(types = {0})
selector1 = SelectTypeModifier(types = {1})
delector = DeleteSelectedModifier()
coloror = AssignColorModifier(color=(1.0, .9, 0.8))

rand = [
    (0.75, 10, 0.7), (0.75, 14, 0.3), (0.75, 14, 0.8), (0.75, 18, 0.5), (0.75, 18, 0.55), (0.75, 18, 0.75), (0.75, 18, 0.8),
    (0.75, 22, 0.8), (0.75, 26, 0.3), (0.75, 26, 0.4), (0.75, 26, 0.75), (0.75, 26, 0.8), (0.75, 30, 0.6), (0.75, 34, 0.3),
    (0.75, 34, 0.4), (0.75, 34, 0.6), (0.75, 42, 0.35),
    (0.5, 10, 0.8), (0.5, 14, 0.8), (0.5, 18, 0.8), (0.5, 22, 0.3), (0.5, 22, 0.4), (0.5, 26, 0.2), (0.5, 26, 0.6), (0.5, 34, 0.7),
    (0.5, 34, 0.25),
    (0.25, 26, 0.7), (0.25, 30, 0.8), (0.25, 34, 0.8), (0.25, 42, 0.65), (0.25, 42, 0.8)
]

def Render1(item, Renderer, selector0, delector):
    pipeline = import_file('./../frac_'+str(item[0])+'/m_'+str(item[1])+'/d_'+str(item[2])+'/final_snapshot.xyz')

    pipeline.modifiers.append(selector0)
    pipeline.modifiers.append(delector)

    pipeline.add_to_scene()

    vis_element = pipeline.source.data.particles.vis
    vis_element.radius = .5

    cell_vis = pipeline.source.data.cell.vis
    cell_vis.render_cell = False

    vp = Viewport(type = Viewport.Type.Left)
    vp.zoom_all(size=(600, 500))
    image = vp.render_image(size=(600, 500), alpha=True, renderer = Renderer)
    
    image.save("f-"+str(int((1-item[0])*10%10))+"/rand/b-"+str(item[1])+"_d-"+str(item[2])+"(phobic).png")

    pipeline.remove_from_scene()

def Render0(item, Renderer, selector1, delector, coloror):
    pipeline = import_file('./../frac_'+str(item[0])+'/m_'+str(item[1])+'/d_'+str(item[2])+'/final_snapshot.xyz')

    pipeline.modifiers.append(selector1)
    pipeline.modifiers.append(delector)
    pipeline.modifiers.append(coloror)

    pipeline.add_to_scene()

    vis_element = pipeline.source.data.particles.vis
    vis_element.radius = .5

    cell_vis = pipeline.source.data.cell.vis
    cell_vis.render_cell = False

    vp = Viewport(type = Viewport.Type.Back)
    vp.zoom_all(size=(600, 500))
    image = vp.render_image(size=(600, 500), alpha=True, renderer = Renderer)
    
    image.save("f-"+str(int((1-item[0])*10%10))+"/rand/b-"+str(item[1])+"_d-"+str(item[2])+"(philic).png")

    pipeline.remove_from_scene()

def VP(rand, Renderer, selector1, selector2, delector, coloror):
    
    for item in rand:                               
        Render1(item, Renderer, selector0, delector)
        Render0(item, Renderer, selector1, delector, coloror)
                   
    exit()               

VP(rand, Renderer, selector0, selector1, delector, coloror)
