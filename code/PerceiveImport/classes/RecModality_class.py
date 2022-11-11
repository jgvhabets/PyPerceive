""" Create a Streaming Class """

from dataclasses import dataclass

import PerceiveImport.methods.select_matfiles as matfiles


@dataclass (init=True, repr=True)
class recModality:
    """
    BrainSense Streaming Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - rec_modality: "Streaming", "Survey", "Timeline"

        __post_init__
        - allmatfiles: loading all .mat files of the datatype Streaming
        - timingmatfiles: loading the selected .mat files of the chosen timing (Postop, 3MFU, 12MFU, 18MFU, 24MFU) of the datatype Streaming
        - ch_names: channel names
        - n_chan: number of channels
        - n_time_samps: number of samples
        - time_secs: timepoints in seconds
        - sampling_freq: sampling frequency
        - time_duration: duration of the recording
        - stim_parameters: amplitude, freq, PW
        - stim_contact:
        - Peak_frequency:
    
    Returns:
        - 
    
    """
    sub: str
    rec_modality: str

    # files: list
    # timingfiles: list

    # initialized fields
    
    def __post_init__(self,):
    
        self.recmod_matfilenames, self.recmod_matfilepaths = matfiles.select_matfiles(self.sub, self.rec_modality)
        

        
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
    
