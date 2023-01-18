""" PEAK Analysis """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import scipy
from scipy.signal import butter, filtfilt, freqz

import sklearn
from sklearn.preprocessing import normalize

import mne

import json
import os

import PerceiveImport.classes.main_class as mainclass
import PerceiveImport.methods.find_folders as findfolders



# mapping = dictionary of all possible channel names as keys, new channel names (Retune standard) as values
mapping = {
    'LFP_Stn_0_3_RIGHT_RING':"LFP_R_03_STN_MT",
    'LFP_Stn_1_3_RIGHT_RING':"LFP_R_13_STN_MT",
    'LFP_Stn_0_2_RIGHT_RING':"LFP_R_02_STN_MT",
    'LFP_Stn_1_2_RIGHT_RING':"LFP_R_12_STN_MT",
    'LFP_Stn_0_1_RIGHT_RING':"LFP_R_01_STN_MT",
    'LFP_Stn_2_3_RIGHT_RING':"LFP_R_23_STN_MT",
    'LFP_Stn_0_3_LEFT_RING':"LFP_L_03_STN_MT",
    'LFP_Stn_1_3_LEFT_RING':"LFP_L_13_STN_MT",
    'LFP_Stn_0_2_LEFT_RING':"LFP_L_02_STN_MT",
    'LFP_Stn_1_2_LEFT_RING':"LFP_L_12_STN_MT",
    'LFP_Stn_0_1_LEFT_RING':"LFP_L_01_STN_MT",
    'LFP_Stn_2_3_LEFT_RING':"LFP_L_23_STN_MT",
    'LFP_Stn_1_A_1_B_RIGHT_SEGMENT':"LFP_R_1A1B_STN_MT",
    'LFP_Stn_1_B_1_C_RIGHT_SEGMENT':"LFP_R_1B1C_STN_MT",
    'LFP_Stn_1_A_1_C_RIGHT_SEGMENT':"LFP_R_1A1C_STN_MT",
    'LFP_Stn_2_A_2_B_RIGHT_SEGMENT':"LFP_R_2A2B_STN_MT",
    'LFP_Stn_2_B_2_C_RIGHT_SEGMENT':"LFP_R_2B2C_STN_MT",
    'LFP_Stn_2_A_2_C_RIGHT_SEGMENT':"LFP_R_2A2C_STN_MT",
    'LFP_Stn_1_A_1_B_LEFT_SEGMENT':"LFP_L_1A1B_STN_MT",
    'LFP_Stn_1_B_1_C_LEFT_SEGMENT':"LFP_L_1B1C_STN_MT",
    'LFP_Stn_1_A_1_C_LEFT_SEGMENT':"LFP_L_1A1C_STN_MT",
    'LFP_Stn_2_A_2_B_LEFT_SEGMENT':"LFP_L_2A2B_STN_MT",
    'LFP_Stn_2_B_2_C_LEFT_SEGMENT':"LFP_L_2B2C_STN_MT",
    'LFP_Stn_2_A_2_C_LEFT_SEGMENT':"LFP_L_2A2C_STN_MT",
    'LFP_Stn_1_A_2_A_RIGHT_SEGMENT':"LFP_R_1A2A_STN_MT",
    'LFP_Stn_1_B_2_B_RIGHT_SEGMENT':"LFP_R_1B2B_STN_MT",
    'LFP_Stn_1_C_2_C_RIGHT_SEGMENT':"LFP_R_1C2C_STN_MT",
    'LFP_Stn_1_A_2_A_LEFT_SEGMENT':"LFP_L_1A2A_STN_MT",
    'LFP_Stn_1_B_2_B_LEFT_SEGMENT':"LFP_L_1B2B_STN_MT",
    'LFP_Stn_1_C_2_C_LEFT_SEGMENT':"LFP_L_1C2C_STN_MT",
    "LFP_Stn_R_03":"LFP_R_03_STN_MT",
    "LFP_Stn_R_13":"LFP_R_13_STN_MT",
    "LFP_Stn_R_02":"LFP_R_02_STN_MT",
    "LFP_Stn_R_12":"LFP_R_12_STN_MT",
    "LFP_Stn_R_01":"LFP_R_01_STN_MT",
    "LFP_Stn_R_23":"LFP_R_23_STN_MT",
    "LFP_Stn_L_03":"LFP_L_03_STN_MT",
    "LFP_Stn_L_13":"LFP_L_13_STN_MT",
    "LFP_Stn_L_02":"LFP_L_02_STN_MT",
    "LFP_Stn_L_12":"LFP_L_12_STN_MT",
    "LFP_Stn_L_01":"LFP_L_01_STN_MT",
    "LFP_Stn_L_23":"LFP_L_23_STN_MT",
    'LFP_Stn_R_1A1B':"LFP_R_1A1B_STN_MT",
    'LFP_Stn_R_1B1C':"LFP_R_1B1C_STN_MT",
    'LFP_Stn_R_1A1C':"LFP_R_1A1C_STN_MT",
    'LFP_Stn_R_2A2B':"LFP_R_2A2B_STN_MT",
    'LFP_Stn_R_2B2C':"LFP_R_2B2C_STN_MT",
    'LFP_Stn_R_2A2C':"LFP_R_2A2C_STN_MT",
    'LFP_Stn_L_1A1B':"LFP_L_1A1B_STN_MT",
    'LFP_Stn_L_1B1C':"LFP_L_1B1C_STN_MT",
    'LFP_Stn_L_1A1C':"LFP_L_1A1C_STN_MT",
    'LFP_Stn_L_2A2B':"LFP_L_2A2B_STN_MT",
    'LFP_Stn_L_2B2C':"LFP_L_2B2C_STN_MT",
    'LFP_Stn_L_2A2C':"LFP_L_2A2C_STN_MT",
    'LFP_Stn_R_1A2A':"LFP_R_1A2A_STN_MT", 
    'LFP_Stn_R_1B2B':"LFP_R_1B2B_STN_MT", 
    'LFP_Stn_R_1C2C':"LFP_R_1C2C_STN_MT",
    'LFP_Stn_L_1A2A':"LFP_L_1A2A_STN_MT", 
    'LFP_Stn_L_1B2B':"LFP_L_1B2B_STN_MT", 
    'LFP_Stn_L_1C2C':"LFP_L_1C2C_STN_MT",
    
}




