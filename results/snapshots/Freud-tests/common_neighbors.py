import numpy as np
import freud as fd
import networkx as nx

bpc_range = [x for x in range(10,50,4) if x not in (38,46)] # # # #    monomer's range
dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range

pre = 'results/snapshots/cluster_analysis/f_'

for a in bpc_range:
    
    for b in dens_range:
        
        box_L = ((1000*a)/b)**(1./3.)
        
        ##### possibles analysis #####
        
        rdf = fd.density.RDF(bins=200, r_max = box_L//2.)
        
#         r_max = 2
#         diameter = 0.001
#         ld = fd.density.LocalDensity(r_max, diameter)
        
        
        
        
        for c in frac_range:
            
            data = './frac_'+str(c)+'/m_'+str(a)+'/d_'+str(b)+'/final_snapshot.xyz'
            aQ = fd.AABBQuery(box_L, data)
            
            ##### possibles analysis #####
            
            rdf.compute(system = aQ, reset = False)
            
#             random_points = (box_L**3)*b
#             queries = np.random.rand(random_points/10)*L - L/2
#             ld.compute(system=aQ, query_points= queries)