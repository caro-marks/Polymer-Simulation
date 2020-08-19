from ovito.io import import_file
from ovito.vis import Viewport
import os

Beads_range=[x for x in range(10,50,4) if x not in (38,46)] # # # #    monomer's range
Dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
Frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range

def Render(Data):
    Data.add_to_scene()

    vis_element = Data.source.data.particles.vis
    vis_element.radius = 1.

    cell_vis = Data.source.data.cell.vis
    cell_vis.render_cell = False

    vp = Viewport()
    vp.type = Viewport.Type.Perspective
    vp.zoom_all()

    image = vp.render_image()
    return image

def VP(Fracs, Beads, Denss):

    pre = 'results/renders/f_'

    for Frac in Fracs:

        f = int((1-Frac)*10%10)

        for Bead in Beads:

            for Dens in Denss:

                output_folder = './'+str(pre)+str(f)+'/b_'+str(Bead)+'/d_'+str(Dens)
                os.makedirs(output_folder)
                
                input_file = './frac_'+str(Frac)+'/m_'+str(Bead)+'/d_'+str(Dens)+'/final_snapshot.xyz'

                data = import_file(input_file)


                Render(data).save(str(output_folder) +"/render.png")

VP(Frac_range, Beads_range, Dens_range)

exit()