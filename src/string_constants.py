import os
import glob


###     categories    ###
# ----------------------#

# labels/ids

# generator - in - data
# generator - out - data

# analysis - out - figures



# *********************************************************** #
#                MC LABELS, IDS & features                    #
# *********************************************************** #

# particle / process dataset IDS
ds_ids_sig = {
    'ee' : ['506193', '506194', '506195'], #['506194', '506195'],
    'mumu' : ['506196', '506197', '506198'],
    'tautau': ['512198', '512199', '512200']
}

ds_ids_bg = {
    'ttbar' : '410472',
    'zqqzll' : '363356',
    'wqqzll' : '363358',
    'ggZllZqq' : '364302',
}


ds_ids_all = list(ds_ids_bg.values()) + sum(list(ds_ids_sig.values()),[])

JET_U, JET_C, JET_B, JET_T = 0, 4, 5, 15
JET_TRUTH = 'jet_truthflavExtended'

feature_names = ['el_e','mu_e','el_charge','mu_charge','el_pt','mu_pt', 'el_phi','mu_phi', 'el_eta', 'mu_eta', \
                    'jet_e', 'jet_eta', 'jet_phi', 'jet_pt', 'jet_GN2_pu', 'jet_GN2_pb', 'jet_GN2_pc', JET_TRUTH,\
                    'weight_mc', 'weight_pileup', 'weight_jvt', 'weight_leptonSF']

feature_names_dat = feature_names[:-5] # no truth or weight features


# *********************************************************** #
#                           IN/OUT DATA                       #
# *********************************************************** #

# ************************* INPUTS ************************** #

# root input directory
in_dir_root = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2v01/Ntuples_Nominal/'

# input directory for run 2 mc 2017 Period D (signal and background samples)
in_dir_mc = os.path.join(in_dir_root,'mc20d')

in_dir_data = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2v01/Ntuples_Nominal/dataRun2_daod_ftag2/user.ltoffoli.data17_13T.periodAllYear.physics_Main.PhysCont.D_FTAG2.grp17_v01_p5981.GN2v01_Nom_output.root'

dsid_root_dir_dd = {dsid : glob.glob(os.path.join(in_dir_mc,'*'+dsid+'*'))[0] for dsid in ds_ids_all}

# ************************* OUTPUTS ************************** #

out_dir_data = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/ucalib'
out_dir_data_selected = os.path.join(out_dir_data,'selected_lightjets')

selected_file_names_dd = {
    'bg' : 'mc_bg.h5',
    'sig' : 'mc_sig.h5',
    'ee' : 'mc_ee.h5',
    'mumu' : 'mc_mumu.h5',
    'tautau' : 'mc_tautau.h5',
    'dat' : 'data.h5'
}


# *********************************************************** #
#                           OUT FIGURES                       #
# *********************************************************** #

results_dir_fig = 'results/fig'


# *********************************************************** #
#                PHYSICS & LHC CONSTANTS                      #
# *********************************************************** #

lumi = 44307.4 # [pb] MC 16 period D

# particle masses
ele_m = 511e-3 
mu_m = 105.7


# *********************************************************** #
#                 XSECS & SCALE FACTORS                       #
# *********************************************************** #

# sample xsec given in picobarn from /cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/AnalysisTop/TopDataPreparation/XSection-MC16-13TeV.data

scale_factors = {
    '506193' : {'xsec': 49.38, 'k': 1.}, # [pb]
    '506194' : {'xsec': 274.64, 'k': 1.},
    '506195' : {'xsec': 1945.68, 'k':1.},
    '506196' : {'xsec': 48.66, 'k':1.},
    '506197' : {'xsec': 274.37, 'k':1.},
    '506198' : {'xsec': 1946.38, 'k':1.},
    '512198' : {'xsec': 49.37, 'k':1.},
    '512199' : {'xsec': 276.57, 'k':1.},
    '512200' : {'xsec': 1943.81, 'k':1.},
    '410472' : {'xsec': 76.95, 'k':1.1398},
    '363356' : {'xsec': 15.563, 'k':0.13961},
    '363358' : {'xsec': 3.437, 'k':1.},
    '364302' : {'xsec': 0.1307037636, 'k':1.}, # not found in file, taken from https://gitlab.cern.ch/atlas-ftag-calibration/ljets_ZJet/-/blob/test_MC23_GN2/DoCalibration/HistReader.cxx?ref_type=heads#L617
}



## sum of weights for each mc dsid (sum over all weights in all files belonging to a given dsid)
sow_dd = {
    '506196' : 83903746624.0,
    '410472' : 101069830504.0,
    '363356' : 6949688.5625,
    '363358' : 2021873.654296875,
    '364302' : 638141.81640625,
    '506193' : 72501813184.0,
    '506194' : 532006530368.0,
    '506195' : 2068729490176.0,
    '506197' : 438336549632.0,
    '506198' : 2138878821504.0,
    '512198' : 60103329024.0,
    '512199' : 522860189264.0,
    '512200' : 2332324618176.0,
}


mc_lumi_dd = {dsid : lumi * (scale_factors[dsid]['xsec'] * scale_factors[dsid]['k']) / sow_dd[dsid] for dsid in ds_ids_all}


