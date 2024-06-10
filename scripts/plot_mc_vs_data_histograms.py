import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import awkward as awk
import os
import pandas as pd
from heputl import logging as heplog

import src.reader as read
import src.generator as gene
import src.selection as sele
import src.string_constants as stco
import src.util as util


logger = heplog.get_logger(__name__)


def read_selected(sample_id:str,feature_names:list[str],N:int=None) -> pd.DataFrame:

    path = os.path.join(stco.out_dir_data_selected,stco.selected_file_names_dd[sample_id])
    df = pd.read_hdf(path,'df')[feature_names]

    return df.iloc[:N] if N else df




if __name__ == '__main__':

    # *********************************************************** #
    #                    read MC & data                           #
    # *********************************************************** #

    N = int(1e3)
    feature_names = ['jet_eta_lead', 'jet_pt_lead', stco.JET_TRUTH, 'wt']

    #***************************** MC *************************** #

    # background
    df = read_mc_from_selected('bg',feature_names=feature_names, N=N)
    ttb, zz, wz = util.split_into_ttbar_zz_wz(df) # ttb, zz, wz
    logger.info(f'mc background read: {len(ttb)} ttb, {len(zz)} zz and {len(wz)} wz samples')

    # signal
    df = read_mc_from_selected('sig',feature_names=feature_names, N=N)
    jetU, jetC, jetB, jetT = util.split_by_jet_flavor(df)
    logger.info(f'mc signal read: {len(jetU)} light, {len(jetC)} charm, {len(jetB)} B and {len(jetT)} tau jet samples')


    #***************************** data ************************** #

    dat = read_mc_from_selected('dat',feature_names=feature_names[:-2], N=N)
    logger.info(f'data read: {len(dat)} samples')


    # *********************************************************** #
    #           plot stacked histogram MC vs data                 #
    # *********************************************************** #

    # assemble samples to plot

    values = [ttb.jet_pt_lead, zz.jet_pt_lead, wz.jet_pt_lead, jetU.jet_pt_lead, jetC.jet_pt_lead, jetB.jet_pt_lead, jetT.jet_pt_lead]
    weights = [ttb.wt, zz.wt, wz.wt, jetU.wt, jetC.wt, jetB.wt, jetT.wt]
    labels = ['ttb', 'zz', 'wz', 'Z + light jet', 'Z + c jet', 'Z + b jet', 'Z + tau jet']

    # set plotting params
    fig_dir = os.path.join(stco.results_dir_fig,'hist')
    logger.info(f'plotting mc vs data histogram to {fig_dir}')
    binN = 100

    # get data bin heights
    dat_n,bins,patches = plt.hist(dat.jet_pt_lead,bins=binN)

    fig = plt.figure()
    _ = plt.hist(values, weights=weights, stacked=True, label=labels, bins=binN)
    plt.scatter(bins[:-1]+ 0.5*(bins[1:] - bins[:-1]), dat_n, marker='o', c='black', s=4, alpha=1)
    plt.legend()
    plt.xlabel('jet pt')
    fig.savefig(os.path.join(fig_dir, 'hist_mc_vs_dat_jet_pt'+'.png'), bbox_inches='tight')

