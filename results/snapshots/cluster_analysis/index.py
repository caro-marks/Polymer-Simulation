from ovito.modifiers import ClusterAnalysisModifier, CreateBondsModifier
from ovito.io import import_file, export_file
import os

Beads_range=[x for x in range(10,50,4) if x not in (38,46)] # # # #    monomer's range
Dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
Frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range

def Cut(Fracs, Beads, Denss):

    pre = 'results/snapshots/cluster_analysis/f_'

    for Frac in Fracs:

        f = int((1-Frac)*10%10)

        for Bead in Beads:

            os.makedirs('./'+str(pre)+str(f)+'/b_'+str(Bead)+'/Cut')

            for Dens in Denss:

                data = import_file('./frac_'+str(Frac)+'/m_'+str(Bead)+'/d_'+str(Dens)+'/final_snapshot.xyz')

                modifier = ClusterAnalysisModifier(cutoff = 2.5, sort_by_size = True, compute_com = True)

                data.modifiers.append(modifier)

                export_file(data, str(pre)+str(f)+"/b_"+str(Bead)+"/Cut/d_"+str(Dens)+".txt", "txt/table", key = 'clusters')

def Bond(Fracs, Beads, Denss):

    pre = 'results/snapshots/cluster_analysis/f_'

    for Frac in Fracs:

        f = int((1-Frac)*10%10)

        for Bead in Beads:

            os.makedirs('./'+str(pre)+str(f)+'/b_'+str(Bead)+'/Bond')

            for Dens in Denss:

                data = import_file('./frac_'+str(Frac)+'/m_'+str(Bead)+'/d_'+str(Dens)+'/final_snapshot.xyz')

                modifier = CreateBondsModifier()
                
                data.modifiers.append(modifier)

                main_modifier = ClusterAnalysisModifier()

                data.modifiers.append(main_modifier)

                export_file(data, str(pre)+str(f)+"/b_"+str(Bead)+"/Bond/d_"+str(Dens)+".txt", "txt/table", key = 'clusters')

def GenerateData(fracs, beads, denss):

    Cut(fracs, beads, denss)

    Bond(fracs, beads, denss)
    
    exit()

GenerateData(Frac_range, Beads_range, Dens_range)