def welch_normalizedPsdToTotalSum_seperateTimepoints(incl_sub: str, incl_session: list, incl_condition: list, tasks: list, pickChannels: list, hemisphere: str):
    """
    incl_sub = str e.g. "024"
    incl_session = list ["postop", "fu3m", "fu12m", "fu18m", "fu24m"]
    incl_condition = ["m0s0", "m1s0"]
    tasks = list ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
    pickChannels = list  ['03', '13', '02', '12', '01', '23', 
    '1A1B', '1B1C', '1A1C', '2A2B', '2B2C', '2A2C', 
    '1A2A', '1B2B', '1C2C']
    - hemisphere: str e.g. "Right"

    1) load data from mainclass.PerceiveData using the input values.
    
    2) band-pass filter by a Butterworth Filter of fifth order (5-95 Hz).
    
    3) Calculate the psd values of every channel for each timepoint by using Welch's method.

    4) Normalize psd to total sum of each Power Spectrum using sklearn.preprocessing.normalize

    5) For each frequency band alpha (), low beta () and high beta (), the highest Peak values (frequency and psd) will be seleted and saved in a DataFrame.

    6) Save figure: f"\sub{incl_sub}_{hemisphere}_normalizedPsdToTotalSum_seperateTimepoints_{pickChannels}.png"
    
    7) Store Dataframes in dictionary: 
        - All frequencies and relative psd values of each channel
        - for the highest PEAK in each frequency band: 
    
    {"frequenciesDataFrame":frequenciesDataFrame,
    "absolutePsdDataFrame":absolutePsdDataFrame,
    "SEM":sem_dict,
    "highestPEAK": highestPEAKDF,
    }


    """

    sns.set()
    # Matplotlib: set the style
    plt.style.use('seaborn-whitegrid')  

    mainclass_sub = mainclass.PerceiveData(
        sub = incl_sub, 
        incl_modalities= ["survey"],
        incl_session = incl_session,
        incl_condition = incl_condition,
        incl_task = ["rest"]
        )

    local_path = findfolders.get_local_path(folder="figures", sub=incl_sub)

    # add error correction for sub and task
    # tasks = ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
    f_psd_dict = {} # dictionary with tuples of frequency and psd for each channel and timepoint of a subject
    sem_dict = {}
    highest_peak_dict = {}

    # set layout for figures: using the object-oriented interface
    fig, axes = plt.subplots(len(incl_session), 1, figsize=(15, 15)) # subplot(rows, columns, panel number)
    fig.tight_layout(pad=5.0)

    for t, tp in enumerate(incl_session):
        # t is indexing time_points, tp are the time_points
        for c, cond in enumerate(incl_condition):

            for tk, task in enumerate(tasks): 
                # tk is indexing task, task is the input task

                # avoid Attribute Error, continue if attribute doesn´t exist
                if getattr(mainclass_sub.survey, tp) is None:
                    continue

                # apply loop over channels
                temp_data = getattr(mainclass_sub.survey, tp) # gets attribute e.g. of tp "postop" from modality_class with modality set to survey
                
                # avoid Attribute Error, continue if attribute doesn´t exist
                if getattr(temp_data, cond) is None:
                    continue
            
                temp_data = getattr(temp_data, cond) # gets attribute e.g. "m0s0"
                temp_data = temp_data.rest.data[tasks[tk]] # gets the mne loaded data from the perceive .mat BSSu, m0s0 file with task "RestBSSuRingR"
    
            
                #################### CREATE A BUTTERWORTH FILTER ####################

                # set filter parameters for band-pass filter
                filter_order = 5 # in MATLAB spm_eeg_filter default=5 Butterworth
                frequency_cutoff_low = 5 # 5Hz high-pass filter
                frequency_cutoff_high = 95 # 95 Hz low-pass filter
                fs = temp_data.info['sfreq'] # sample frequency: 250 Hz

                # create the filter
                b, a = scipy.signal.butter(filter_order, (frequency_cutoff_low, frequency_cutoff_high), btype='bandpass', output='ba', fs=fs)


                #################### RENAME CHANNELS ####################
                # all channel names of one loaded file (one session, one task)
                ch_names_original = temp_data.info.ch_names

                # select only relevant keys and values from the mapping dictionary to rename channels
                mappingSelected = dict((key, mapping[key]) for key in ch_names_original if key in mapping)

                # rename channels using mne and the new selected mapping dictionary
                mne.rename_channels(info=temp_data.info, mapping=mappingSelected, allow_duplicates=False)

                # get new channel names
                ch_names_renamed = temp_data.info.ch_names


                #################### PICK CHANNELS ####################
                include_channelList = [] # this will be a list with all channel names selected
                exclude_channelList = []

                for n, names in enumerate(ch_names_renamed):
                    
                    # add all channel names that contain the picked channels: e.g. 02, 13, etc given in the input pickChannels
                    for picked in pickChannels:
                        if picked in names:
                            include_channelList.append(names)


                    # exclude all bipolar 0-3 channels, because they do not give much information
                    # if "03" in names:
                    #     exclude_channelList.append(names)
                    
                # Error Checking: 
                if len(include_channelList) == 0:
                    continue

                # pick channels of interest: mne.pick_channels() will output the indices of included channels in an array
                ch_names_indices = mne.pick_channels(ch_names_renamed, include=include_channelList)

                # ch_names = [ch_names_renamed[idx] for idx in ch_names_indices] # new list of picked channel names based on the indeces 
                

                # create signal per channel with Welch´s method and plot
                for i, ch in enumerate(ch_names_renamed):
                    
                    # only get picked channels
                    if i not in ch_names_indices:
                        continue

                    #################### FILTER THE SIGNAL ####################
                    # filter the signal by using the above defined butterworth filter
                    filtered = scipy.signal.filtfilt(b, a, temp_data.get_data()[i, :]) # .get_data()

                    #################### CALCULATE PSD VALUES WITH WELCH'S METHOD ####################

                    # transform the filtered time series data into power spectral density using Welch's method
                    f, px = scipy.signal.welch(filtered, fs)  # Returns: f=array of sample frequencies, px= psd or power spectrum of x (amplitude)
                    # density unit: µV**2/Hz

                    #################### NORMALIZE PSD TO TOTAL SUM ####################

                    # reshape the array to a single-row 2D array, so it can be used in sklearn.preprocessing.normalize()
                    # normalize() does not work with px as input, eventhough it is a numpy array, reshaping px to a 2D array .reshape(1,-1) is necessary
                    px_2Darray = px.reshape(1, -1) # reshape into a single-row 2D Array: -1 is a placeholder, so as many features as in px

                    # sklearn.preprocessing.normalize() norm="l1" will normalize so that sum of absolute values is 1
                    px_rel_2Darray = normalize(px_2Darray, norm='l1') 
                    
                    # reshape back to 1D Array, because of other functions that input 1D arrays: like scipy.signal.find_peaks
                    rel_psd_1Darray = px_rel_2Darray.reshape(-1,) 

                    # *100 to get the values in percentage
                    rel_psd = rel_psd_1Darray * 100

                    # calculate the SEM of psd values and store sem of each channel in dictionary
                    sem = np.std(rel_psd)/np.sqrt(len(rel_psd))
                    sem_dict[f'sem_{tp}_{ch}'] = sem

                    # store frequencies 1-100Hz and relative psd values in a dictionary
                    f_psd_dict[f'{tp}_{ch}'] = [f, rel_psd]
                    
                    # # get y-axis label and limits
                    # axes[t].get_ylabel()
                    # axes[t].get_ylim()

                    #################### PEAK DETECTION ####################

                    # find all peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
                    # X must be a 1D array
                    peaks = scipy.signal.find_peaks(rel_psd, height=0.01) # height: peaks only above 0.1 will be recognized
                    
                    # Error checking: if no peaks found, continue
                    if len(peaks) == 0:
                        continue

                    # get the heights(=y values) and positions(=x values) of all peaks
                    peaks_height = peaks[1]["peak_heights"] # np.array of y-value of peaks = power
                    peaks_pos = f[peaks[0]] # np.array of indeces on x-axis of peaks = frequency

                    # set the x-range for alpha, low beta and high beta and create boolean masks
                    mask_alpha_range = (peaks_pos >= 8) & (peaks_pos <= 12) # alpha_range will output a boolean of True values within the alpha range
                    mask_lowBeta_range = (peaks_pos >= 13) & (peaks_pos <= 20)
                    mask_highBeta_range = (peaks_pos >= 21) & (peaks_pos <= 35)

                    # make a list with all boolean masks of each frequency, so I can loop through
                    frequency_ranges = [mask_alpha_range, mask_lowBeta_range, mask_highBeta_range]

                    # loop through frequency ranges and get the highest peak of each frequency band                
                    for count, mask_frequencies in enumerate(frequency_ranges):

                        frequency = []
                        if count == 0:
                            frequency = "alpha"
                        elif count == 1:
                            frequency = "lowBeta"
                        elif count == 2:
                            frequency = "highBeta"
                        
                        # get all peak positions and heights within each frequency range
                        peaksinfreq_pos = peaks_pos[frequency_ranges[count]]
                        peaksinfreq_height = peaks_height[frequency_ranges[count]]

                        # Error checking: check first, if there is a peak in the frequency range
                        if len(peaksinfreq_height) == 0:
                            continue

                        # select only the highest peak within the alpha range
                        highest_peak_height = peaksinfreq_height.max()

                        # get the index of the highest peak y value to get the corresponding peak position x
                        ix = np.where(peaksinfreq_height == highest_peak_height)
                        highest_peak_pos = peaksinfreq_pos[ix].item() # this will get the x-value of the highest peak from the array as an integer by indexing and using .item()

                        # plot only the highest peak within each frequency band
                        axes[t].scatter(highest_peak_pos, highest_peak_height, color="k", s=15, marker="D")

                        # store highest peak values of each frequency band in a dictionary
                        # highest_peak_dict[f'{tp}_{ch}_highestPEAK_{frequency}'] = [highest_peak_pos, highest_peak_height]

                        highest_peak_dict[f'{tp}_{ch}_highestPEAK_{frequency}'] = [tp, ch, frequency, highest_peak_pos, highest_peak_height]



                    # the title of each plot is set to the timepoint e.g. "postop"
                    axes[t].set_title(tp, fontsize=20)

                    # # get y-axis label and limits
                    # axes[t].get_ylabel()
                    # axes[t].get_ylim()

                    # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
                    axes[t].plot(f, rel_psd, label=f"{ch}_{cond}")  # or np.log10(px)

                    # make a shadowed line of the sem
                    axes[t].fill_between(f, rel_psd-sem, rel_psd+sem, color='b', alpha=0.2)

    font = { "size": 16}
    
    for ax in axes: 
        ax.legend(loc='upper right') # shows legend for each axes[t]
        ax.set(xlim=[-5, 60], ylim=[0, 7])
        ax.set_xlabel("Frequency", fontdict=font)
        ax.set_ylabel("relative PSD to total sum in %", fontdict=font)
        ax.axvline(x=8, color='k', linestyle='--')
        ax.axvline(x=13, color='k', linestyle='--')
        ax.axvline(x=20, color='k', linestyle='--')
        ax.axvline(x=35, color='k', linestyle='--')
    
    #plt.figlegend(loc="upper right")
    plt.show()

    fig.savefig(local_path + f"\sub{incl_sub}_{hemisphere}_normalizedPsdToTotalSum_seperateTimepoints_{pickChannels}.png")
    
    # write DataFrame of all frequencies and psd values of each channel per timepoint
    frequenciesDataFrame = pd.DataFrame({k: v[0] for k, v in f_psd_dict.items()}) # Dataframe of frequencies
    relativePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_psd_dict.items()}) # Dataframe of psd

    # write DataFrame of frequency and psd values of the highest peak in each frequency band
    # highestPEAKDF = pd.DataFrame(highest_peak_dict) # Dataframe with 2 rows and columns each for one single power spectrum
    # highestPEAKDF.rename(index={0: "PEAK_frequency", 1:"PEAK_relativePSD"}, inplace=True) # rename the rows

    highestPEAKDF = pd.DataFrame(highest_peak_dict) # Dataframe with 5 rows and columns for each single power spectrum
    highestPEAKDF.rename(index={0: "session", 1: "bipolarChannel", 2: "frequencyBand", 3: "PEAK_frequency", 4:"PEAK_relativePSD"}, inplace=True) # rename the rows
    highestPEAKDF = highestPEAKDF.transpose() # Dataframe with 5 columns and rows for each single power spectrum


    return {
        "frequenciesDataFrame":frequenciesDataFrame,
        "relativePsdDataFrame":relativePsdDataFrame,
        "SEM":sem_dict,
        "highestPEAK": highestPEAKDF,
        }




