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


def compute_dilepton_pt_m_pxpypz(pt, eta, phi, part_m):

	mass = sele.calc_dilepton_mass(pt, eta, phi, part_m=part_m)
	pt_ll = sele.calc_dilepton_pt(pt, eta, phi)
	px, py, pz = sele.calc_dilepton_px_py_pz(pt, eta, phi)

	return mass, pt_ll, px, py, pz



if __name__ == '__main__':

	feature_names = ['el_e','mu_e','el_charge','mu_charge','el_pt','mu_pt', 'el_phi','mu_phi',\
                      'el_eta', 'mu_eta', 'jet_e', 'jet_GN2_pu', 'jet_GN2_pb', 'jet_GN2_pc']
	
	# read b-tagged electron samples
	path_ee = glob.glob(os.path.join(stco.generator_in_dir_lightjet,'*'+stco.ds_ids['ee'][0]+'*'))[0]
	fname_ee = os.listdir(path_ee)[3]
	samples_ee = read.read_samples_from_file(os.path.join(path_ee,fname_ee),feature_names)

	# select electron samples
	samples_selected_ee = sele.select_lightjets(samples_ee)

	# read muon samples
	path_mumu = glob.glob(os.path.join(stco.generator_in_dir_lightjet,'*'+stco.ds_ids['mumu'][0]+'*'))[0]
	fname_mumu = os.listdir(path_mumu)[3]
	samples_mumu = read.read_samples_from_file(os.path.join(path_mumu,fname_mumu),feature_names)

	# select muon samples
	samples_selected_mumu = sele.select_lightjets(samples_mumu)

	# compute dilepton pt, invariant mass, px,py,pz
	
	## compute additional features of electrons
	mass, pt, px, py, pz = compute_dilepton_pt_m_pxpypz(samples_selected_ee.el_pt, samples_selected_ee.el_eta, samples_selected_ee.el_phi, stco.ele_m)
	samples_selected_ee['ee_m'], samples_selected_ee['ee_pt'], samples_selected_ee['ee_px'], samples_selected_ee['ee_py'], samples_selected_ee['ee_pz'] = mass, pt, px, py, pz

	## compute additional features of muons
	mass, pt, px, py, pz = compute_dilepton_pt_m_pxpypz(samples_selected_mumu.mu_pt, samples_selected_mumu.mu_eta, samples_selected_mumu.mu_phi, stco.mu_m)
	samples_selected_mumu['mumu_m'], samples_selected_mumu['mumu_pt'], samples_selected_mumu['mumu_px'], samples_selected_mumu['mumu_py'], samples_selected_mumu['mumu_pz'] = mass, pt, px, py, pz

	# plot distributions

	kine_features_ee = ['el_'+kk for kk in ['e','charge','pt', 'phi','eta']]+ ['jet_e'] + ['ee_'+kk for kk in ['m', 'pt', 'px', 'py', 'pz']]
	kine_features_mumu = ['mu_'+kk for kk in ['e','charge','pt', 'phi','eta']]+ ['jet_e'] + ['mumu_'+kk for kk in ['m', 'pt', 'px', 'py', 'pz']]

	for ff_ee, ff_mumu in zip(kine_features_ee,kine_features_mumu):
	    dd_ee, dd_mumu = samples_selected_ee[ff_ee], samples_selected_mumu[ff_mumu]
	    data = [awk.flatten(dd) if dd.ndim >=2 else dd for dd in [dd_ee,dd_mumu]]
	    sample_names = ['electron','muon']
	    label = ff_ee[3:]+'_l' if ff_ee.startswith('el_') else ff_ee[3:]+'_ll' if ff_ee.startswith('ee_') else ff_ee
	    heplt.plot_feature_for_n_samples(data,sample_names,xlabel=label,plot_name='hist_'+label,fig_dir=stco.results_fig_dir)


	# plot GN2 probability distributions electrons
	ff_names = ['pu','pb','pc']
	data = [awk.flatten(samples_selected_ee[ff]) for ff in ['jet_GN2_pu', 'jet_GN2_pb', 'jet_GN2_pc']]
	heplt.plot_feature_for_n_samples(data,ff_names,xlabel='prob ee',plot_name='hist_gn2_ee',fig_dir=stco.results_fig_dir)

	# plot GN2 probability distributions muons
	data = [awk.flatten(samples_selected_mumu[ff]) for ff in ['jet_GN2_pu', 'jet_GN2_pb', 'jet_GN2_pc']]
	heplt.plot_feature_for_n_samples(data,ff_names,xlabel='prob mumu',plot_name='hist_gn2_mumu',fig_dir=stco.results_fig_dir)
