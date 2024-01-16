import os
import uproot
from typing import List
import awkward as awk

import src.reader as read
import src.selection as sele


def sample_generator(paths:List[str], N:int, feature_names):
    
    samples_concat = None

    for next_chunk in uproot.iterate([pp+'/*.root:nominal' for pp in paths],feature_names):

        #print(len(next_chunk))

        # select lightjets
        selected = sele.select_lightjets(next_chunk)

        if samples_concat is None: 
            samples_concat = selected
        else:
            samples_concat = awk.concatenate([samples_concat,selected])

        while(len(samples_concat) >= N):
            samples_batch = samples_concat[:N]
            samples_concat = samples_concat[N:]
            yield samples_batch

        # if data left, yield it
        if len(samples_concat) > 0:
            yield samples_concat

