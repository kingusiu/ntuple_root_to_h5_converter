import awkward as awk
import numpy as np
import src.string_constants as stco



def split_by_jet_flavor(samples:awk.highlevel.Array,jet_truth_var:str='jet_truthflav_lead') -> list[awk.highlevel.Array]:
	# *********************************************************** #
	#                 SPLIT SIGNAL BY JET FLAVOR                  #
	# *********************************************************** #
	## split signal samples by jet flavor z+lightjet, z+bjet and z+cjet
	## requires jet_truthflav_lead

	# Z+lightjets
	light_mask = awk.flatten(samples[jet_truth_var] == stco.JET_U)
	ZplusLight = samples[light_mask]

	# Z+c-jets
	charm_mask = awk.flatten(samples[jet_truth_var] == stco.JET_C)
	ZplusC = samples[charm_mask]

	# Z+b-jets
	b_mask = awk.flatten(samples[jet_truth_var] == stco.JET_B)
	ZplusB = samples[b_mask]

	# Z+tau-jets
	tau_mask = awk.flatten(samples[jet_truth_var] == stco.JET_T)
	ZplusTau = samples[tau_mask]

	return [ZplusLight,ZplusC,ZplusB,ZplusTau]


def compute_mc_event_weights(samples:awk.highlevel.Array) -> np.ndarray:

	

	