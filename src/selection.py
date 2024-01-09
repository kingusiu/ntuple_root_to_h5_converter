import numpy as np
import awkward as awk

def select(samples:awk.highlevel.Array) -> awk.highlevel.Array:

	# compute invariant mass of electrons
	el_px = samples.el_pt * np.cos(samples.el_phi)
	el_py = samples.el_pt * np.sin(samples.el_phi)
	el_pz = samples.el_pt * np.sinh(samples.el_eta)
	el_pt3d = np.sqrt(el_px**2 + el_py**2 + el_pz**2)
	el_e3d = np.sqrt((samples.el_pt*cosh(samples.el_eta))**2 + (511e-3)**2)
	samples['ee_m'] = awk.sum(np.sqrt(el_e3d**2 - el_pt3d**2),axis=1)

	# compute invariant mass of muons
	mu_px = samples.mu_pt * np.cos(samples.mu_phi)
	mu_py = samples.mu_pt * np.sin(samples.mu_phi)
	mu_pz = samples.mu_pt * np.sinh(samples.mu_eta)
	mu_pt3d = np.sqrt(mu_px**2 + mu_py**2 + mu_pz**2)
	mu_e3d = np.sqrt((samples.mu_pt*cosh(samples.mu_eta))**2 + (511e-3)**2)
	samples['mumu_m'] = awk.sum(np.sqrt(mu_e3d**2 - mu_pt3d**2),axis=1)

	# invariant mass of electrons 80-100 GeV
	mask_ee_m = samples['ee_m'] > 80 & samples['ee_m'] < 100

	# invariant mass of muons 80-100 GeV
	mask_mumu_m = samples['mumu_m'] > 80 & samples['mumu_m'] < 100

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

