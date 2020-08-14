#### creating polymers for trying modelling Ficoll molecules #########
###################### looking for more patterns #####################
####################### trying other things ##########################

print("\n OK, here we go again! \n")

import espressomd; import numpy as np
from espressomd.interactions import HarmonicBond
from espressomd import polymer#, MDA_ESP
from espressomd.observables import ParticlePositions
from espressomd.accumulators import Correlator
from espressomd.io.writer import vtf
import time
#import MDAnalysis as mda

required_features = ["LENNARD_JONES", "WCA", "EXCLUSIONS"]
espressomd.assert_features(required_features)

################################################################################
#######       loop for diferents densities and monomers quantities       #######
################################################################################

bpc_range= [x for x in range(42,51,4)] # # # #    monomer's range
dens_range=[x/100 for x in range(0,81,5) if x>0] # # # #    dens' range
frac_range=[x/100 for x in range(0,100,25) if x!=0] # # # #    frac' range

n_polymers=1000 # # # #    total polymers
i_box_l=((((bpc_range[0]*n_polymers)/dens_range[0])**(1./3.))-1)*np.ones(3) # # # #    initial box length
system=espressomd.System(box_l=i_box_l, periodicity=[True,True,True])

################################
#####     Interactions     #####
################################

eps = 1.0; sig = 1.0; cut = 2.5 # # # #    non_bonded interaction's variables
hb=HarmonicBond(k=30., r_0=1.); system.bonded_inter.add(hb)
system.non_bonded_inter[0, 0].lennard_jones.set_params(epsilon=.9*eps, sigma=.9*sig, cutoff=cut, shift=0)
system.non_bonded_inter[0, 1].wca.set_params(epsilon=1.2*eps, sigma=1.2*sig)
system.non_bonded_inter[1, 1].wca.set_params(epsilon=1.2*eps, sigma=1.2*sig)

