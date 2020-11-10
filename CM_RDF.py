from ovito.modifiers import CoordinationAnalysisModifier
from ovito.io import import_file, export_file

Beads_range=[x for x in range(10,50,4) if x not in (38,46)] # # # #    monomer's range
Dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
Frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range
inters = ('chain_cm', 'blocos_filicos', 'blocos_fobicos')

def Mods(Fracs, Beads, Denss, Inters):

    for Frac in Fracs:

        frac = int((1-Frac)*10%10)

        print(frac)
        print('')

        for Bead in Beads:

            print(Bead)
            print('')

            for Dens in Denss:
                print(Dens)
                print('')
                
                for Inter in Inters:
                    print(Inter)
                    print('')
        
                    File = f'centros_de_massas/{Inter}/f_{frac}-b_{Bead}-d_{Dens}.xyz'
                    path = f'centros_de_massas/{Inter}/rdfs/f-'

                    data = import_file(File)
                    
                    co = ((Bead*1000)/Dens)**(1/3)
                    
                    modifier = CoordinationAnalysisModifier(cutoff = co/2, number_of_bins = 60)
                    
                    data.modifiers.append(modifier)

                    export_file(data, path+str(frac)+"_b-"+str(Bead)+"_d-"+str(Dens)+".txt", "txt/table")
                    
                    print('Done. Next Inter')
                
                print('Done. Next Dens')

            print('Done. Next Bead')

        print('Done. Next Frac')
    
    print('')
    print('that\'s all, folks!')
            

    exit()


Mods(Frac_range, Beads_range, Dens_range, inters)