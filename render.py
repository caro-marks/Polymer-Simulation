from ovito.io import import_file
from ovito.vis import Viewport
# Renderer = TachyonRenderer()

Beads_range=[x for x in range(10,50,4) if x not in (38,46)] # # # #    monomer's range
Dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
Frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range

def Render(Frac, Bead, Dens):
    data = import_file('./frac_'+str(Frac)+'/m_'+str(Bead)+'/d_'+str(Dens)+'/final_snapshot.xyz')
    data.add_to_scene()

    vis_element = data.source.data.particles.vis
    vis_element.radius = .9

    cell_vis = data.source.data.cell.vis
    cell_vis.render_cell = False

    vp = Viewport(type = Viewport.Type.Perspective)
    vp.zoom_all(size=(600, 500))
    image = vp.render_image(size=(600, 500), alpha=True)
    
    image.save("renders/f-"+str(int((1-Frac)*10%10))+"/b-"+str(Bead)+"_d-"+str(Dens)+".png")

    data.remove_from_scene()

def VP(Fracs, Beads, Denss):
    
    Fracs.reverse()

    for Frac in Fracs:

        for Bead in Beads:

            for Dens in Denss:
                               
                Render(Frac, Bead, Dens)
                   
    exit()               

VP(Frac_range, Beads_range, Dens_range)
