""" Create a Streaming Class """

import os
from dataclasses import dataclass



@dataclass (init=True, repr=True)
class StreamingData:
    """
    BrainSense Streaming Class 
    
    parameters: ???? are defined by loading data in ???
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
    # initialized fields
    
    
    
    
    def __post_init__(self,):
        # run load_matfile method??
        
        # ch_names = raw.ch_names
        # n_chan = len(ch_names)
        # n_time_samps = raw.n_times #nsamples
        # time_secs = raw.times #timepoints set to zero
        # ch_trials = raw._data
        # sampling_freq = raw.info['sfreq']
        # time_duration = (n_time_samps/sampling_freq).astype(float)

        print('streaming functions executing')
    
    # def __str__(self,):
    #     #return f'channel names are {self.ch_names}'
    
    # # return for every loaded file:
    # # print(
    # #   f'The data object has:\n\t{n_time_samps} time samples,'
    #   f'\n\tand a sample frequency of {sampling_freq} Hz' 
    #   f'\n\twith a recording duration of {time_duration} seconds.' 
    #   f'\n\t{n_chan} channels were labeled as \n{ch_names}.'
    #   )
    
