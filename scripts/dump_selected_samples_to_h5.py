import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import awkward as awk
import os
from heputl import logging as heplog

import src.reader as read
import src.generator as gene
import src.selection as sele
import src.string_constants as stco
import src.util as util


logger = heplog.get_logger(__name__)


def read_mc(dsids:list[str],feature_filter:list[str],N:int=None) -> awk.highlevel.Array:

    samples_concat = None

    for dsid in dsids:
        samples = read.read_samples_for_dsid(dsid,N=N,filtered=True)
        weights = util.compute_w_samples(samples, dsid)
        samples['dsid'] = dsid
        samples['wt'] = weights
        if samples_concat is None:
            samples_concat = samples[feature_filter]
        else:    
            samples_concat = awk.concatenate([samples_concat,samples[feature_filter]])

    return samples_concat


if __name__ == '__main__':

    # *********************************************************** #
    #                    read MC & data                           #
    # *********************************************************** #

    N = int(1e3)
    feat_mc = ['jet_pt_lead','jet_eta_lead','jet_phi_lead','jet_truthflav_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead', 'wt', 'dsid']
    feat_dat = ['jet_pt_lead','jet_eta_lead','jet_phi_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead']

    #***************************** MC *************************** #

    # background ttb, zz, wz
    dsids = list(stco.ds_ids_bg.values())
    samples_bg = read_mc(dsids=dsids, feature_filter=feat_mc, N=N)
    logger.info(f'mc background read: {len(samples_bg)} samples')

    # signal
    dsids = sum(list(stco.ds_ids_sig.values()),[])
    samples_sig = read_mc(dsids=dsids, feature_filter=feat_mc, N=N)
    logger.info(f'mc signal read: {len(samples_sig)} samples')


    #***************************** data ************************** #

    samples_dat = read.read_data_samples(N,filtered=True)
    samples_dat = samples_dat[feat_dat]
    logger.info(f'data read: {len(samples_dat)} samples')


    # *********************************************************** #
    #           convert to dataframe and dump to h5               #
    # *********************************************************** #

    # assemble samples to plot

    values = [ttb.jet_pt_lead, zz.jet_pt_lead, wz.jet_pt_lead, jetU.jet_pt_lead, jetC.jet_pt_lead, jetB.jet_pt_lead, jetT.jet_pt_lead]
    weights = [ttb.wt, zz.wt, wz.wt, jetU.wt, jetC.wt, jetB.wt, jetT.wt]
    labels = ['ttb', 'zz', 'wz', 'Z + light jet', 'Z + c jet', 'Z + b jet', 'Z + tau jet']

    # set plotting params
    fig_dir = os.path.join(stco.results_fig_dir,'hist')
    logger.info(f'plotting mc vs data histogram to {fig_dir}')
    binN = 100

    # get data bin heights
    dat_n,bins,patches = plt.hist(dat.jet_pt_lead,bins=binN)

    fig = plt.figure()
    _ = plt.hist(values, weights=weights, stacked=True, label=labels, bins=binN)
    plt.scatter(bins[:-1]+ 0.5*(bins[1:] - bins[:-1]), dat_n, marker='o', c='black', s=4, alpha=1)
    plt.legend()
    fig.savefig(os.path.join(fig_dir, 'hist_mc_vs_dat_jet_pt'+'.png'), bbox_inches='tight')

