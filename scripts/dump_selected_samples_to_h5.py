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


def read_samples(dsids:list[str],feature_filter:list[str],N:int=None) -> awk.highlevel.Array:

    samples_concat = None

    for dsid in dsids:
        samples = read.read_samples_for_dsid(dsid,N=N)
        selected = sele.select_lightjets(samples)
        weights = util.compute_w_samples(selected, dsid)
        selected['dsid'] = dsid
        selected['wt'] = weights
        if samples_concat is None:
            samples_concat = selected[feature_filter]
        else:    
            samples_concat = awk.concatenate([samples_concat,selected[feature_filter]])

    return samples_concat


def read_mc(dsids:list[str], N:int=None) -> tuple[awk.highlevel.Array]:

    feature_filter = ['jet_pt_lead','jet_eta_lead','dsid','wt']

    samples_concat = read_samples(dsids,feature_filter, N=N)
    
    return util.split_into_ttbar_zz_wz(samples_concat) # ttb, zz, wz


def read_mc_signal(N:int=None) -> tuple[awk.highlevel.Array]:

    dsids = sum(list(stco.ds_ids_sig.values()),[])

    feature_filter=['jet_pt_lead','jet_eta_lead','jet_truthflav_lead', 'wt']

    samples_concat = read_samples(dsids,feature_filter,N=N)

    return util.split_by_jet_flavor(samples_concat)





if __name__ == '__main__':

    # *********************************************************** #
    #                    read MC & data                           #
    # *********************************************************** #

    N = int(1e5)
    feat_mc = ['jet_pt_lead','jet_eta_lead','jet_phi_lead','jet_truthflav_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead', 'wt', 'dsid']
    feat_dat = ['jet_pt_lead','jet_eta_lead','jet_phi_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead']

    #***************************** MC *************************** #

    # background
    dsids = list(stco.ds_ids_bg.values())
    ttb, zz, wz = read_mc(dsids=dsids,N=N)
    logger.info(f'mc background read: {len(ttb)} ttb, {len(zz)} zz and {len(wz)} wz samples')

    # signal

    jetU, jetC, jetB, jetT = read_mc_signal(N)
    logger.info(f'mc signal read: {len(jetU)} light, {len(jetC)} charm, {len(jetB)} B and {len(jetT)} tau jet samples')


    #***************************** data ************************** #

    dat = read.read_data_samples(N)
    logger.info(f'data read: {len(dat)} samples')


    # *********************************************************** #
    #           plot stacked histogram MC vs data                 #
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

