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
| Period | D ('17)| PeriodD |
| MC Campain | mc20 | r13144 |
| Process | Z+Jets | ZJets |
| Final state | 2 leptons | see decay table below|


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

### Leading Jet Augmentation

   find the leading pt jet in each event and add corresponding fields `'jet_pt_lead','jet_truthflav_lead', 'jet_e_lead', 'jet_GN2_pu_lead', 'jet_GN2_pb_lead', 'jet_GN2_pc_lead'`


### Usage

To use this event selection script, you can call the `select` function with your dataset represented as an Awkward Array.

```python
import numpy as np
import awkward as awk

# Load your dataset (replace with actual dataset loading)
samples = ...

# Apply event selection
selected_samples = select(samples)
```

## III Normalisation of MC to the integrated luminosity (MC event weight calculation)

Each MC event is weighted by a weight $w$ computed as

```math
   w = w_\mathrm{evt} \cdot w_\mathrm{dsid}
```

### w_evt: MC weight per event

The event weight is computed as 

```math
   w_\mathrm{evt} = w_{\text{mc}} \times w_{\text{pu}} \times w_{\text{jvt}} \times w_{\text{lSF}}
```

where

> w_mc:
> : The weight associated with Monte Carlo simulations.
>
> w_pu:
> : The weight used to account for pileup effects.
>
> w_jvt:
> : The weight applied based on Jet Vertex Tagger information.
>
> w_lSF:
> : The weight applied based on lepton scale factor information.
>

$w_\mathrm{evt}$ is computed by the function `compute_w_evt(samples:awk.highlevel.Array) -> np.ndarray` of `utils.py`.


### w_dsid: MC weight per DSID
The `dsid` weight $w_\mathrm{dsid}$ is computed as 
```math
w_\mathrm{dsid} = \frac{\mathcal{L} \cdot \sigma}{N_\mathrm{MC}}
```
where 

> - $\mathcal{L}$:
> : The integrated luminosity corresponding to the MC campaign.
> 
> - $\sigma$:
> : The cross-section of the simulated MC process.
> 
> - $N_\mathrm{MC}$:
> : The number of Monte Carlo events.

$w_\mathrm{dsid}$ is computed by the function `compute_w_dsid(dsid:string) -> float` of `utils.py`.

The number of MC events is calculated from all sample files for a dsid as

```math
N_{\text{MC}} = \sum_{\substack{all files i \\ for dsid}} \sum_{\substack{all branches j \\ in file i}} \text{totalEventsWeighted}_{ij}
```
The $N_{\text{MC}}$ values for each dsid are stored in the dictionary `sow_dd` in `string_constants.py`.

The cross section $\sigma$ of the MC process is calculated as the product of the k-factor and the generator cross-section (per dsid)

```math   
   \sigma = k \cdot \sigma_{\mathrm{dsid}}
```
The values for each dsid are stored in the dictionary `scale_factors` in `string_constants.py`.
