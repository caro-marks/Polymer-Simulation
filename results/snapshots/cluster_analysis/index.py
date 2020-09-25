from ovito.modifiers import ClusterAnalysisModifier
from ovito.io import import_file, export_file
import os

Beads_range=[x for x in range(10,50,4) if x not in (38,46)] # # # #    monomer's range
Dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
Frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range
pre = 'results/snapshots/rdf/f_'

def Cut(Fracs, Beads, Denss):

    for Frac in Fracs:

        for Bead in Beads:

            os.makedirs('./'+str(pre)+str(int((1-Frac)*10%10))+'/b_'+str(Bead))

            for Dens in Denss:

                data = import_file('./frac_'+str(Frac)+'/m_'+str(Bead)+'/d_'+str(Dens)+'/final_snapshot.xyz')

                for cut in CutOffs:
                    cutter = ClusterAnalysisModifier(cutoff = cut, sort_by_size = True)

                    data.modifiers.append(cutter)

                    export_file(data, str(pre)+str(int((1-Frac)*10%10))+"/b_"+str(Bead)+"/d_"+str(Dens)+".txt", "txt/table", key = 'clusters')

def GenerateData(fracs, beads, denss):

    Cut(fracs, beads, denss)
    
    exit()

GenerateData(Frac_range, Beads_range, Dens_range)