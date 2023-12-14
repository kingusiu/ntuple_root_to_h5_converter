"""Summary
"""
import numpy as np
import uproot
import awkward as ak

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
        

    def read_file(self, file_path:string) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
        """read features of samples in file
        
        Args:
            file_path (string): full path to file
        
        Returns:
            tuple[np.ndarray, np.ndarray, np.ndarray]: a tuple of arrays, each corresponding to a feature of self.feature_names
        """
        ff = uproot.open(file_path)
        tree = ff['nominal;1']
        
        pu = ak.to_numpy(ak.flatten(tree['jet_GN2_pu'].array()))
        pb = ak.to_numpy(ak.flatten(tree['jet_GN2_pb'].array()))
        pc = ak.to_numpy(ak.flatten(tree['jet_GN2_pc'].array()))

        return pu, pb, pc
