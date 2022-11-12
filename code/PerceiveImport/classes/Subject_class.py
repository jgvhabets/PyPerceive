""" Create a subject class """


@dataclass (init=True, repr=True)
class subject:
    """
    subject Survey Class 
    
    parameters:
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
    
    # initialized fields
    ch_names
    
    
    def __post_init__(self,):
        print(self.ch_names)
    
    def __str__(self,):
        return f'channel names are {self.ch_names}'


    # ch_names = raw.ch_names
    # n_chan = len(ch_names)
    # n_time_samps = raw.n_times #nsamples        
    # time_secs = raw.times #timepoints set to zero
    # ch_trials = raw._data
    # sampling_freq = raw.info['sfreq']
    # time_duration = (n_time_samps/sampling_freq).astype(float)


     # # return for every loaded file:
    # # print(
    # #   f'The data object has:\n\t{n_time_samps} time samples,'
    #   f'\n\tand a sample frequency of {sampling_freq} Hz' 
    #   f'\n\twith a recording duration of {time_duration} seconds.' 
    #   f'\n\t{n_chan} channels were labeled as \n{ch_names}.'
    #   )