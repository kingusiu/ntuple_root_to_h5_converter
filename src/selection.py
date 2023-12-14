import numpy as np


def select(samples):

	mask = np.ones(len(samples), dtype=bool)

	# exactly two leptons
