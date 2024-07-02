"""Summary
"""
import numpy as np
import uproot
import awkward as awk
import glob
import os
import gc
import h5py
import pandas as pd
from typing import List

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heputl import logging as heplog

import src.selection as sele
import src.string_constants as stco
import src.generator as gene


logger = heplog.get_logger(__name__)


def read_samples_from_file(file_path:str, feature_names:List[str]) -> awk.highlevel.Array:
    """read features of samples in file
    
    Args:
        file_path (str): full path to file
        feature_names (list): list of feature names to be read
    
    Returns:
        awk.highlevel.Array: ragged array containing self.feature_names values
    
    """
    tree = uproot.open(file_path+':nominal')

    return tree.arrays(feature_names)


def read_concatenate_samples(file_paths:list[str], feature_names_from_file:list[str], N:int=None, filtered=False) -> awk.highlevel.Array:

    samples_concat = None

    for file_path in file_paths:

        try:

            samples = read_samples_from_file(file_path, feature_names=feature_names_from_file)
            samples_to_concat = sele.select_lightjets(samples) if filtered else samples
            
            if samples_concat is None:
                samples_concat = samples_to_concat
            else:
                samples_concat = awk.concatenate([samples_concat,samples_to_concat])

            if N and len(samples_concat) >= N:
                return samples_concat[:N]

        except Exception as exc:

            logger.warning(f'caught exception while reading file: {exc}')

        del samples
        del samples_to_concat
        gc.collect()


    return samples_concat[:N]



def read_samples_for_dsid(dsid:str, N:int=None, filtered=False) -> awk.highlevel.Array:

    dsid_root_dir = glob.glob(os.path.join(stco.in_dir_mc,'*'+dsid+'*'))[0]
    file_paths = [os.path.join(dsid_root_dir, ff) for ff in os.listdir(dsid_root_dir)]

    logger.info(f'reading samples for dsid {dsid} from {dsid_root_dir}')

    return read_concatenate_samples(file_paths,feature_names_from_file=stco.feature_names,N=N,filtered=filtered)


def read_data_samples(N:int=None, filtered=False) -> awk.highlevel.Array:

    file_paths = [os.path.join(stco.in_dir_data, ff) for ff in os.listdir(stco.in_dir_data)]

    logger.info(f'reading data samples from {stco.in_dir_data}')

    return read_concatenate_samples(file_paths,feature_names_from_file=stco.feature_names_dat,N=N,filtered=filtered)


def read_selected(sample_id:str,feature_names:list[str],N:int=None) -> pd.DataFrame:
    """read selected samples from dump
    
    Args:
        sample_id (str): sample id
        feature_names (list[str]): features to be read
        N (int, optional): limit number
    
    Returns:
        pd.DataFrame: N samples for id sample_id with features feature_names
    """
    path = os.path.join(stco.out_dir_data_selected,stco.selected_file_names_dd[sample_id])
    ff = h5py.File(path, 'r')
    df = pd.DataFrame(np.array(ff['events'][:N][feature_names]))
    if 'dsid' in feature_names: df['dsid'] = df['dsid'].apply(str)

    return df