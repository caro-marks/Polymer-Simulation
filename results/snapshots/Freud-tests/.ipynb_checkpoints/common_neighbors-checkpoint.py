import freud

bpc_range= [x for x in range(42,51,4)] # # # #    monomer's range
dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range

n_polymers=1000 # # # #    total polymers

for a in bpc_range:
    for b in dens_range:
        n_part=a*n_polymers # # # #    total monomers
        beads_per_chain=a; density=b
        box_v=n_part/density
        Box_l = (box_v**(1./3.))
        freud.box.Box.cube(10)