import uproot
import h5py
import numpy as np
import os
import awkward as awk
from heplot import plotting as heplt
import glob

import sys
sys.path.append('../src/')

import src.string_constants as stco
import src.reader as read
import src.selection as sele

if __name__ == '__main__':

	feature_names = ['el_e','mu_e','el_charge','mu_charge','el_pt','mu_pt', 'el_phi','mu_phi',\
                      'el_eta', 'mu_eta', 'jet_pt', 'jet_e', 'jet_GN2_pu', 'jet_GN2_pb', 'jet_GN2_pc']

	# *********************************************************** #
	#              		   READ MC (SIG & BG)                     #
	# *********************************************************** #

	## signal (one file per ee, mumu, tautau)
	
	# read electron samples
	path_ee = glob.glob(os.path.join(stco.in_dir_mc,'*'+stco.ds_ids_sig['ee'][0]+'*'))[0]
	fname_ee = os.listdir(path_ee)[3]
	samples_ee = read.read_samples_from_file(os.path.join(path_ee,fname_ee),feature_names)

	# read muon samples
	path_mumu = glob.glob(os.path.join(stco.in_dir_mc,'*'+stco.ds_ids_sig['mumu'][0]+'*'))[0]
	fname_mumu = os.listdir(path_mumu)[3]
	samples_mumu = read.read_samples_from_file(os.path.join(path_mumu,fname_mumu),feature_names)

	# read tau samples
	path_tautau = glob.glob(os.path.join(stco.in_dir_mc,'*'+stco.ds_ids_sig['tautau'][0]+'*'))[0]
	fname_tautau = os.listdir(path_tautau)[3]
	samples_tautau = read.read_samples_from_file(os.path.join(path_tautau,fname_tautau),feature_names)


	samples_sig = awk.concatenate([samples_ee,samples_mumu,samples_tautau])

	# z+jets samples that passed lightjet selection (contains z+light jets, z+b-jets, z+c-jets)
	samples_zplusjets = sele.select_lightjets(samples_sig)

	## background

	# ttbar
	path_ttbar = glob.glob(os.path.join(stco.in_dir_mc,'*'+stco.ds_ids_bg['ttbar'][0]+'*'))[0]
	fname_ttbar = os.listdir(path_ttbar)[3]
	samples_ttbar = read.read_samples_from_file(os.path.join(path_ttbar,fname_ttbar),feature_names)
	
	# zqqzll
	path_zqqzll = glob.glob(os.path.join(stco.in_dir_mc,'*'+stco.ds_ids_bg['zqqzll'][0]+'*'))[0]
	fname_zqqzll = os.listdir(path_zqqzll)[3]
	samples_zqqzll = read.read_samples_from_file(os.path.join(path_zqqzll,fname_zqqzll),feature_names)

	# wqqzll
	path_wqqzll = glob.glob(os.path.join(stco.in_dir_mc,'*'+stco.ds_ids_bg['wqqzll'][0]+'*'))[0]
	fname_wqqzll = os.listdir(path_wqqzll)[3]
	samples_wqqzll = read.read_samples_from_file(os.path.join(path_wqqzll,fname_wqqzll),feature_names)

	# ggZllZqq
	path_ggZllZqq = glob.glob(os.path.join(stco.in_dir_mc,'*'+stco.ds_ids_bg['ggZllZqq'][0]+'*'))[0]
	fname_ggZllZqq = os.listdir(path_ggZllZqq)[3]
	samples_ggZllZqq = read.read_samples_from_file(os.path.join(path_ggZllZqq,fname_ggZllZqq),feature_names)


	samples_zz = awk.concatenate([samples_zqqzll,samples_ggZllZqq])

	# diboson and ttbar samples that passed lightjet selection (contains zw, zz and ttbar)
	samples_ttbar = sele.select_lightjets(samples_ttbar)
	samples_zz = sele.select_lightjets(samples_zz)
	samples_zw = sele.select_lightjets(samples_wqqzll)



	# *********************************************************** #
	#                 SPLIT SIGNAL BY JET FLAVOR                  #
	# *********************************************************** #
	## split signal samples by jet flavor z+lightjet, z+bjet and z+cjet

	# Z+lightjets
	light_mask = awk.flatten(samples_sig.jet_truthflav_lead == stco.JET_U)
	ZplusLight = samples_sig[light_mask]

	# Z+c-jets
	charm_mask = awk.flatten(samples_sig.jet_truthflav_lead == stco.JET_C)
	ZplusC = samples_sig[charm_mask]

	# Z+b-jets
	b_mask = awk.flatten(samples_sig.jet_truthflav_lead == stco.JET_B)
	ZplusB = samples_sig[b_mask]

	# Z+tau-jets
	tau_mask = awk.flatten(samples_sig.jet_truthflav_lead == stco.JET_T)
	ZplusTau = samples_sig[tau_mask]


	# plot as stacked histogram


