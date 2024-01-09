# Event Selections for *light-jet* enriched samples

This repository contains a Python script for converting a raw root dataset to a light-jet enriched dataset for light-calibration. The script reads events in root-format, filters them based on light-jet criteria (see below) and saves them in numpy/h5 format.

## Code Overview
The code consists of two main parts: Data reading and event selection.

### Event Selection Criteria

The main function in the selection script is `select(samples:awk.highlevel.Array) -> awk.highlevel.Array`, which takes an Awkward Array of particle samples as input and returns a subset of events that pass certain selection criteria.

The selections are based on invariant mass of two-electron and two-muon systems. The calculation of the invariant mass is based on the 3D momentum components (px,py and pz calculated from transvere momentum pt and angles eta and phi) and energy.

The selections are:

1. **Charge and Multiplicity: 2 Leptons of same flavor and opposite charge**
   - Selects events with exactly two electrons of opposite charge (`mask_ee`) or two muons of opposite charge (`mask_mumu`).
   - Excludes events with four leptons (`mask_4l`).

2. **Z Invariant Mass Windows: ee_m or mumu_m in 80-100 GeV**
   - Applies invariant mass windows (80-100 GeV) to the electron- (`mask_ee_m`) resp. muon-system (`mask_mumu_m`) to select Z candidates.

3. **Jet Multiplicity:**
   - Requires at least one jet in the event (`awk.num(samples['jet_e']) >= 1`).

4. **Final Selection:**
   - Combines all the individual masks to obtain the final selection (`mask`).
   - Applies the selection to the input samples, returning a subset of events.

### Usage

To use this event selection script, you can call the `select` function with your dataset represented as an Awkward Array.

```python
import numpy as np
import awkward as awk

# Load your dataset (replace with actual dataset loading)
samples = ...

# Apply event selection
selected_samples = select(samples)
