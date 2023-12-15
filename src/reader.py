"""Summary
"""
import numpy as np
import uproot
import awkward as awk

class Reader:

    """Sample reader: reads root files, returns numpy arrays
    
    Attributes:
        feature_names (list): the list of 
    """
    
    def __init__(self, feature_names:list):
        """docstring for init
        
        Args:
            feature_names (list): the features to be read for a sample
        """
        self.feature_names = feature_names
        

    def read_file(self, file_path:string) -> awk.highlevel.Array:
        """read features of samples in file
        
        Args:
            file_path (string): full path to file
        
        Returns:
            awk.highlevel.Array: ragged array containing self.feature_names values
        
        """
        tree = uproot.open(file_path+':nominal')

        return tree.arrays(self.feature_names)
