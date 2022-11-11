""" Create a Streaming Class """

import os
from dataclasses import dataclass

import PerceiveImport.methods.load_matfiles as loadmat


@dataclass (init=True, repr=True)
class StreamingData:
    """
    BrainSense Streaming Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - files: list of selected Streaming files to load
        - timingfiles: list of selected Streaming files of a specific Follow Up timing

        (manually input ??)
        - Rec_contacts_left: "0-2", "1-3", "0-3" 
        - Rec_contacts_left: "0-2", "1-3", "0-3" 
        - Stim_contact_left: "Ring_0-2", "Ring_1-3", "1a", "1b", "1c", "2a", "2b" ,"2c"
        - Stim_contact_right: "Ring_0-2", "Ring_1-3", "1a", "1b", "1c", "2a", "2b" ,"2c"

        __post_init__
        - allmatfiles: loading all .mat files of the datatype Streaming
        - timingmatfiles: loading the selected .mat files of the chosen timing (Postop, 3MFU, 12MFU, 18MFU, 24MFU) of the datatype Streaming
        - ch_names: channel names
        - n_chan: number of channels
        - n_time_samps: number of samples
        - time_secs: timepoints in seconds
        - sampling_freq: sampling frequency
        - time_duration: duration of the recording
    
    Returns:
        - 
    
    """
    sub: str
    files: list
    timingfiles: list

    # initialized fields
    
    
    
    
    def __post_init__(self,):
        
        self.allmatfiles = loadmat.load_datatypematfiles(self.files)
        self.timingmatfiles = loadmat.load_timingdatatypematfiles(self.files)
        

        
        # ch_names = raw.ch_names
        # n_chan = len(ch_names)
        # n_time_samps = raw.n_times #nsamples
        # time_secs = raw.times #timepoints set to zero
        # ch_trials = raw._data
        # sampling_freq = raw.info['sfreq']
        # time_duration = (n_time_samps/sampling_freq).astype(float)

        
    
    def __str__(self,):
        return f'The Streaming Class will load all selected .mat files.'
    
    # # return for every loaded file:
    # # print(
    # #   f'The data object has:\n\t{n_time_samps} time samples,'
    #   f'\n\tand a sample frequency of {sampling_freq} Hz' 
    #   f'\n\twith a recording duration of {time_duration} seconds.' 
    #   f'\n\t{n_chan} channels were labeled as \n{ch_names}.'
    #   )
    
