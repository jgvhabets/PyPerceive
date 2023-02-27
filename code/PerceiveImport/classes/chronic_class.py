""" Create a recording modality Class """

from dataclasses import dataclass
import os

import pandas as pd
import warnings

# import own functions
import PerceiveImport.methods.load_rawfile as load_rawfile
from PerceiveImport.methods.ch_renaming import custom_mne_renaming
import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.session_class as sesClass


@dataclass (init=True, repr=True)
class Chronic:
    """
    BrainSense recording modality Class for Chronic Data
    this is a separatae class since its functionality is different
    then the other modalities.
    For Chronic: all available data recorded in all extracted JSON-
    files are combined into one data class. 
    
    parameters:
        - sub: e.g. "021"
        - modality: "survey", "streaming", "timeline", "indefiniteStreaming"
        - metaClass: all original attributes set in Main_Class
        - meta_table: modality selected meta_table set in Main_Class

    Returns:
        - sel_meta_table: session selected meta_table 
    
    """
    sub: str
    metaClass: any
    meta_table: pd.DataFrame
    import_json: bool = False

    def __post_init__(self,):
        
        # suppress RuntimeWarning
        warnings.simplefilter(action='ignore', category=RuntimeWarning)

        matfiles = self.meta_table['perceiveFilename']
        jsonfiles = self.meta_table['report']

        for matfile, jsonfile in zip(matfiles, jsonfiles):

            # print(mfile)

            try:
                # load with mne.read_raw_fieldtrip()
                mne_raw = load_rawfile.load_matfile(self.sub, matfile)
                print(mne_raw)

            except:
                print(f'{matfile} FAILED')
            
            try:
                json_raw = load_rawfile.load_sourceJSON(self.sub, jsonfile)
                print(jsonfile)
            except:
                print(f'{jsonfile} FAILED')
            