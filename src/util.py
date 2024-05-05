import awkward as awk
import numpy as np
import sys
sys.path.append('/eos/home-k/kiwoznia/dev/rodem/jettag')
import ntuple_root_to_h5_converter.src.string_constants as stco



def split_by_jet_flavor(samples:awk.highlevel.Array,jet_truth_var:str='jet_truthflav_lead') -> list[awk.highlevel.Array]:
	# *********************************************************** #
	#                 SPLIT SIGNAL BY JET FLAVOR                  #
	# *********************************************************** #
	## split signal samples by jet flavor z+lightjet, z+bjet and z+cjet
	## requires jet_truthflav_lead

	# Z+lightjets
	light_mask = samples[jet_truth_var] == stco.JET_U
	ZplusLight = samples[light_mask]

	# Z+c-jets
	charm_mask = samples[jet_truth_var] == stco.JET_C
	ZplusC = samples[charm_mask]

	# Z+b-jets
	b_mask = samples[jet_truth_var] == stco.JET_B
	ZplusB = samples[b_mask]

	# Z+tau-jets
	tau_mask = samples[jet_truth_var] == stco.JET_T
	ZplusTau = samples[tau_mask]

	return [ZplusLight,ZplusC,ZplusB,ZplusTau]


def split_light_vs_nonlight_jet(samples:awk.highlevel.Array,jet_truth_var:str='jet_truthflav_lead') -> list[awk.highlevel.Array]:
	# *********************************************************** #
	#     SPLIT SIGNAL INTO LIGHT and NON-LIGHT JET EVENTS        #
	# *********************************************************** #
	## split signal samples by jet flavor z+lightjet, z+bjet and z+cjet
	## requires jet_truthflav_lead

	# Z+lightjets
	light_mask = samples[jet_truth_var] == stco.JET_U
	samples_light = samples[light_mask]
	samples_non_light = samples[~light_mask]

	return [samples_light, samples_non_light]


def compute_mc_event_weights(samples:awk.highlevel.Array) -> np.ndarray:

	return np.array(samples.weight_mc*samples.weight_pileup*samples.weight_jvt*samples.weight_leptonSF)

