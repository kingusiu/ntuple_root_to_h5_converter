import numpy as np
import awkward as awk

def calc_invariant_mass(pt:awk.highlevel.Array, phi:awk.highlevel.Array, eta:awk.highlevel.Array, part_m:float) -> awk.highlevel.Array:

	# compute x,y,z momentum of each lepton and sum -> px,py,pz of dilepton system
	px = ak.sum(pt * np.cos(phi),axis=1)
	py = ak.sum(pt * np.sin(phi),axis=1)
	pz = ak.sum(pt * np.sinh(eta),axis=1)

	moment2 = px**2 + py**2 + pz**2
	energy = ak.sum(np.sqrt((pt*np.cosh(eta))**2 + part_m**2),axis=1)

	return np.sqrt(energy**2 - moment2)
	

def select(samples:awk.highlevel.Array) -> awk.highlevel.Array:

	# z mass window
	z_m_min, z_m_max = 80e3, 100e3.
	# particle masses
	ele_m, mu_m = 511e-3, 105.7

	# compute invariant mass of electrons
	samples['ee_m'] = calc_invariant_mass(samples.el_pt, samples.el_phi, samples.el_eta, part_m=ele_m)

	# compute invariant mass of muons
	samples['mumu_m'] = calc_invariant_mass(samples.mu_pt, samples.mu_phi, samples.mu_eta, part_m=mu_m)

	# invariant mass of electrons 80-100 GeV
	mask_ee_m = samples['ee_m'] > z_m_min & samples['ee_m'] < z_m_max

	# invariant mass of muons 80-100 GeV
	mask_mumu_m = samples['mumu_m'] > z_m_min & samples['mumu_m'] < z_m_max

	# exactly two electrons of opposite charge
	mask_ee = (awk.num(samples['el_e']) == 2) & (ak.sum(samples['el_charge'],axis=1) == 0) 
	
	# exactly two muons of opposite charge
	mask_mumu = (awk.num(samples['mu_e']) == 2) & (ak.sum(samples['mu_charge'],axis=1) == 0)

	# exclude events with four leptons
	mask_4l = mask_ee & mask_mumu

	# electrons in Z invariant mass window
	mask_ee = (mask_ee & mask_ee_m) ^ mask_4l

	# muons in Z invariant mass window
	mask_mumu = (mask_mumu & mask_mumu_m) ^ mask_4l

	# 2 electrons or 2 muons with Z invariant mass
	mask = mask_ee | mask_mumu

	# and at least one jet
	mask = mask & (awk.num(samples['jet_e']) >= 1)

	return samples[mask]

