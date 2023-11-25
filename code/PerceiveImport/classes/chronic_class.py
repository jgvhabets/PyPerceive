""" Create a recording modality Class """

from dataclasses import dataclass
import os
from dataclasses import field
import pandas as pd
from numpy import array
import warnings

# import own functions
import PerceiveImport.methods.load_rawfile as load_rawfile
from PerceiveImport.methods.extract_chronic_timeline_samples import (
    extract_chronic_from_JSON_list
)
from PerceiveImport.methods.timezone_handling import (
    convert_times_to_local
)



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
            chronic_df, snap_list = extract_chronic_from_JSON_list(self.sub, json_files)
            setattr(self, 'data', chronic_df)
            setattr(self, 'events', snap_list)  

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


@dataclass(init=True,)
class singleSnapshotEvent:
    """
    Stores all data for one single actively
    induced snapshot (Ereignis) event
    """
    sub: str
    sensing_settings: list
    json_event_dict: dict
    contains_LFP: bool = False
    LFP_events_key: str = field(
        default_factory=lambda:
        'LfpFrequencySnapshotEvents'
    )
    convert_times_local: bool = True

    def __post_init__(self,):
        self.time = self.json_event_dict['DateTime']
        if self.convert_times_local:
            self.time = convert_times_to_local(self.time)
        self.name = self.json_event_dict['EventName']
        # add neurophys if present
        if self.LFP_events_key in self.json_event_dict.keys():
            self.contains_LFP = True
            # get dict with present hemispheres
            ephys_temp = self.json_event_dict[self.LFP_events_key]
            # loop over hemispheres
            for side in ephys_temp.keys():
                lfp_side = side.split('.')[1].lower()  # get current hemisphere
                lfp_t = ephys_temp[side]['DateTime']  # get time of lfp, is 30 sec's of vs t_event (?)
                if self.convert_times_local:
                    lfp_t = convert_times_to_local(lfp_t)
                setattr(self,
                        f'lfp_{lfp_side}',
                        {'time': lfp_t,
                         'group': ephys_temp[side]['GroupId'],
                         'psd': ephys_temp[side]['FFTBinData'],
                         'freq': ephys_temp[side]['Frequency']})
                
