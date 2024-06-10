import h5py
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import awkward as awk
import os
import argparse
from heputl import logging as heplog
import gc
import numpy as np

import src.reader as read
import src.generator as gene
import src.selection as sele
import src.string_constants as stco
import src.util as util



logger = heplog.get_logger(__name__)


def read_samples_for_dsid(dsid:str,feat:list[str]) -> awk.highlevel.Array:

    samples = read.read_samples_for_dsid(dsid,N=N,filtered=True)
    weights = util.compute_w_samples(samples, dsid)
    samples['dsid'] = np.int32(dsid)
    samples['wt'] = weights

    return samples[feat]


def add_samples_to_file(events:h5py.File,samples:awk.highlevel.Array) -> h5py.File:

    logger.info(f'adding {len(samples)} samples to file of length {len(events)}')

    arr = awk.to_numpy(samples)
    n_batch = len(arr)
    events.resize(len(events) + n_batch, axis=0)
    events[-n_batch:] = arr

    return events



def write_to_h5(dsids:list[str],features_out:list[str],file_path:str,N:int=None) -> None:

    # read one chunk to get dtype
    samples = read_samples_for_dsid(dsids[0],features_out)

    # set dtype
    field_types = [s._primitive for s in samples.type.content.contents]
    dtype = np.dtype(list(zip(samples.fields,field_types)))

    # create file
    with h5py.File(file_path, 'w') as outfile:

        outfile.create_dataset("feature_names",data=[f.encode("ascii", "ignore") for f in feat_mc],dtype='S10')
        events = outfile.create_dataset("events", shape=(0,), maxshape=(None,), dtype=dtype)

        events = add_samples_to_file(events,samples)

        for dsid in dsids[1:]:

            # read one chunk to get dtype
            samples = read_samples_for_dsid(dsid,features_out)
            events = add_samples_to_file(events,samples)

            gc.collect()

        logger.info(f'wrote {len(events)} selected samples for dsids {dsids} to {file_path}')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='read arguments for lightjet dump')
    tt = parser.add_argument('-t', dest='type', choices=['ee','mumu','tautau'], help='type of samples to be read')
    args = parser.parse_args()

    # *********************************************************** #
    #                 read MC and write to h5                     #
    # *********************************************************** #

    N = None
    feat_mc = ['jet_pt_lead','jet_eta_lead','jet_phi_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead', 'jet_truthflavExtended_lead', 'wt', 'dsid']

    dsids = stco.ds_ids_sig[args.type]
    path = os.path.join(stco.out_dir_data_selected,stco.selected_file_names_dd[args.type])
    write_to_h5(dsids=dsids,features_out=feat_mc,file_path=path,N=N)        

