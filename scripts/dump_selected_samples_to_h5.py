import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import awkward as awk
import os
import argparse
from heputl import logging as heplog
import gc

import src.reader as read
import src.generator as gene
import src.selection as sele
import src.string_constants as stco
import src.util as util


logger = heplog.get_logger(__name__)


def read_mc(dsids:list[str],features_out:list[str],N:int=None) -> awk.highlevel.Array:

    samples_concat = None

    for dsid in dsids:
        
        samples = read.read_samples_for_dsid(dsid,N=N,filtered=True)
        weights = util.compute_w_samples(samples, dsid)
        samples['dsid'] = dsid
        samples['wt'] = weights

        if samples_concat is None:
            samples_concat = samples[features_out]
        else:    
            samples_concat = awk.concatenate([samples_concat,samples[features_out]])

        del samples
        del weights
        gc.collect()

        logger.info(f'{len(samples_concat)} samples read for dsid {dsid}')

    return samples_concat


def dump(samples:awk.highlevel.Array,file_name:str) -> None:

    # *********************************************************** #
    #           convert to dataframe and dump to h5               #
    # *********************************************************** #

    # convert to dataframe

    df = awk.to_dataframe(samples)

    # dump to h5
    path = os.path.join(stco.out_dir_data_selected,file_name)
    logger.info(f'writing selected samples to {path}')
    df.to_hdf(path,key='df',mode='w')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='read arguments for lightjet dump')
    tt = parser.add_argument('-t', dest='type', choices=['bg','ee','mumu','tautau','dat'], help='type of samples to be read')
    args = parser.parse_args()

    # *********************************************************** #
    #                    read MC & data                           #
    # *********************************************************** #

    N = None
    feat_mc = ['jet_pt_lead','jet_eta_lead','jet_phi_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead', 'jet_truthflavExtended_lead', 'wt', 'dsid']
    feat_dat = ['jet_pt_lead','jet_eta_lead','jet_phi_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead']


    #***************************** data ************************** #

    if args.type == 'dat':
        samples = read.read_data_samples(N,filtered=True)
        samples = samples[feat_dat]
        logger.info(f'data read: {len(samples)} samples')
        dump(samples,stco.selected_file_names_dd[args.type])
        

    #***************************** MC *************************** #

    elif args.type == 'bg' or args.type == 'tautau':
        dsids = list(stco.ds_ids_bg.values()) if args.type == 'bg' else stco.ds_ids_sig[args.type]
        samples = read_mc(dsids=dsids, features_out=feat_mc, N=N)
        logger.info(f'mc {args.type} read: {len(samples)} samples')
        dump(samples,stco.selected_file_names_dd[args.type])


    else: # signals ee, mumu, tautau must be read per dsid because too large

        dsids = stco.ds_ids_sig[args.type]
        
        for dsid in dsids:
        
            samples = read_mc(dsids=[dsid], features_out=feat_mc, N=N)
            logger.info(f'mc {args.type} read: {len(samples)} samples for dsid {dsid}')
        
            file_name = stco.selected_file_names_dd[args.type]
            idx = file_name.index('.h5')
            dump(samples,file_name[:idx]+'_'+dsid+file_name[idx:])
        
            gc.collect()


    


