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
in_dir_root = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2v01/mc20_Run2/Ntuples_Nominal/'

# input directory for run 2 mc 2017 Period D (signal and background samples)
in_dir_mc_run2_D = os.path.join(in_dir_root,'PeriodD')

# atm only period D
dir_dict_mc_run2 = {
    
        'sig_mg' : os.path.join(in_dir_mc_run2_D,'MG'), # signal samples by MG 
        'sig_sh' : os.path.join(in_dir_mc_run2_D,'SH'), # signal samples by Sherpa
        'bg' : os.path.join(in_dir_mc_run2_D,'Other'), # background samples: Sherpa diboson and PhPy ttbar dilepton 

}


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

