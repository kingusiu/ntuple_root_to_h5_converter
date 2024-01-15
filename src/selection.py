import numpy as np
import awkward as awk
from typing import Tuple


def calc_dilepton_px_py_pz(pt:awk.highlevel.Array, eta:awk.highlevel.Array, phi:awk.highlevel.Array) -> Tuple[awk.highlevel.Array]:

	# compute x,y,z momenta of each lepton and sum -> px,py,pz of dilepton system
	px = awk.sum(pt * np.cos(phi),axis=1)
	py = awk.sum(pt * np.sin(phi),axis=1)
	pz = awk.sum(pt * np.sinh(eta),axis=1)

	return px, py, pz


def calc_invariant_mass(pt:awk.highlevel.Array, eta:awk.highlevel.Array, phi:awk.highlevel.Array, part_m:float) -> awk.highlevel.Array:

	px, py, pz = calc_dilepton_px_py_pz(pt, eta, phi)

	# compute momentum and energy of dilepton system
	moment2 = px**2 + py**2 + pz**2
	energy = awk.sum(np.sqrt((pt*np.cosh(eta))**2 + part_m**2),axis=1)

	return np.sqrt(energy**2 - moment2)
	

def calc_dilepton_pt(pt:awk.highlevel.Array, eta:awk.highlevel.Array, phi:awk.highlevel.Array) -> float:

	px, py, pz = calc_dilepton_px_py_pz(pt, eta, phi)

	return np.sqrt(px**2 + py**2)


def select(samples:awk.highlevel.Array) -> awk.highlevel.Array:

	# z mass window [MeV]
	z_m_min, z_m_max = 80e3, 100e3
	# particle masses [MeV]
	ele_m, mu_m = 511e-3, 105.7
	# Z transverse momentum [MeV]
	z_pt_min = 50e3

	# compute invariant mass of electrons
	ee_m = calc_invariant_mass(samples.el_pt, samples.el_eta, samples.el_phi, part_m=ele_m)

	# compute invariant mass of muons
	mumu_m = calc_invariant_mass(samples.mu_pt, samples.mu_eta, samples.mu_phi, part_m=mu_m)

	# invariant mass of electrons 80-100 GeV
	mask_ee_m = (ee_m > z_m_min) & (ee_m < z_m_max)

	# invariant mass of muons 80-100 GeV
	mask_mumu_m = (mumu_m > z_m_min) & (mumu_m < z_m_max)

	# di-electron pt
	mask_ee_pt = calc_dilepton_pt(samples.el_pt, samples.el_eta, samples.el_phi) > z_pt_min

	# di-muon pt
	mask_mumu_pt = calc_dilepton_pt(samples.mu_pt, samples.mu_eta, samples.mu_phi) > z_pt_min

	# exactly two electrons of opposite charge
	mask_ee = (awk.num(samples.el_e) == 2) & (awk.sum(samples.el_charge,axis=1) == 0) 
	
	# exactly two muons of opposite charge
	mask_mumu = (awk.num(samples.mu_e) == 2) & (awk.sum(samples.mu_charge,axis=1) == 0)

	# exclude events with four leptons
	mask_4l = mask_ee & mask_mumu
	mask_ee = mask_ee & ~mask_4l
	mask_mumu = mask_mumu & ~mask_4l

	# electrons in Z invariant mass and transverse momentum window
	mask_ee = mask_ee & mask_ee_m & mask_ee_pt

	# muons in Z invariant mass and transverse momentum window
	mask_mumu = mask_mumu & mask_mumu_m & mask_mumu_pt

	# 2 electrons or 2 muons with Z invariant mass
	mask = mask_ee | mask_mumu

	# at least one jet
	mask = mask & (awk.num(samples.jet_e) >= 1)

	return samples[mask]

