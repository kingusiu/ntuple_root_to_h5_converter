import awkward as awk
import numpy as np
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#sys.path.append('/eos/home-k/kiwoznia/dev/rodem/jettag')
# import ntuple_root_to_h5_converter.src.string_constants as stco
import src.string_constants as stco
import src.selection as sele




def split_by_jet_flavor(samples:awk.highlevel.Array|pd.DataFrame, jet_truth_var:str=stco.JET_TRUTH+'_lead') -> tuple[awk.highlevel.Array|pd.DataFrame]:
	# *********************************************************** #
	#                 SPLIT SIGNAL BY JET FLAVOR                  #
	# *********************************************************** #
	## split signal samples by jet flavor z+lightjet, z+bjet and z+cjet
	## requires jet_truthflav_lead

	# Z+lightjets
	light_mask = samples[jet_truth_var] == stco.JET_U
	ZplusLight = samples[light_mask]

	# Z+c-jets
	charm_mask = (samples[jet_truth_var] == stco.JET_C) | (samples[jet_truth_var] == stco.JET_C_DB) 
	ZplusC = samples[charm_mask]

	# Z+b-jets
	b_mask = (samples[jet_truth_var] == stco.JET_B) | (samples[jet_truth_var] == stco.JET_B_DB) | (samples[jet_truth_var] == stco.JET_BC)
	ZplusB = samples[b_mask]

	# Z+tau-jets
	tau_mask = samples[jet_truth_var] == stco.JET_T
	ZplusTau = samples[tau_mask]

	return [ZplusLight,ZplusC,ZplusB,ZplusTau]


# *********************************************************** #
#     					  MC class 		    			      #
# *********************************************************** #

def split_light_vs_nonlight_jet(samples:awk.highlevel.Array|pd.DataFrame,jet_truth_var:str=stco.JET_TRUTH+'_lead') -> tuple[awk.highlevel.Array|pd.DataFrame]:
	# *********************************************************** #
	#     SPLIT SIGNAL INTO LIGHT and NON-LIGHT JET EVENTS        #
	# *********************************************************** #
	## split signal samples by jet flavor z+lightjet, z+bjet and z+cjet
	## requires jet_truthflav_lead

	# Z+lightjets
	light_mask = samples[jet_truth_var] == stco.JET_U
	samples_light = samples[light_mask]
	samples_non_light = samples[~light_mask]

	return samples_light, samples_non_light


def split_into_ttbar_zz_wz(samples:awk.highlevel.Array|pd.DataFrame) -> tuple[awk.highlevel.Array|pd.DataFrame]:
	"""split samples into ttbar, zz-diboson and wz-diboson events
	
	Args:
	    samples (awk.highlevel.Array): input samples containing 'dsid' field
	
	Returns:
	    tuple[awk.highlevel.Array]: triple of ttbar, zz, wz
	"""
	tt_mask = samples.dsid == '410472'
	zz_mask = (samples.dsid == '363356') | (samples.dsid == '364302') # 'ggZllZqq', 'zqqzll'
	wz_mask = samples.dsid == '363358' # 'wqqzll'

	return samples[tt_mask], samples[zz_mask], samples[wz_mask] 



# *********************************************************** #
#     					MC weighting	    			      #
# *********************************************************** #

def compute_w_evt(samples:awk.highlevel.Array) -> np.ndarray:

	return np.array(samples.weight_mc*samples.weight_pileup*samples.weight_jvt*samples.weight_leptonSF)


def compute_w_dsid(dsid:str) -> float:

	return stco.lumi * (stco.scale_factors[dsid]['xsec'] * stco.scale_factors[dsid]['k']) / stco.sow_dd[dsid]


def compute_w_samples(samples:awk.highlevel.Array, dsid:str) -> awk.highlevel.Array:

	return compute_w_evt(samples) * compute_w_dsid(dsid)



# *********************************************************** #
#     					event observables    			      #
# *********************************************************** #


def compute_dilepton_pt_m(pt, eta, phi, part_m):

	mass = sele.calc_dilepton_mass(pt, eta, phi, part_m=part_m)
	pt_ll = sele.calc_dilepton_pt(pt, eta, phi)

	return mass, pt_ll



def compute_dl1r(pu:np.ndarray, pb:np.ndarray, pc:np.ndarray) -> np.ndarray:

	fc = 0.018
	return np.log(pb) - np.log(fc * pc + (1. - fc) * pu)

