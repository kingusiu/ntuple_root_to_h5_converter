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



# read MC (signal and background)
# signal (one file per ee, mumu, tautau)
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



# read data


# pass MC through light jet selection


# pass data through light jet selection


# plot as stacked histogram

