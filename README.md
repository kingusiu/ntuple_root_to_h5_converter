# Generation of Samples for Light-jet and b-jet Calibration

This repository contains a Python script for converting a raw root dataset to a light-jet enriched dataset for light-calibration. The script reads events in root-format, filters them based on light-jet criteria (see below) and saves them in numpy/h5 format.

The code consists of two main parts: Data reading and event selection.

## I. Data Reading

Production Period: Run2, MC20

2 types of samples:
1. Light jets: /eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2/mc20_Run2/Ntuples
2. B-jets: /eos/atlas/unpledged/group-tokyo/users/wojang/qt/wonho_samples_run2

### ad 1. light-jets:

#### Samples

| Option | Choice | Path-suffix |
| --- | ----------- | ----------- |
| SW release | Release 24, GN2 | Rel24_GN2 |
| Period | E ('18)| PeriodE | 
| Process | Z+Jets | ZJets |
| Final state | 2 leptons | see decay table below|
| Generator | Madgraph | MG |

#### Decays

| Z Decays | B Filter | CFilterBVeto | CVetoBVeto |
| --- | -------- | -------- | -------- | 
| Z-ee |  506193 | 506194 | 506195 |
| Z-mumu |  506196 | 506197 | 506198 |
| Z-tautau |  512198 | 512199 | 512200 |

For example, reading a file of Run2 Madgraph MC for b-triggered Z+jet events decaying to two electrons:

`'/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2/mc20_Run2/Ntuples/PeriodE/ZJets_MG/user.ltoffoli.mc20_13TeV.506193.MGPy8EG_3jets_HT2bias_BFilter.deriv.DAOD_PHYS.e8382_s3681_r13145_p5631.toffoGN2_v1_output.root'
`


### ad 2. B-jets:

Process: 410472 (???)

## II. Kinematics Calculations

### Invariant mass calculation of two-lepton system
The selections are based on the invariant mass of two-electron and two-muon systems. The calculation of the invariant mass is based on the x,y,z momentum components ($px$, $py$ and $pz$ calculated from transvere momentum $pt$ and angles $\eta$ and $\phi$) and energy.

1. **Momentum Components:**
   - Calculate the x, y, and z components of each lepton's momentum from the transverse momentum $pt$ and angles $\eta$ and $\phi$.
     $$px = pt * \cos(\phi)$$
     $$py = pt * \sin(\phi)$$
     $$pz = pt * \sinh(\eta)$$

2. **Dilepton Momentum**
   - Sum over both leptons
   $$\vec{p} = \[px \\ py \\ pz\]$$
   $$\vec{p_{ll}} = \sum_l \vec{p_l}$$

2. **Momentum Magnitude:**
   - Compute the momentum of the system as dot product.
     $$mom2 = \vec{p_{ll}} \cdot \vec{p_{ll}}$$

3. **Energy Calculation:**
   - Determine the energy of the particle in the 3D space.
     $$enrg = \sqrt((pt * \cosh(\eta))^2 + part_m^2)$$
     where part_m is the particle mass (511e-3 MeV for the electron, 105.7MeV for the muon)

4. **Invariant Mass Calculation:**
   - Utilize the energy and momentum components to calculate the invariant mass for each event.
     $$m_{ll} = \sum \sqrt(enrg^2 - mom2)$$


### Transverse momentum calculation of two-lepton system
The selections are based on the transverse momentum of two-electron and two-muon systems. The calculation of the transverse momentum is based on the x and y momentum components ($px$, $py$ calculated from transvere momentum $pt$ and angles $\eta$ and $\phi$).

1. **Momentum Components:**
   - Calculate the x, y, components of each lepton's momentum from the transverse momentum $pt$ and angles $\eta$ and $\phi$.
     $$px = pt * \cos(\phi)$$
     $$py = pt * \sin(\phi)$$

2. **Dilepton Momentum**
   - Sum over both leptons
   $$\vec{p} = \[px \\ py]$$
   $$\vec{p_{ll}} = \sum_l \vec{p_l}$$

3. **Transverse Momentum:**
     $$pt_{ll} = \sqrt(\vec{p_{ll}} \cdot \vec{p_{ll}})$$

## II. Event Selection

The main function in the selection script is `select(samples:awk.highlevel.Array) -> awk.highlevel.Array`, which takes an Awkward Array of particle samples as input and returns a subset of events that pass certain selection criteria.


The selections are:

1. **Z Invariant Mass Windows: $m_{ll}$ (electron or muon system) $\in$ 80-100 GeV**
   - Applies invariant mass windows (80-100 GeV) to the electron- (`mask_ee_m`) resp. muon-system (`mask_mumu_m`) to select Z candidates.

2. **Z transverse Momentum: $pt_{ll}$ (electron or muon system) > 50 GeV**
   - Selects events with di-lepton transverse momentum above 50 GeV of the electron- (`mask_ee_pt`) resp. muon-system (`mask_mumu_pt`) because of mismodeling issues below this value.

3. **Lepton Charge and Multiplicity: Exactly two leptons of same flavor and opposite charge**
   - Selects events with exactly two electrons of opposite charge (`mask_ee`) or two muons of opposite charge (`mask_mumu`).
   - Excludes events with four leptons (`mask_4l`).

4. **Jet Multiplicity:**
   - Requires at least one jet in the event (`awk.num(samples['jet_e']) >= 1`).

5. **Final Selection:**
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
