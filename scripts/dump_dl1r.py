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



def write_dl1r_to_file(df:pd.DataFrame,out_name:str):

    # computing dl1r
    # import ipdb; ipdb.set_trace()
    pu, pb, pc = np.asarray(df['jet_GN2_pu_lead']), np.asarray(df['jet_GN2_pb_lead']), np.asarray(df['jet_GN2_pc_lead'])
    df['dl1r'] = util.compute_dl1r(pu=pu, pb=pb, pc=pc)
    df.drop(['jet_GN2_pu_lead','jet_GN2_pb_lead','jet_GN2_pc_lead'], axis=1, inplace=True)

    # turn to recarray, storing data in same format as root dump and pandas format can not be customized
    if 'dsid' in df.columns:
        df.dsid = pd.to_numeric(df.dsid, errors='coerce').fillna(0).astype(np.int32)
    rec = df.to_records()

    # dump results
    out_path = os.path.join(stco.out_dir_data_selected,out_name)
    logger.info(f'writing sample with features {df.columns} to {out_path}')

    with h5py.File(out_path, 'w') as ff:
        ff.create_dataset('events',data=rec)



if __name__ == '__main__':


    # *********************************************************** #
    #               read data and dump dl1r                       #
    # *********************************************************** #

    feature_names = ['jet_GN2_pu_lead','jet_GN2_pb_lead','jet_GN2_pc_lead', \
                    'jet_pt_lead','jet_eta_lead','wt', 'dsid', stco.JET_TRUTH+'_lead']


    #***************************** MC *************************** #

    # background
    logger.info('reading MC background')
    df = read.read_selected('bg',feature_names=feature_names)
    logger.info(f'mc background read: {len(df)} samples')
    write_dl1r_to_file(df,'mc_bg_dl1r.h5')
    del df; gc.collect()
    


    # signal
    logger.info('reading MC signal')
    df = read.read_selected('sig',feature_names=feature_names)
    logger.info(f'mc signal read: {len(df)} samples')
    write_dl1r_to_file(df,'mc_sig_dl1r.h5')
    del df; gc.collect()

    #***************************** data ************************** #

    logger.info('reading data')
    df = read.read_selected('dat',feature_names=feature_names[:-3])
    logger.info(f'data read: {len(df)} samples')
    logger.info(f'mc signal read: {len(df)} samples')
    write_dl1r_to_file(df,'data_dl1r.h5')
    del df; gc.collect()


