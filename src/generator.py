import os
import uproot
from typing import List, Callable
import awkward as awk

import src.reader as read
import src.selection as sele


def sample_generator(paths:List[str], N:int, selection_fun:Callable, feature_names_in:List[str] = None, feature_names_out:List[str] = None) -> awk.highlevel.Array:
    """Summary
    
    Args:
        paths (List[str]): list of directories containing root files
        N (int): batch size
        selection_fun (Callable): selections to be applied
        feature_names (List[str]): features to be read
    
    Yields:
        awk.highlevel.Array: N selected events at each iteration
    """

    if type(paths) == str: paths = [paths]
    samples_concat = None

    for next_chunk in uproot.iterate([pp+'/*.root:nominal' for pp in paths],feature_names_in):

        #print(len(next_chunk))

        # select lightjets
        selected = selection_fun(next_chunk)

        if samples_concat is None: 
            samples_concat = selected
        else:
            samples_concat = awk.concatenate([samples_concat,selected])

        while(len(samples_concat) >= N):
            samples_batch = samples_concat[:N]
            samples_concat = samples_concat[N:]
            yield samples_batch[feature_names_out] if feature_names_out else samples_batch

        # if data left, yield it
        if len(samples_concat) > 0:
            yield samples_concat[feature_names_out] if feature_names_out else samples_concat

