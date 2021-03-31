from ovito.modifiers import ClusterAnalysisModifier
from ovito.io import import_file
import pandas as pd
import os

Beads_range=[x for x in range(10,50,4) if x not in (38,46)] # # # #    monomer's range
Dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
Frac_range=[abs(1-x/100) for x in range(0,100,25) if x!=0] # # # #    frac' range
Cut_range = [x/100 for x in range(112,130, 2)]

def Cut(Fracs, Beads, Denss, Cut):

    os.makedirs(f'./results/snapshots/cluster_analysis/cuts-phobics/{Cut}')

    for Frac in Fracs:

        print(f'Iniciando frac {Frac}')

        table = pd.DataFrame({'Densities':Denss}).set_index('Densities')

        for Bead in Beads:

            print(f'Iniciando bead {Bead}')

            clusters = []

            for Dens in Denss:

                print(f'Iniciando dens {Dens}')

                cutter = ClusterAnalysisModifier(cutoff = Cut)

                pipeline = import_file(f'./frac_{Frac}/m_{Bead}/d_{Dens}/pb.xyz')

                pipeline.modifiers.append(cutter)

                data = pipeline.compute()

                clusters_table = data.tables['clusters']

                number_of_clusters = len(clusters_table['Cluster Identifier'])

                clusters.append(number_of_clusters)

                print(f'Dens {Dens} finalizado.')
                print('')

            table[Bead] = clusters

            print(f'Bead {Bead} finalizado.')
            print('')

        table.to_csv(f'./results/snapshots/cluster_analysis/cuts-phobics/{Cut}/Frac_{Frac}.csv')

        print(f'Frac {Frac} finalizado.')
        print('')

def GenerateData(fracs, beads, denss, cuts):

    for cut in cuts:

        print(f'Iniciando cut {cut}')

        Cut(fracs, beads, denss, cut)

        print(f'Cut {cut} finalizado.')
        print('')
    
    exit()

GenerateData(Frac_range, Beads_range, Dens_range, Cut_range)