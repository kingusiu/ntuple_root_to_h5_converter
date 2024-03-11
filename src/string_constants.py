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

# input directory for run 2 mc (signal and background samples)
in_dir_mc_run2 = os.path.join(in_dir_root,'mc20d')

# input directory data run 2 / 2017 (period D)
in_dir_data_run2 = os.path.join(in_dir_root,'dataRun2_daod_ftag2/user.ltoffoli.data17_13T.periodAllYear.physics_Main.PhysCont.D_FTAG2.grp17_v01_p5981.GN2v01_Nom_output.root')


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
sig_ds_ids = {
    'ee' : ['506193', '506194', '506195'],
    'mumu' : ['506196', '506197', '506198'],
    'tautau': ['512198', '512199', '512200']
}

bg_ds_ids = {
    'ttbar' : 410472,
    'zqqzll' : 363356,
    '363358' : 363358,
    '364302' : 364302,
}

