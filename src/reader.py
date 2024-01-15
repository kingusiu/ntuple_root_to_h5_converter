"""Summary
"""
import numpy as np
import uproot
import awkward as awk
from typing import List

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
