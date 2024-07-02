import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import awkward as awk
import os
import numpy as np
import pandas as pd
import argparse
import h5py
import gc
import mplhep as hep
import heplot as hepl
from heputl import logging as heplog
from heplot.string_constants import histo_palette as hepl_palette 

import src.reader as read
import src.generator as gene
import src.selection as sele
import src.string_constants as stco
import src.util as util


logger = heplog.get_logger(__name__)


def get_min(vals_mc:list[pd.Series],vals_dat:pd.Series) -> float:

    return min(min(v.min() for v in vals_mc),vals_dat.min())

def get_max(vals_mc:list[pd.Series],vals_dat:pd.Series) -> float:

    return max(max(v.max() for v in vals_mc),vals_dat.max())


def plot_ratio_hist(vals_mc:list[pd.Series],vals_dat:pd.Series,weights:list[pd.Series],labels=list[str],val_max:float=None,\
                    xlabel:str='x',plot_name:str='ratio_hist') -> None:

    # set plotting params

    # Load CMS style sheet
    #plt.style.use(hep.style.CMS)

    fig_dir = os.path.join(stco.results_dir_fig,'hist')
    logger.info(f'plotting mc vs data histogram to {fig_dir}')
    binN = 100

    val_max = val_max or get_max(vals_mc=vals_mc,vals_dat=vals_dat)
    val_min = get_min(vals_mc=vals_mc, vals_dat=vals_dat)

    # get data bin heights
    dat_n,bins,patches = plt.hist(vals_dat,bins=binN,range=(val_min,val_max))

    fig, (ax1, ax2) = plt.subplots(2,1,figsize=(7,7), gridspec_kw={'height_ratios': [3, 1]})

    mc_ns, bins, _ = ax1.hist(vals_mc, weights=weights, stacked=True, label=labels, bins=bins, color=hepl_palette, range=(val_min,val_max))
    ax1.scatter(bins[:-1]+ 0.5*(bins[1:] - bins[:-1]), dat_n, marker='o', c='black', s=4, alpha=1, label='data')
    ax1.legend(frameon=False)
    # import ipdb; ipdb.set_trace()
    ratio = np.divide(mc_ns[-1],dat_n,out=np.zeros_like(dat_n), where=dat_n!=0)
    honolulu = '#E54F6D'
    ax2.scatter(bins[:-1], ratio, color=honolulu, s=4)
    ax2.set_xlabel(xlabel)
    ax1.set_ylabel('density')
    ax2.set_ylabel("Ratio \n (mc/data)")
    ax2.axhline(y=1., color='k', linestyle='-')
    ax1.set_xticklabels([])
    plt.tight_layout()

    fig.savefig(os.path.join(fig_dir, plot_name+'.png'), bbox_inches='tight')



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='read arguments for histogramming')
    tt = parser.add_argument('-n', dest='N', default=None, type=int, help='number of samples to be read for each datatype')
    parser.add_argument('-f', dest='feat', choices=['pt','eta','pu','pb','pc'], help='feature to plot')
    args = parser.parse_args()


    # *********************************************************** #
    #                    read MC & data                           #
    # *********************************************************** #

    feat_dd = {
        'pt' : {'name':'jet_pt_lead', 'xlabel': 'jet pt [GeV]', 'max':300},
        'eta' : {'name':'jet_eta_lead','xlabel': 'jet eta','max': None},
        'pu' : {'name':'jet_GN2_pu_lead','xlabel': 'pu','max': None},
        'pb' : {'name':'jet_GN2_pb_lead','xlabel': 'pb','max': None},
        'pc' : {'name':'jet_GN2_pc_lead','xlabel': 'pc','max': None},
    }

    feat_name = feat_dd[args.feat]['name']
    xlabel = feat_dd[args.feat]['xlabel']
    val_max = feat_dd[args.feat]['max']
    feature_names = [feat_name, stco.JET_TRUTH+'_lead', 'wt', 'dsid']

    #***************************** MC *************************** #

    # background
    logger.info('reading MC background')
    df = read.read_selected('bg',feature_names=feature_names, N=args.N)
    # import ipdb; ipdb.set_trace()
    ttb, zz, wz = util.split_into_ttbar_zz_wz(df) # ttb, zz, wz
    logger.info(f'mc background read: {len(ttb)} ttbar, {len(zz)} zz and {len(wz)} wz samples')
    gc.collect()

    # signal
    logger.info('reading MC signal')
    df = read.read_selected('sig',feature_names=feature_names, N=args.N)
    jetU, jetC, jetB, jetT = util.split_by_jet_flavor(df)
    logger.info(f'mc signal read: {len(jetU)} light, {len(jetC)} charm, {len(jetB)} B and {len(jetT)} tau jet samples')
    gc.collect()

    #***************************** data ************************** #

    logger.info('reading data')
    dat = read.read_selected('dat',feature_names=feature_names[:-3], N=args.N)
    logger.info(f'data read: {len(dat)} samples')
    gc.collect()


    # *********************************************************** #
    #           plot stacked histogram MC vs data                 #
    # *********************************************************** #

    # assemble samples to plot

    vals_mc = [ttb[feat_name], zz[feat_name], wz[feat_name], jetU[feat_name], jetC[feat_name], jetB[feat_name], jetT[feat_name]]
    vals_dat = dat[feat_name]
    if 'pt' in feat_name: 
        vals_mc = [v/1e3 for v in vals_mc]
        vals_dat = vals_dat/1e3
    weights = [ttb.wt, zz.wt, wz.wt, jetU.wt, jetC.wt, jetB.wt, jetT.wt]
    labels = ['ttbar', 'zz', 'wz', 'Z + light jet', 'Z + c jet', 'Z + b jet', 'Z + tau jet']

    # plot
    plot_name = 'hist_mc_vs_dat_'+feat_name
    plot_ratio_hist(vals_mc=vals_mc,vals_dat=vals_dat,weights=weights,labels=labels,val_max=val_max,xlabel=xlabel,plot_name=plot_name)

    

