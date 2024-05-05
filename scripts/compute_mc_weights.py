import os
import glob
import numpy as np
import uproot
import sys
sys.path.append('../src/')

import src.string_constants as stco


def compute_mc_weights_forall_dsid():

	sow_dd = {}

	for dsid in stco.ds_ids_all:
	    dsid_path = glob.glob(os.path.join(stco.in_dir_mc,'*'+dsid+'*'))[0]
	    fnames = [os.path.join(dsid_path, ff) for ff in os.listdir(dsid_path)]
	    
	    sow_per_dsid = 0
	    for ff in fnames: # for all files
	        rt = uproot.open(ff)
	        sow_per_dsid += np.array(rt['sumWeights/totalEventsWeighted'], dtype=np.float64).sum() # for all branches in 
	    
	    sow_dd[dsid] = sow_per_dsid

	return sow_dd
