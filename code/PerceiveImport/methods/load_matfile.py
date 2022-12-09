""" loading the selection of matfiles with MNE """

from os.path import join
from mne.io import read_raw_fieldtrip

import PerceiveImport.methods.find_folders as find_folder


def load_matfile(sub: str, filename: str):
    """"
    Reads (perceived) .mat-file in FieldTrip
    structure using mne-function
    
    Input:
        - sub: str code of sub
        - filename: str of only .mat-filename
    
    Returns:
        - data: mne-object of .mat file
    """

    # Error check: 
    # Error if sub str is not exactly 3 letters e.g. 024
    assert len(sub) == 3, f'Subject string ({sub}) INCORRECT' 
    
    # Error if filename doesn´t end with .mat
    assert filename[-4:] == '.mat', (
        f'filename no .mat INCORRECT extension: {filename}'
    )

    # find the path to the raw_perceive folder of a subject
    datapath = find_folder.get_onedrive_path("perceivedata")
    datapath = join(datapath, f'sub-{sub}', 'raw_perceive')
    
    data = read_raw_fieldtrip(
        join(datapath, filename),
        info={}, # add info here
        data_name='data',  # name of heading dict/ variable of original MATLAB object
    )
    # use mne get_data() to actually load data
    
    return data
        