for a in bpc_range:

	configs=open('configurations_of_'+str(a)+'_beads.txt', 'a+')
	configs.write(" Total Particles | Monomers per Polymer | Real Frac Phobic | Density | Average Radius of Gyration | Mean End-To-End Distance of Chains\n")


	for b in dens_range:

		################################################
		#######       Global System objects      #######
		################################################

		n_part=a*n_polymers # # # #    total monomers
		beads_per_chain=a; density=b
		box_v=n_part/density; Box_l = (box_v**(1./3.))*np.ones(3)
		system.change_volume_and_rescale_particles(d_new=Box_l[0])
		#system.thermostat.set_langevin(kT=1, gamma=1, seed=88)
		system.time_step=0.01; system.cell_system.skin= 0.1
		print("The Vol. of Box Simulation is", box_v,"\n")
		
		############################################
		######     initializing polymers     #######
		############################################

		for k in frac_range:

			polymers = polymer.positions(n_polymers=n_polymers, beads_per_chain=beads_per_chain, bond_length=1., seed=88)

			frac_phobic=k
			polymers_list=[]; c=0 ## unnecessary list. creates a list that gonna contains others lists.
			for p in polymers:
				polymers_list.append([x for x in range(c,c + beads_per_chain)]) ## inserts a list(numbered from c to c+beads_per_chain) into polymers_list for each polymer p in polymers
				c+=beads_per_chain
				for i, m in enumerate(p):
					if i<beads_per_chain*frac_phobic:
						id=len(system.part)
						system.part.add(id=id, type=0, pos=m)
						if i > 0:
							system.part[id].add_bond(( hb , id - 1))			
					else:
						id=len(system.part)
						system.part.add(id=id, type=1, pos=m)
						system.part[id].add_bond((hb,id-1))
					
			print("There are ",str(len(system.part[:].id)),"particles\nand the density is ", str(density),"\n")
			print('The simulation has ',str(len(polymers_list)),' polymers, each with ',str(len(polymers_list[0])),' monomers.\n')

			#cs=open('frac_05/m_'+str(beads_per_chain)+'/d_'+str(density)+'/trajectory.vtf', mode='w+t')
			#vtf.writevsf(system,cs)

			#############################################
			#######       exclusion options       #######     
			#############################################

			##### exclude non_bonded interactions between all monomers of each polymer
			exclusions_list_1 = []

			for i in range(len(polymers_list)):
				## for each list in polymers_list, add all the items (but the last)
				j=0
				while j<(len(polymers_list[i])-1):
					exclusions_list_1.append(polymers_list[i][j])
					j+=1

			exclusions_list_2=[]

			g=0
			for h in range(len(polymers_list)):
				## for each item (but the last) at each list in polymers_list, add a list of ids
				i=0
				while i<(len(polymers_list[h])-1):
					exclusions_list_2.append([x for x in polymers_list[h] if x > g])
					i+=1; g+=1
				g+=1

			g=0
			while g<len(exclusions_list_1):
				## exclude all the iterations between each item of exclusion_list_1 and its respective index list in exclusion_list_2
				system.part[exclusions_list_1[g]].exclusions == exclusions_list_2[g]
				g+=1
			
			###############################################
			#####     Warming up the polymers        ######
			###############################################

			eq_steps=100; eq_times=500; wca_cap=1
			system.force_cap = wca_cap
			system.thermostat.set_langevin(kT=0.0, gamma=1.0,seed=88) ##### warmup with zero temperature to remove overlaps

			print("equilibrating... \n")
			for t in range(eq_times):
				print("step {} of {}".format(t,eq_times))
				system.integrator.run(eq_steps)
				system.part[:].v = [0, 0, 0]
				wca_cap = wca_cap * 1.001
				system.force_cap = wca_cap

			print("actual min dist: "+str(system.analysis.min_dist())+"\nfinal cap force: "+str(wca_cap)+"\n")
			##### remove force cap
			wca_cap = 0
			system.force_cap = wca_cap
			print("restoring temp\n")
			##### restore simulation temperature
			system.thermostat.set_langevin(kT=1.0, gamma=1.0, seed=88)
			system.integrator.run(10*eq_steps)
			#vtf.writevcf(system,cs)
			print("Finished equilibration\n")

			##########################################
			#####        Simulating...          ######
			##########################################

			#part_pos = ParticlePositions(ids=range(len(polymers_list)*len(polymers_list[0])))
			
			#msd_corr = Correlator(obs1=part_pos, tau_lin=20, delta_N=5, tau_max=600,corr_operation="square_distance_componentwise",compress1="discard1")
			
			#system.auto_update_accumulators.add(msd_corr)

			avg_Rg = 0

			print("simulating...\n")

			energy=open('frac_'+str(k)+'/m_'+str(beads_per_chain)+'/d_'+str(density)+'/energy.csv', 'w+')		
			energy.write("Step,Total,Kinetic,Bonded,Non-Bonded,Pressure\n")

			s_interval = 1000; s_iterations = 100

			for t in range(s_interval):
				print("step {} of {}".format(t,s_interval))
				system.integrator.run(s_iterations)
				#vtf.writevcf(system, cs)
				Rg=system.analysis.calc_rg(0,n_polymers,beads_per_chain)
				avg_Rg += Rg[0] / s_iterations
				if t%2==0:
					energies=system.analysis.energy(); press=system.analysis.pressure()
					energy.write(str(t)+","+str(energies["total"])+","+str(energies["kinetic"])+","+str(energies["bonded"])+"\
,"+str(energies["non_bonded"])+","+str(press["total"])+"\n")
				
			energy.close()
			print('saving files\n')
			
			#msd_corr.finalize()
			#np.savetxt('m[18-28]/m_'+str(beads_per_chain)+'/msd-d_'+str(density)+'.txt',msd_corr.result())

			print('average Radius of Gyration= ',avg_Rg, 'in reduced units\n')
			print("Final energies:\n"+str(system.analysis.energy())+"\n")
			mlc=system.analysis.calc_re(0,n_polymers,beads_per_chain)
			print("mean end-to-end distance of chains: "+str(mlc[0])+"\n")

			#cs.close()

			final=open('frac_'+str(k)+'/m_'+str(a)+'/d_'+str(b)+'/final_snapshot.xyz','w+')
			final.write(str(len(system.part[:].id))+"\n")
			final.write("type x y z\n")
			z=0
			for p in range(len(polymers_list)):
				for i in range(len(polymers_list[p])):
					final.write(str(system.part[z].type)+' '+str(format((system.part[z].pos[0]),'.3f'))+' '+str(format((system.part[z].pos[1]),'.3f'))+' '+str(format((system.part[z].pos[2]),'.3f'))+'\n')
					z+=1
			final.close()
			
			configs.write(str(len(system.part[:].id))+" | "+str(len(polymers_list[-1]))+"\
| "+str(int(beads_per_chain*(1-frac_phobic)))+" | "+str(density)+" | "+str(avg_Rg)+" | "+str(mlc[0])+"\n")

			if density == dens_range[-1] and frac_phobic == frac_range[-1]:
				print(" __                _    __                              \n\
|_   _   _|    _  (_   (_  .  _      |  _  |_ .  _   _  \n\
|__ | ) (_|   (_) |    __) | ||| |_| | (_| |_ | (_) | ) \n")
			else:
				print("+-+ +-+ +-+ +-+   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+\n\
|N| |e| |x| |t|   |S| |i| |m| |u| |l| |a| |t| |i| |o| |n|\n\
+-+ +-+ +-+ +-+   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+\n")
			system.part.clear()
			#system.auto_update_accumulators.clear()

			time.sleep(60)

configs.close()

print('c u'); exit()
