""" 
loading the selection of raw files
    - .mat files loaded with MNE
    - .json files loaded with json.loads()
 """

from os.path import join
from mne.io import read_raw_fieldtrip
import json

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
    datapath = find_folder.get_onedrive_path("sourcedata")
    datapath = join(datapath, f'sub-{sub}')
    
    data = read_raw_fieldtrip(
        join(datapath, filename),
        info={}, # add info here
        data_name='data',  # name of heading dict/ variable of original MATLAB object
    )
    
    return data


def load_sourceJSON(sub: str, filename: str):

    """
    Reads source JSON file 

    Input:
        - subject = str, e.g. "024"
        - fname = str of filename, e.g. "Report_Json_Session_Report_20221205T134700.json"

    Returns: 
        - data: json.loads() loaded JSON file

    """

    # Error check: 
    # Error if sub str is not exactly 3 letters e.g. 024
    assert len(sub) == 3, f'Subject string ({sub}) INCORRECT' 
    
    # Error if filename doesn´t end with .mat
    assert filename[-5:] == '.json', (
        f'filename no .json INCORRECT extension: {filename}'
    )


    # find the path to the raw_perceive folder of a subject
    datapath = find_folder.get_onedrive_path("sourcedata")
    json_path = join(datapath, f'sub-{sub}') # same path as to perceive files, all in sourcedata folder

    # fname = os.listdir(json_path)[0] # first filename of all JSON files in that folder

    with open(join(json_path, filename), 'r') as f:
        json_object = json.loads(f.read())


    return json_object
        