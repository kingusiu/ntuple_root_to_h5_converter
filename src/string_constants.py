import os


###     categories    ###
# ----------------------#
# generator - in - data
# generator - out - data

# analysis - out - figures





# *********************************************************** #
#                           IN/OUT DATA                       #
# *********************************************************** #

# ************************* INPUTS ************************** #

# root input directory
in_dir_root = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2v01/Ntuples_Nominal/'

# input directory for run 2 mc 2017 Period D (signal and background samples)
in_dir_mc = os.path.join(in_dir_root,'mc20d')

in_dir_data = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2v01/Ntuples_Nominal/dataRun2_daod_ftag2/'

# ************************* OUTPUTS ************************** #

out_dir_data = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/ucalib'


# *********************************************************** #
#                           OUT FIGURES                       #
# *********************************************************** #

results_fig_dir = 'results/fig'



# *********************************************************** #
#                       LABELS & IDS                          #
# *********************************************************** #

# particle / process dataset IDS
ds_ids_sig = {
    'ee' : ['506193', '506194', '506195'],
    'mumu' : ['506196', '506197', '506198'],
    'tautau': ['512198', '512199', '512200']
}

ds_ids_bg = {
    'ttbar' : 410472,
    'zqqzll' : 363356,
    'wqqzll' : 363358,
    'ggZllZqq' : 364302,
}

JET_U, JET_C, JET_B, JET_T = 0, 4, 5, 15



# *********************************************************** #
#                 XSECS & SCALE FACTORS                       #
# *********************************************************** #

# sample xsec given in picobarn from /cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/AnalysisTop/TopDataPreparation/XSection-MC16-13TeV.data

scale_factors = {
    506193 : {'xsec': 49.38, 'k': 1.}, # [pb]
    506194 : {'xsec': 274.64, 'k': 1.},
    506195 : {'xsec': 1945.68, 'k':1.},
    506196 : {'xsec': 48.66, 'k':1.},
    506197 : {'xsec': 274.37, 'k':1.},
    506198 : {'xsec': 1946.38, 'k':1.},
    512198 : {'xsec': 49.37, 'k':1.},
    512199 : {'xsec': 276.57, 'k':1.},
    512200 : {'xsec': 1943.81, 'k':1.},
    410472 : {'xsec': 76.95, 'k':1.1398},
    363356 : {'xsec': 15.563, 'k':0.13961},
    363358 : {'xsec': 3.437, 'k':1.},
    364302 : {'xsec': 0.1307037636, 'k':1.}, # not found in file, taken from https://gitlab.cern.ch/atlas-ftag-calibration/ljets_ZJet/-/blob/test_MC23_GN2/DoCalibration/HistReader.cxx?ref_type=heads#L617
}

lumi = 44307.4 # [pb] MC 16 period D
