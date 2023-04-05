""" Create a recording modality Class """

from dataclasses import dataclass
import os
from dataclasses import field
import pandas as pd
from numpy import array
import warnings

# import own functions
import py_perceive.PerceiveImport.methods.load_rawfile as load_rawfile
from py_perceive.PerceiveImport.methods.extract_chronic_timeline_samples import extract_chronic_from_JSON_list



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
    meta_table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    use_json_file: bool = True
    use_mat_file: bool = False
    search_all_jsons: bool = True

    def __post_init__(self,):
        # suppress RuntimeWarning
        warnings.simplefilter(action='ignore', category=RuntimeWarning)

        if self.search_all_jsons:
            json_files = load_rawfile.find_all_present_jsons(self.sub)

        else:
            json_files = self.meta_table['report']

        setattr(self, 'json_files_list', json_files)

        # import json (direct Percept output) if defined
        if self.use_json_file:
            # add content of all jsons
            chronic_df = extract_chronic_from_JSON_list(self.sub, json_files)
            
            setattr(self, 'data', chronic_df)  

        # import mat-file (result of Perceive) if defined
        elif self.use_mat_file:
            mat_files = self.meta_table['perceiveFilename']
            for matfile in mat_files:
                try:
                    # load with mne.read_raw_fieldtrip()
                    mne_raw = load_rawfile.load_matfile(self.sub, matfile)
                    print(mne_raw)

                except:
                    print(f'{matfile} FAILED')


