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

