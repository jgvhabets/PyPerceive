""" loading the selection of matfiles with MNE """

from os.path import join
from mne.io import read_raw_fieldtrip

import PerceiveImport.methods.find_folders as find_folder



# this function loads files from a uniform path 
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
    assert len(sub) == 3, f'Subject string ({sub}) INCORRECT'
    assert filename[-4:] == '.mat', (
        f'filename no .mat INCORRECT extension: {filename}'
    )

    datapath = find_folder.get_onedrive_path("perceivedata")
    datapath = join(datapath, f'sub-{sub}', 'raw_perceive')
    
    data = read_raw_fieldtrip(
        join(datapath, filename),
        info={},
        data_name='data',  # name of heading dict/ variable of original MATLAB object
    )
    # use mne get_data() to actually load data
    
    return data
        