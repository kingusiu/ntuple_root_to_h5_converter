"""Summary
"""
import numpy as np
import uproot
import awkward as awk
import glob
import os
from typing import List

import sys
sys.path.append('../src/')

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


def read_samples_for_dsid(dsid:str, feature_names:List[str]=stco.feature_names, N:int=None) -> awk.highlevel.Array:

    dsid_root_dir = glob.glob(os.path.join(stco.in_dir_mc,'*'+dsid+'*'))[0]
    file_paths = [os.path.join(dsid_root_dir, ff) for ff in os.listdir(dsid_root_dir)]

    print(f'reading samples for dsid {dsid} from {dsid_root_dir}')

    samples_concat = None

    for file_path in file_paths:

        if samples_concat is None:
            samples_concat = read_samples_from_file(file_path, feature_names)
        else:
            sample_batch = read_samples_from_file(file_path, feature_names)
            samples_concat = awk.concatenate([samples_concat,sample_batch])

        if N and len(samples_concat) >= N:
            return samples_concat[:N]

    return samples_concat[:N]


def read_data_samples(N:int=None) -> awk.highlevel.Array:

    N_batch = int(1e3)
    N_total = N
    generator_ee = gene.sample_generator(stco.in_dir_data, N=N_batch, selection_fun=sele.select_lightjets, feature_names_in=stco.feature_names_dat)

    samples_concat = None

    for sample_batch in generator_ee:

        if samples_concat is None:
            samples_concat = sample_batch
        else:
            samples_concat = awk.concatenate([samples_concat,sample_batch])

        if N_total and len(samples_concat) >= N_total:
            break

    logger.info(f'{len(samples_concat)} data samples read')

    return samples_concat
