import numpy as np
import awkward as awk
from typing import Tuple


def calc_dilepton_px_py_pz(pt:awk.highlevel.Array, eta:awk.highlevel.Array, phi:awk.highlevel.Array) -> Tuple[awk.highlevel.Array]:

    # compute x,y,z momenta of each lepton and sum -> px,py,pz of dilepton system
    px = awk.sum(pt * np.cos(phi),axis=1)
    py = awk.sum(pt * np.sin(phi),axis=1)
    pz = awk.sum(pt * np.sinh(eta),axis=1)

    return px, py, pz


def calc_invariant_mass(pt:awk.highlevel.Array, eta:awk.highlevel.Array, phi:awk.highlevel.Array, part_m:float) -> awk.highlevel.Array:

    px, py, pz = calc_dilepton_px_py_pz(pt, eta, phi)

    # compute momentum and energy of dilepton system
    moment2 = px**2 + py**2 + pz**2
    energy = awk.sum(np.sqrt((pt*np.cosh(eta))**2 + part_m**2),axis=1)

    return np.sqrt(energy**2 - moment2)
    

def calc_dilepton_pt(pt:awk.highlevel.Array, eta:awk.highlevel.Array, phi:awk.highlevel.Array) -> float:

    px, py, pz = calc_dilepton_px_py_pz(pt, eta, phi)

    return np.sqrt(px**2 + py**2)


def drop_non_leading_pt_jet_features(samples:awk.highlevel.Array) -> awk.highlevel.Array:

    jet_fields = [field for field in samples.fields if 'jet_' in field]
    leading_jet_mask = awk.argmax(samples['jet_pt'],axis=1,keepdims=True)

    for jet_field in jet_fields:
        samples[jet_field+'_lead'] = samples[jet_field][leading_jet_mask] # cant overwrite fields -> check

    return samples


def select_lightjets(samples:awk.highlevel.Array) -> awk.highlevel.Array:

    # required features: jet_pt, jet_e, el_pt, el_eta, el_phi, el_charge, mu_pt, mu_eta, mu_phi, mu_charge

    # retain leading pt jet
    samples = drop_non_leading_pt_jet_features(samples)

    # z mass window [MeV]
    z_m_min, z_m_max = 80e3, 100e3
    # particle masses [MeV]
    ele_m, mu_m = 511e-3, 105.7
    # Z transverse momentum [MeV]
    z_pt_min = 50e3

    # compute invariant mass of electrons
    ee_m = calc_invariant_mass(samples.el_pt, samples.el_eta, samples.el_phi, part_m=ele_m)

    # compute invariant mass of muons
    mumu_m = calc_invariant_mass(samples.mu_pt, samples.mu_eta, samples.mu_phi, part_m=mu_m)

    # invariant mass of electrons 80-100 GeV
    mask_ee_m = (ee_m > z_m_min) & (ee_m < z_m_max)

    # invariant mass of muons 80-100 GeV
    mask_mumu_m = (mumu_m > z_m_min) & (mumu_m < z_m_max)

    # di-electron pt
    mask_ee_pt = calc_dilepton_pt(samples.el_pt, samples.el_eta, samples.el_phi) > z_pt_min

    # di-muon pt
    mask_mumu_pt = calc_dilepton_pt(samples.mu_pt, samples.mu_eta, samples.mu_phi) > z_pt_min

    # exactly two electrons of opposite charge
    mask_ee = (awk.num(samples.el_e) == 2) & (awk.sum(samples.el_charge,axis=1) == 0) 
    
    # exactly two muons of opposite charge
    mask_mumu = (awk.num(samples.mu_e) == 2) & (awk.sum(samples.mu_charge,axis=1) == 0)

    # exclude events with four leptons
    mask_4l = mask_ee & mask_mumu
    mask_ee = mask_ee & ~mask_4l
    mask_mumu = mask_mumu & ~mask_4l

    # electrons in Z invariant mass and transverse momentum window
    mask_ee = mask_ee & mask_ee_m & mask_ee_pt

    # muons in Z invariant mass and transverse momentum window
    mask_mumu = mask_mumu & mask_mumu_m & mask_mumu_pt

    # 2 electrons or 2 muons with Z invariant mass
    mask = mask_ee | mask_mumu

    # at least one jet
    mask = mask & (awk.num(samples.jet_e) >= 1)

    return samples[mask]



