from ovito.modifiers import CentroSymmetryModifier
from ovito.io import import_file, export_file
import os

Beads_range=[x for x in range(10,50,4) if x not in (38,46)] # # # #    monomer's range
Dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
Frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range

def GenerateData(Fracs, Beads, Denss):
    pre = 'results/snapshots/centro-symmetric/f_'

    for Frac in Fracs:

        f = int((1-Frac)*10%10)

        for Bead in Beads:

            os.makedirs('./'+str(pre)+str(f)+'/b_'+str(Bead))

            for Dens in Denss:


                data = import_file('./frac_'+str(Frac)+'/m_'+str(Bead)+'/d_'+str(Dens)+'/final_snapshot.xyz')

                modifier = CentroSymmetryModifier()
                modifier.Mode.Matching

                data.modifiers.append(modifier)

                export_file(data, str(pre)+str(f)+"/b_"+str(Bead)+"/centroSym_1-d_"+str(Dens)+".txt", "txt/table")
                export_file(data, str(pre)+str(f)+"/b_"+str(Bead)+"/centroSym_2-d_"+str(Dens)+".txt", "xyz", columns = ["Particle Identifier", "Centrosymmetry"])
    
    exit()

GenerateData(Frac_range, Beads_range, Dens_range)


