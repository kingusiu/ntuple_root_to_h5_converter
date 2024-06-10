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
import glob

import src.reader as read
import src.generator as gene
import src.selection as sele
import src.string_constants as stco
import src.util as util



logger = heplog.get_logger(__name__)


def read_and_select_lightjets(file_path:str,feat_in:list[str]=stco.feature_names) -> awk.highlevel.Array:

    samples = read.read_samples_from_file(file_path, feature_names=feat_in)
    samples = sele.select_lightjets(samples)

    return samples


def get_preprocessed_mc_samples_from_file(file_path:str,dsid:str,feat_out:list[str],feat_in:list[str]=stco.feature_names) -> awk.highlevel.Array:

    # import ipdb; ipdb.set_trace()

    samples = read_and_select_lightjets(file_path, feature_names=feat_in)
    weights = util.compute_w_samples(samples, dsid)
    samples['dsid'] = np.int32(dsid)
    samples['wt'] = weights

    return samples[feat_out]



def add_samples_to_file(events:h5py.Dataset,samples:awk.highlevel.Array) -> h5py.Dataset:

    arr = awk.to_numpy(samples)
    n_batch = len(arr)
    events.resize(len(events) + n_batch, axis=0)
    events[-n_batch:] = arr

    return events



def get_file_paths_for_dsid(dsid:str) -> list[str]:
        dsid_root_dir = glob.glob(os.path.join(stco.in_dir_mc,'*'+dsid+'*'))[0]
        return [os.path.join(dsid_root_dir, ff) for ff in os.listdir(dsid_root_dir)]



def write_selected_samples_to_h5_mc(events:h5py.Dataset, dsids:list[str], feat_out:list[str]) -> None:

    n_curr = 0

    for dsid in dsids:
        
        for file_path in get_file_paths_for_dsid(dsid):

            try:
                samples = get_preprocessed_mc_samples_from_file(file_path,dsid,feat_out)
                logger.info(f'adding {len(samples)} samples from {os.path.basename(file_path)} to out-file of length {len(events)}')
                events = add_samples_to_file(events,samples)
                gc.collect()

            except Exception as exc:

                logger.warning(f'caught exception while reading file: {exc}')

        logger.info(f'wrote {len(events-n_curr)} selected samples for dsid {dsid} to {events.file.filename}')
        n_curr = len(events)

    return events


def write_selected_samples_to_h5_data(events:h5py.Dataset, file_paths:list[str], feat_out:list[str], feat_in:list[str]=stco.feature_names_dat) -> None:
        
    for file_path in file_paths:

        try:
            samples = read_and_select_lightjets(file_path,feat_in)
            logger.info(f'adding {len(samples)} samples from {os.path.basename(file_path)} to set of length {len(events)}')
            events = add_samples_to_file(events,samples)
            gc.collect()

        except Exception as exc:

            logger.warning(f'caught exception while reading file: {exc}')

    logger.info(f'wrote {len(events)} selected data samples to {events.file.filename}')

    return events



def get_dtype_for_h5(samples:awk.highlevel.Array) -> np.dtype:

    # set dtype
    field_types = [s._primitive for s in samples.type.content.contents]
    return np.dtype(list(zip(samples.fields,field_types)))
    


def dump_mc_to_h5(dsids:list[str],feat_out:list[str],file_out_path:str,sample_type:str) -> None:

    # read one chunk to get dtype
    samples = get_preprocessed_mc_samples_from_file(get_file_paths_for_dsid(dsids[0])[0],dsid[0],feat_out)
    dtype = get_dtype_for_h5(samples)

    # create file
    with h5py.File(file_out_path, 'w') as outfile:

        outfile.create_dataset("feature_names",data=[f.encode("ascii", "ignore") for f in feat_out],dtype='S10')
        events = outfile.create_dataset("events", shape=(0,), maxshape=(None,), dtype=dtype)

        events = write_selected_samples_to_h5_mc(events, dsids, feat_out)

        logger.info(f'final counts: {len(events)} samples for {sample_type} in {events.file.filename}')


def dump_data_to_h5(file_out_path:str,feat_out:list[str]) -> None:

    file_paths = [os.path.join(stco.in_dir_data, ff) for ff in os.listdir(stco.in_dir_data)]

    # read one file to get dtype for output file
    samples = read_and_select_lightjets(file_paths[0], feature_names=stco.feature_names_dat)
    dtype = get_dtype_for_h5(samples[feat_out])


    with h5py.File(file_out_path, 'w') as outfile:

        # create output file
        outfile.create_dataset("feature_names",data=[f.encode("ascii", "ignore") for f in feat_out],dtype='S10')
        events = outfile.create_dataset("events", shape=(0,), maxshape=(None,), dtype=dtype)

        # populate with events input-file by input-file
        events = write_selected_samples_to_h5_data(events=events, file_paths=file_paths, feat_out=feat_out, feat_in=stco.feature_names_dat)

        logger.info(f'final counts: {len(events)} samples for {sample_type} in {events.file.filename}')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='read arguments for lightjet dump')
    tt = parser.add_argument('-t', dest='type', choices=['dat','bg','ee','mumu','tautau'], help='type of samples to be read')
    args = parser.parse_args()

    # *********************************************************** #
    #          read, select and write samples to h5               #
    # *********************************************************** #

    N = None
    feat_mc = ['jet_pt_lead','jet_eta_lead','jet_phi_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead', 'jet_truthflavExtended_lead', 'wt', 'dsid']
    feat_dat = ['jet_pt_lead','jet_eta_lead','jet_phi_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead']


    #***************************** data ************************** #

    if args.type == 'dat':

        out_path = os.path.join(stco.out_dir_data_selected,stco.selected_file_names_dd[args.type])
        dump_data_to_h5(file_out_path=out_path,feat_out=feat_dat)

        
    #***************************** MC ************************** #

    else:

        dsids = list(stco.ds_ids_bg.values()) if args.type == 'bg' else stco.ds_ids_sig[args.type]
        out_path = os.path.join(stco.out_dir_data_selected,stco.selected_file_names_dd[args.type])
        dump_mc_to_h5(dsids=dsids,feat_out=feat_mc,file_out_path=out_path,sample_type=args.type)        

