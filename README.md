# Event Selections for *Light-Jet* Enriched Samples

This repository contains a Python script for converting a raw root dataset to a light-jet enriched dataset for light-calibration. The script reads events in root-format, filters them based on light-jet criteria (see below) and saves them in numpy/h5 format.

## Code Overview
The code consists of two main parts: Data reading and event selection.

### I. Data Reading

TODO

### II. Event Selection

The main function in the selection script is `select(samples:awk.highlevel.Array) -> awk.highlevel.Array`, which takes an Awkward Array of particle samples as input and returns a subset of events that pass certain selection criteria.

#### Invariant mass calculation of two-lepton system
The selections are based on the invariant mass of two-electron and two-muon systems. The calculation of the invariant mass is based on the 3D momentum components (px,py and pz calculated from transvere momentum pt and angles eta and phi) and energy.

1. **Momentum Components:**
   - Calculate the x, y, and z components of the particle momentum from the transverse momentum $pt_t$ and angles $\eta$ and $\phi$.
     $$px = pt_t * \cos(\phi)$$
     $$py = pt_t * \sin(\phi)$$
     $$pz = pt_t * \sinh(\eta)$$

2. **3D Momentum Magnitude:**
   - Compute the particles' 3D momentum.
     $$pt = \sqrt(px^2 + py^2 + pz^2)$$

3. **Energy Calculation:**
   - Determine the energy of the particle in the 3D space.
     $$e = \sqrt((pt_t * \cosh(\eta))^2 + (511e-3)^2)$$

4. **Invariant Mass Calculation:**
   - Utilize the energy and momentum components to calculate the invariant mass for each event.
     $$m_{ll} = \sum \sqrt(e^2 - pt^2)$$


#### Selections

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
