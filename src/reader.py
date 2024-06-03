"""Summary
"""
import numpy as np
import uproot
import awkward as awk
import glob
import os
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


def read_concatenate_samples(file_paths:list[str], feature_names:list[str], N:int=None, filtered=False) -> awk.highlevel.Array:

    samples_concat = None

    for file_path in file_paths:

        if samples_concat is None:
            samples = read_samples_from_file(file_path, feature_names)
            samples_concat = sele.select_lightjets(samples) if filtered else samples
        else:
            samples = read_samples_from_file(file_path, feature_names)
            samples_to_concat = sele.select_lightjets(sample_batch) if filtered else samples
            samples_concat = awk.concatenate([samples_concat,sample_batch])


        if N and len(samples_concat) >= N:
            return samples_concat[:N]

    return samples_concat[:N]



def read_samples_for_dsid(dsid:str, feature_names:List[str]=stco.feature_names, N:int=None, filtered=False) -> awk.highlevel.Array:

    dsid_root_dir = glob.glob(os.path.join(stco.in_dir_mc,'*'+dsid+'*'))[0]
    file_paths = [os.path.join(dsid_root_dir, ff) for ff in os.listdir(dsid_root_dir)]

    logger.info(f'reading samples for dsid {dsid} from {dsid_root_dir}')

    return read_concatenate_samples(file_paths,feature_names,N,filtered)


def read_data_samples(feature_names:List[str]=stco.feature_names, N:int=None, filtered=False) -> awk.highlevel.Array:

    file_paths = [os.path.join(stco.in_dir_data, ff) for ff in os.listdir(stco.in_dir_data)]

    logger.info(f'reading data samples from {dsid_root_dir}')

    return read_concatenate_samples(file_paths,feature_names,N,filtered)