def select_bjets(samples:awk.highlevel.Array) -> awk.highlevel.Array:

    # taken from https://gitlab.cern.ch/atlas-ftag-calibration/ftag-otcalib/-/blob/dump_root_bjet/dumpjets_b_calib.py?ref_type=heads

    ### What we want to save from the jets
    save_var   = ['jet_pt',
                  'jet_eta',
                  'jet_DL1r_pu',
                  'jet_DL1r_pc',
                  'jet_DL1r_pb',
                  'jet_truthflav',
                  'jet_truthflavExtended',
                  'jet_truthPartonLabel',
                  'jet_isTrueHS',
                 ]
    ### Any other variables we want from the event
    meta_var   = ['eventNumber', 'weight_mc']

    fourv_card = ['px', 'py', 'pz', 'e']
    branches = ['el_' + v for v in fourv_card] \
             + ['mu_' + v for v in fourv_card] \
             + ['jet_' + v for v in fourv_card]\
             + save_var + meta_var

    aliases  = {"el_px" : "el_pt*cos(el_phi)",
                "el_py" : "el_pt*sin(el_phi)",
                "el_pz" : "el_pt*sinh(el_eta)", 
                "el_e"  : "sqrt( (el_pt*cosh(el_eta))**2 + (511e-3)**2 )",
                "mu_px" : "mu_pt*cos(mu_phi)",
                "mu_py" : "mu_pt*sin(mu_phi)",
                "mu_pz" : "mu_pt*sinh(mu_eta)", 
                "mu_e"  : "sqrt( (mu_pt*cosh(mu_eta))**2 + (105.7)**2 )",
                "jet_px" : "jet_pt*cos(jet_phi)",
                "jet_py" : "jet_pt*sin(jet_phi)",
                "jet_pz" : "jet_pt*sinh(jet_eta)"
               }

    columns = branches+list(aliases.keys())
    # df = pd.DataFrame(columns=columns)
    current_arrays = []

    print("Starting loop over provided files")
    print(f"\temu = {emu_cut}\n\tmlj = {mljcut_val}")
    for i,batch in enumerate(up.iterate(files_nominal,columns,
                                        step_size=CHUNK_SIZE,
                                        filter_name=branches,aliases=aliases)):
        if i % 10 == 0: 
            print(f"Processed {i*CHUNK_SIZE} events")
        #Check num of jet vector per entry
        twojets = ak.num(batch['jet_e']) == 2
        
        if emu_cut:
            #Check num of electron and muons per entry
            emu = (ak.num(batch['el_e']) == 1) & (ak.num(batch['mu_e']) == 1)
            cut = ak.to_numpy(emu & twojets)
        else:
            cut = ak.to_numpy(twojets)
        
        #load electrons and (thanks to awkwards default record type...) convert to standard numpy array
        el = batch[['el_' + var for var in fourv_card]][cut]
        el = ak.pad_none(el,1,clip=True) #clip to size one in 2nd dim (nelectrons)
        el = np.concatenate([np.expand_dims(ak.to_numpy(el[f'el_{var}']), axis=1) for var in fourv_card],
                            axis=-1)
        
        #load muons and (thanks to awkwards default record type...) convert to standard numpy array
        mu = batch[['mu_' + var for var in fourv_card]][cut]
        mu = ak.pad_none(mu,1,clip=True) #clip to size one in 2nd dim (nmuons)
        mu = np.concatenate([np.expand_dims(ak.to_numpy(mu[f'mu_{var}']), axis=1) for var in fourv_card],
                            axis=-1)
        
        #combine into lepton vector
        lep = np.concatenate([el,mu],axis=1)
        
        #load jets and (thanks to awkwards default record type...) convert to standard numpy array
        jets = batch[['jet_' + var for var in fourv_card]][cut]
        jets = ak.pad_none(jets,2,clip=True) #clip to size two in 2nd dim (njets)
        jets = np.concatenate([np.expand_dims(ak.to_numpy(jets[f'jet_{var}']),-1) for var in fourv_card],
                              axis=-1)
        
        #calculate all possible mlj [[[j1+l1], [j1+l2]], [[j2+l1], [j2+l2]]]
        mlj = (np.expand_dims(lep,1) + np.expand_dims(jets,2))
        #fv = px py pz e, m2 = e2 - p2
        mlj = np.sqrt(mlj[...,-1]**2 - np.sum(mlj[...,:-1]**2, axis=-1))
        
        #swap one of the dimensions for easier sum [[[j1 l1], [j1,l2]], [[j2 l2], [j2,l1]]]
        mlj[:,1] = mlj[:,1,::-1]
        # sum over 1st axis for combinations [(j1l1+j2l2), (j1l2+j2l1)] and get minimum
        # reshape into same shape as mlj tensor for np.take_along_axis
        mlj_lowest_idx = np.tile(np.argmin(np.sum(mlj**2, axis=1),
                                        axis=-1)[::,np.newaxis,np.newaxis],
                                (1,2,1))
        lowest_mlj = np.take_along_axis(mlj,mlj_lowest_idx,axis=-1)
        
        # calculate per jet mlj cut
        mljcut = (lowest_mlj < mljcut_val)
        if req_mlj_both_jets:
            pass_both = np.all(mljcut,axis=1).ravel()
            cut[cut] = pass_both
            mljcut = mljcut[pass_both]


        # select jet variables for events passing event level cuts
        jets_save = batch[save_var][cut]
        jets_save = np.concatenate([np.expand_dims(ak.to_numpy(jets_save[var]),-1) for var in save_var],
                                   axis=-1)
        
        # select event variables for events passing event level cuts
        meta = batch[meta_var][cut]
        meta = np.concatenate([np.expand_dims(ak.to_numpy(meta[var]),-1) for var in meta_var],
                              axis=-1)
        
        # broadcast event vars to jet vars
        tosave = np.concatenate([np.tile(np.expand_dims(meta,1),(1,2,1)),jets_save],
                                axis=-1)
        # flatten to a jet per row shape, apply mlj cut
        tosave = np.reshape(tosave,(-1,tosave.shape[-1]))[np.ravel(mljcut)]

        if numsave+len(tosave) < MAX_PER_FILE:
            current_arrays.append(tosave)
            numsave += len(tosave)
        else:
            filename = f'{output_path}/{output_name}_{numfiles}.h5'
            print(f"Saving {numsave} entries into file: {filename}")
            # Dump into  dataframe, can change format if something else preferable
            df = pd.DataFrame(data=np.concatenate(current_arrays,axis=0),
                              columns=meta_var+save_var)
            df.to_hdf(filename,'jets')
            # Tidy memory by hand, just to be safe
            del df
            for n in current_arrays:
                del n
            current_arrays = []
            current_arrays.append(tosave)
            numsave = 0
            numfiles += 1

    # Save last collection of data
    print(current_arrays[0].shape,np.concatenate(current_arrays,axis=0).shape,len(meta_var+save_var))
    filename = f'{output_path}/{output_name}_{numfiles}.h5'

    print(f"Saving {numsave} entries into file: {filename}\nThis is the last file.")
    df = pd.DataFrame(data=np.concatenate(current_arrays,axis=0),
                      columns=meta_var+save_var,dtype=np.float32)
    df.to_hdf(f'{output_path}/{output_name}_{numfiles}.h5','jets')        