def welch_normalizedPsdToTotalSum_seperateChannels(incl_sub: str, incl_session: list, incl_condition: list, tasks: list, pickChannels: list):

    """
    incl_sub = str e.g. 024 
    incl_session = ["postop", "fu3m", "fu12m"]
    tasks = list e.g. ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
    pickChannels = list  ['13', '02', '12', '01', '23', 
    '1A1B', '1B1C', '1A1C', '2A2B', '2B2C', '2A2C', 
    '1A2A', '1B2B', '1C2C']

    This function will first load the data from mainclass.PerceiveData using the input values.
    After loading the data it will calculate and plot the psd of each channel seperately in every timepoint.
    The frequencies and relative psd values will be returned in a Dataframe as a tuple: frequenciesDataFrame, absolutePsdDataFrame
    
    Tasks: only one task is being plotted, a loop over tasks is missing because
    """

    sns.set()

    mainclass_sub = mainclass.PerceiveData(
        sub = incl_sub, 
        incl_modalities=["survey"],
        incl_session = incl_session,
        incl_condition = incl_condition,
        incl_task = ["rest"]
        )


    # results_path = findfolders.get_local_path(folder="results", sub=incl_sub)

    # add error correction for sub and task
    
    f_psd_dict = {} # dictionary with tuples of frequency and psd for each channel and timepoint of a subject
    sem_dict = {}
    highest_peak_dict = {}

    # 

    # # get the channelnames of the first timepoint and the first task (e.g. postop, RestBSSuRingR -> 6 channels: 0_)
    # task_ch_names = getattr(mainclass_sub.survey, incl_session[0])
    # task_ch_names = task_ch_names.m0s0.rest.data[tasks[0]]

    # create grid for plots using the number of pickChannels 
    # fig = plt.figure() -> figure is an instance of a single container containing all objects representing axes, graphics, text and labels    
    # axes = plt.axes() -> axes is a box which will contain the plot

    fig, axes = plt.subplots(len(pickChannels), 1, figsize=(20, 20)) # rows as many as channels, 1 column
    fig.tight_layout(pad=5.0)

    # fig, axes = plt.subplots(len(task_ch_names.ch_names), 1, figsize=(20, 20)) # rows as many as channels, 1 column
    # fig.tight_layout(pad=5.0)


    # loop through each session and task and load mne data
    for t, tp in enumerate(incl_session):

        for tk, task in enumerate(tasks):

            temp_data = getattr(mainclass_sub.survey, tp) # gets attribute e.g. of tp "postop" from modality_class with modality set to survey
            temp_data = temp_data.m0s0.rest.data[tasks[tk]] # e.g. gets the mne loaded data from the BSSu, m0s0 perceived file with task "RestBSSuRingR"

            #################### CREATE A BUTTERWORTH FILTER ####################

            # set filter parameters for band-pass filter
            filter_order = 5 # in MATLAB spm_eeg_filter default=5 Butterworth
            frequency_cutoff_low = 5 # 5Hz high-pass filter
            frequency_cutoff_high = 95 # 95 Hz low-pass filter
            fs = temp_data.info['sfreq'] # sample frequency: 250 Hz

            # create the filter
            b, a = scipy.signal.butter(filter_order, (frequency_cutoff_low, frequency_cutoff_high), btype='bandpass', output='ba', fs=fs)

            #################### RENAME CHANNELS ####################
            # all channel names of one loaded file (one session, one task)
            ch_names_original = temp_data.info.ch_names

            # select only relevant keys and values from the mapping dictionary to rename channels
            mappingSelected = dict((key, mapping[key]) for key in ch_names_original if key in mapping)

            # rename channels using mne and the new selected mapping dictionary
            mne.rename_channels(info=temp_data.info, mapping=mappingSelected, allow_duplicates=False)

            # get new channel names
            ch_names_renamed = temp_data.info.ch_names

            include_channelList = [] # this will be a list with all channel names selected
            exclude_channelList = []

            for n, names in enumerate(ch_names_renamed):
                
                # add all channel names that contain the picked channels: e.g. 02, 13, etc given in the input pickChannels
                for picked in pickChannels:
                    if picked in names:
                        include_channelList.append(names)


                # exclude all bipolar 0-3 channels, because they do not give much information
                # if "03" in names:
                #     exclude_channelList.append(names)
                
    
            # Error Checking: 
            if len(include_channelList) == 0:
                continue

            # pick channels of interest: mne.pick_channels() will output the indices of included channels in an array
            ch_names_indices = mne.pick_channels(ch_names_renamed, include=include_channelList)

            # ch_names = [ch_names_renamed[idx] for idx in ch_names_indices] # new list of picked channel names based on the indeces 
           
            # loop through each channel of the loaded file (one session, one task)
            for i, ch in enumerate(ch_names_renamed):

                # only get picked channels
                if i not in ch_names_indices:
                    continue

                #################### FILTER THE SIGNAL ####################
                filtered = scipy.signal.filtfilt(b, a, temp_data.get_data()[i, :])

                #################### CALCULATE PSD VALUES WITH WELCH'S METHOD ####################
                # transform the filtered time series data into power spectral density using Welch's method
                f, px = scipy.signal.welch(filtered, fs)  # Returns: f=array of sample frequencies, px= psd or power spectrum of x (amplitude)
                # density unit: V**2/Hz


                #################### NORMALIZE PSD TO TOTAL SUM ####################

                # reshape the array to a single-row 2D array, so it can be used in sklearn.preprocessing.normalize()
                # normalize() does not work with px as input, eventhough it is a numpy array, reshaping px to a 2D array .reshape(1,-1) is necessary
                px_2Darray = px.reshape(1, -1) # reshape into a single-row 2D Array: -1 is a placeholder, so as many features as in px

                # sklearn.preprocessing.normalize() norm="l1" will normalize so that sum of absolute values is 1
                px_rel_2Darray = normalize(px_2Darray, norm='l1') 
                
                # reshape back to 1D Array, because of other functions that input 1D arrays: like scipy.signal.find_peaks
                rel_psd_1Darray = px_rel_2Darray.reshape(-1,) 

                # *100 to get the values in percentage
                rel_psd = rel_psd_1Darray * 100

                # store frequencies and relative psd values in a dictionary
                f_psd_dict[f'{tp}_{ch}'] = [f, rel_psd]

                # calculate the SEM of psd values and store sem of each channel in dictionary
                sem = np.std(rel_psd)/np.sqrt(len(rel_psd))
                sem_dict[f'sem_{tp}_{ch}'] = sem

            
                #################### PEAK DETECTION ####################

                # find all peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
                # X must be a 1D array
                peaks = scipy.signal.find_peaks(rel_psd, height=0.01) # height: peaks only above 0.1 will be recognized
                
                # Error checking: if no peaks found, continue
                if len(peaks) == 0:
                    continue

                # get the heights(=y values) and positions(=x values) of all peaks
                peaks_height = peaks[1]["peak_heights"] # np.array of y-value of peaks = power
                peaks_pos = f[peaks[0]] # np.array of indeces on x-axis of peaks = frequency

                # set the x-range for alpha, low beta and high beta and create boolean masks
                mask_alpha_range = (peaks_pos >= 8) & (peaks_pos <= 12) # alpha_range will output a boolean of True values within the alpha range
                mask_lowBeta_range = (peaks_pos >= 13) & (peaks_pos <= 20)
                mask_highBeta_range = (peaks_pos >= 21) & (peaks_pos <= 35)

                # make a list with all boolean masks of each frequency, so I can loop through
                frequency_ranges = [mask_alpha_range, mask_lowBeta_range, mask_highBeta_range]

                # loop through frequency ranges and get the highest peak of each frequency band                
                for count, mask_frequencies in enumerate(frequency_ranges):

                    frequency = []
                    if count == 0:
                        frequency = "alpha"
                    elif count == 1:
                        frequency = "lowBeta"
                    elif count == 2:
                        frequency = "highBeta"
                    
                    # get all peak positions and heights within each frequency range
                    peaksinfreq_pos = peaks_pos[frequency_ranges[count]]
                    peaksinfreq_height = peaks_height[frequency_ranges[count]]

                    # Error checking: check first, if there is a peak in the frequency range
                    if len(peaksinfreq_height) == 0:
                        continue

                    # select only the highest peak within the alpha range
                    highest_peak_height = peaksinfreq_height.max()

                    # get the index of the highest peak y value to get the corresponding peak position x
                    ix = np.where(peaksinfreq_height == highest_peak_height)
                    highest_peak_pos = peaksinfreq_pos[ix].item() # this will get the x-value of the highest peak from the array as an integer by indexing and using .item()

                    # plot only the highest peak within each frequency band
                    axes[i].scatter(highest_peak_pos, highest_peak_height, color='r', s=15, marker='D')

                    # store highest peak values of each frequency band in a dictionary
                    highest_peak_dict[f'{tp}_{ch}_highestPEAK_{frequency}'] = [highest_peak_pos, highest_peak_height]


                # get y-axis label and limits
                axes[i].get_ylabel()
                axes[i].get_ylim()

                # axes in row number of channel index, all in same column 1
                axes[i].set_title(ch) # the title of each plot is set to the channel e.g. "LFP_Stn_R_03"

                # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
                axes[i].plot(f, rel_psd, label=tp)  # or np.log10(px)

                # make a shadowed line of the sem
                axes[i].fill_between(f, rel_psd-sem, rel_psd+sem, color='b', alpha=0.2)
                
    
    for ax in axes: 
        ax.legend(loc='upper right') # shows legend for each axes[t]
        ax.set(xlabel="Frequency", ylabel="relative PSD to total sum in % +- SEM", xlim=[-5, 100])
        # mark vertical lines seperating alpha, low beta and high beta frequency bands
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')
    

    plt.show()
    
    # write DataFrame of frequencies and psd values of each channel per timepoint
    frequenciesDataFrame = pd.DataFrame({k: v[0] for k, v in f_psd_dict.items()}) # Dataframe of frequencies
    relativePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_psd_dict.items()}) # Dataframe of psd

    # write DataFrame of frequency and psd values of the highest peak in each frequency band
    highestPEAKDF = pd.DataFrame(highest_peak_dict) # Dataframe with 2 rows and columns each for one single power spectrum
    highestPEAKDF.rename(index={0: "PEAK_frequency", 1:"PEAK_relativePSD"}, inplace=True) # rename the rows
    

    return {
        "frequenciesDataFrame":frequenciesDataFrame,
        "relativePsdDataFrame":relativePsdDataFrame,
        "SEM":sem_dict,
        "highestPEAK": highestPEAKDF,
        }


    # for adding subplots use Figure.add_subplot()
