""" power spectral density methods """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import scipy
from scipy.signal import butter, filtfilt, freqz

import sklearn
from sklearn.preprocessing import normalize

import json
import os
import mne

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



def welch_rawPsd_seperateTimepoints(incl_sub: str, incl_session: list, incl_condition: list, tasks: list, pickChannels: list, hemisphere: str, normalization: str):
    """

    Input: 
        - incl_sub = str e.g. "024"
        - incl_session = list ["postop", "fu3m", "fu12m", "fu18m", "fu24m"]
        - incl_condition = list e.g. ["m0s0", "m1s0"]
        - tasks = list ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
        - hemisphere: str e.g. "Right"
        - normalization: str "rawPSD", "normPsdToTotalSum", "normPsdToSum1_100Hz", "normPsdToSum40_90Hz"

    
    1) load data from mainclass.PerceiveData using the input values.
    
    2) band-pass filter by a Butterworth Filter of fifth order (5-95 Hz).
    
    3) Calculate the raw psd values of every channel for each timepoint by using Welch's method.

    4) Normalization variants: calculate different normalized PSD values 
        - normalized to total sum of PSD from each power spectrum
        - normalized to sum of PSD from 1-100 Hz
        - normalized to sum of PSD from 40-90 Hz


    Depending on normalization variation: 
    
    5) For each frequency band alpha (8-12 Hz), low beta (13-20 Hz), high beta (21-35 Hz), beta (13-35 Hz), gamma (40-90 Hz) the highest Peak values (frequency and psd) will be seleted and saved in a DataFrame.

    6) The raw or noramlized PSD values will be plotted and the figure will be saved as:
        f"\sub{incl_sub}_{hemisphere}_normalizedPsdToTotalSum_seperateTimepoints_{pickChannels}.png"
    
    6) All frequencies and relative psd values, as well as the values for the highest PEAK in each frequency band will be returned as a Dataframe in a dictionary: 
    
    return {
        "rawPsdDataFrame":rawPSDDataFrame,
        "normPsdToTotalSumDataFrame":normToTotalSumPsdDataFrame,
        "normPsdToSum1_100Hz": normToSum1_100Hz,
        "normPsdToSum40_90Hz":normToSum40_90Hz,
        "psdAverage_dict": psdAverage_dict,
        "highestPeakRawPSD": highestPeakRawPsdDF,
    }

    """

    # sns.set()

    mainclass_sub = mainclass.PerceiveData(
        sub = incl_sub, 
        incl_modalities= ["survey"],
        incl_session = incl_session,
        incl_condition = incl_condition,
        incl_task = ["rest"]
        )

    
    local_path = findfolders.get_local_path(folder="figures", sub=incl_sub)

    # add error correction for sub and task??
    
    f_rawPsd_dict = {} # dictionary with tuples of frequency and psd for each channel and timepoint of a subject
    f_normPsdToTotalSum_dict = {}
    f_normPsdToSum1to100Hz_dict = {}
    f_normPsdToSum40to90Hz_dict = {}
    psdAverage_dict = {}
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
            
                # try:
                #     temp_data = getattr(temp_data, cond)
                #     temp_data = temp_data.rest.data[tasks[tk]]
                
                # except AttributeError:
                #     continue

                temp_data = getattr(temp_data, cond) # gets attribute e.g. "m0s0"
                temp_data = temp_data.rest.data[tasks[tk]] # gets the mne loaded data from the perceive .mat BSSu, m0s0 file with task "RestBSSuRingR"
    
                print("DATA", temp_data)

                #################### CREATE A BUTTERWORTH FILTER ####################

                # sample frequency: 250 Hz
                fs = temp_data.info['sfreq'] 

                # set filter parameters for band-pass filter
                filter_order = 5 # in MATLAB spm_eeg_filter default=5 Butterworth
                frequency_cutoff_low = 5 # 5Hz high-pass filter
                frequency_cutoff_high = 95 # 95 Hz low-pass filter
                fs = temp_data.info['sfreq'] # sample frequency: 250 Hz

                # create the filter
                b, a = scipy.signal.butter(filter_order, (frequency_cutoff_low, frequency_cutoff_high), btype='bandpass', output='ba', fs=fs)


                # the title of each plot is set to the timepoint e.g. "postop"
                axes[t].set_title(tp)  

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

                    #################### FILTER ####################

                    # filter the signal by using the above defined butterworth filter
                    filtered = scipy.signal.filtfilt(b, a, temp_data.get_data()[i, :]) # .get_data()

                    #################### GET ABSOLUTE PSD VALUES BY USING WELCH'S METHOD ####################

                    # transform the filtered time series data into power spectral density using Welch's method
                    f, px = scipy.signal.welch(filtered, fs)  # Returns: f=array of sample frequencies, px= psd or power spectrum of x (amplitude)
                    # density unit: mV**2/Hz

                    # calculate the SEM of psd values and store sem of each channel in dictionary
                    semRawPsd = np.std(px)/np.sqrt(len(px))
                    # semRawPsd_dict[f'sem_{tp}_{ch}'] = semRawPsd

                    # average of PSD in each frequency band
                    

                    # store frequency, raw psd and sem values in a dictionary, together with session timepoint and channel
                    f_rawPsd_dict[f'{tp}_{ch}'] = [tp, ch, f, px, semRawPsd]

                

                    #################### NORMALIZE PSD IN MULTIPLE WAYS ####################
                    
                    #################### NORMALIZE PSD TO TOTAL SUM OF THE POWER SPECTRUM (ALL FREQUENCIES) ####################

                    # reshape the array to a single-row 2D array, so it can be used in sklearn.preprocessing.normalize()
                    # normalize() does not work with px as input, eventhough it is a numpy array, reshaping px to a 2D array .reshape(1,-1) is necessary
                    px_2Darray = px.reshape(1, -1) # reshape into a single-row 2D Array: -1 is a placeholder, so as many features as in px

                    # sklearn.preprocessing.normalize() norm="l1" will normalize so that sum of absolute values is 1
                    px_rel_2Darray = normalize(px_2Darray, norm='l1') 
                    
                    # reshape back to 1D Array, because of other functions that input 1D arrays: like scipy.signal.find_peaks
                    rel_psd_1Darray = px_rel_2Darray.reshape(-1,) 

                    # *100 to get the values in percentage
                    normToTotalSum_psd = rel_psd_1Darray * 100                  

                    # calculate the SEM of psd values 
                    semNormToTotalSum_psd = np.std(normToTotalSum_psd)/np.sqrt(len(normToTotalSum_psd))

                    # store frequencies and normalized psd values and sem of normalized psd in a dictionary
                    f_normPsdToTotalSum_dict[f'{tp}_{ch}'] = [tp, ch, f, normToTotalSum_psd, semNormToTotalSum_psd]


                    #################### NORMALIZE PSD TO SUM OF PSD BETWEEN 1-100 Hz  ####################
                   
                    # get raw psd values from 1 to 100 Hz by indexing the numpy arrays f and px
                    rawPsd_1to100Hz = px[1:104]

                    # sum of rawPSD between 1 and 100 Hz
                    psdSum1to100Hz = rawPsd_1to100Hz.sum()

                    # raw psd divided by sum of psd between 1 and 100 Hz
                    normPsdToSum1to100Hz = px/psdSum1to100Hz
                    percentageNormPsdToSum1to100Hz = normPsdToSum1to100Hz * 100 

                    # calculate the SEM of psd values 
                    semNormPsdToSum1to100Hz = np.std(percentageNormPsdToSum1to100Hz)/np.sqrt(len(percentageNormPsdToSum1to100Hz))

                    # store frequencies and normalized psd values and sem of normalized psd in a dictionary
                    f_normPsdToSum1to100Hz_dict[f'{tp}_{ch}'] = [tp, ch, f, percentageNormPsdToSum1to100Hz, semNormPsdToSum1to100Hz]


                    #################### NORMALIZE PSD TO SUM OF PSD BETWEEN 40-90 Hz  ####################
                   
                    # get raw psd values from 40 to 90 Hz (gerundet) by indexing the numpy arrays f and px
                    rawPsd_40to90Hz = px[41:93] 

                    # sum of rawPSD between 40 and 90 Hz
                    psdSum40to90Hz = rawPsd_40to90Hz.sum()

                    # raw psd divided by sum of psd between 40 and 90 Hz
                    normPsdToSum40to90Hz = px/psdSum40to90Hz
                    percentageNormPsdToSum40to90Hz = normPsdToSum40to90Hz * 100 

                    # calculate the SEM of psd values 
                    semNormPsdToSum40to90Hz = np.std(percentageNormPsdToSum40to90Hz)/np.sqrt(len(percentageNormPsdToSum40to90Hz))

                    # store frequencies and normalized psd values and sem of normalized psd in a dictionary
                    f_normPsdToSum40to90Hz_dict[f'{tp}_{ch}'] = [tp, ch, f, percentageNormPsdToSum40to90Hz, semNormPsdToSum40to90Hz]

                    

                    # get y-axis label and limits
                    axes[t].get_ylabel()
                    axes[t].get_ylim()

                    #################### PEAK DETECTION ####################

                    # depending on what normalization or raw was chosen: define variables for psd, sem and ylabel accordingly
                    if normalization == "rawPsd":
                        chosenPsd = px
                        chosenSem = semRawPsd
                        chosen_ylabel = "uV^2/Hz +- SEM"
                    
                    elif normalization == "normPsdToTotalSum":
                        chosenPsd = normToTotalSum_psd
                        chosenSem = semNormToTotalSum_psd
                        chosen_ylabel = "relative PSD to total sum in % +- SEM"

                    elif normalization == "normPsdToSum1_100Hz":
                        chosenPsd = percentageNormPsdToSum1to100Hz
                        chosenSem = semNormPsdToSum1to100Hz
                        chosen_ylabel = "relative PSD to sum between 1-100 Hz in % +- SEM"

                    elif normalization == "normPsdToSum40_90Hz":
                        chosenPsd = percentageNormPsdToSum40to90Hz
                        chosenSem = semNormPsdToSum40to90Hz
                        chosen_ylabel = "relative PSD to sum between 40-90 Hz in % +- SEM"


                    #################### PSD AVERAGE OF EACH FREQUENCY BAND DEPENDING ON CHOSEN PSD NORMALIZATION ####################
                    
                    # create booleans for each frequency-range for alpha, low beta, high beta, beta and gamma
                    alpha_frequency = (f >= 8) & (f <= 12) # alpha_range will output a boolean of True values within the alpha range
                    lowBeta_frequency = (f >= 13) & (f <= 20)
                    highBeta_frequency = (f >= 21) & (f <= 35)
                    beta_frequency = (f >= 13) & (f <= 35)
                    narrowGamma_frequency = (f >= 40) & (f <= 90)

                    # make a list with all boolean masks of each frequency, so I can loop through
                    range_allFrequencies = [alpha_frequency, lowBeta_frequency, highBeta_frequency, beta_frequency, narrowGamma_frequency]

                    # loop through frequency ranges and get all psd values of each frequency band
                    for count, boolean in enumerate(range_allFrequencies):

                        frequency = []
                        if count == 0:
                            frequency = "alpha"
                        elif count == 1:
                            frequency = "lowBeta"
                        elif count == 2:
                            frequency = "highBeta"
                        elif count == 3:
                            frequency = "beta"
                        elif count == 4:
                            frequency = "narrowGamma"


                        # get all frequencies and chosen psd values within each frequency range
                        frequencyInFreqBand = f[range_allFrequencies[count]] # all frequencies within a frequency band
                        psdInFreqBand = chosenPsd[range_allFrequencies[count]] # all psd values within a frequency band

                        psdAverage = np.mean(psdInFreqBand)

                        # store averaged psd values of each frequency band in a dictionary
                        psdAverage_dict[f'{tp}_{ch}_psdAverage_{frequency}'] = [tp, ch, frequency, psdAverage]



                    #################### PEAK DETECTION PSD DEPENDING ON CHOSEN PSD NORMALIZATION ####################
                    # find all peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
                    peaks = scipy.signal.find_peaks(chosenPsd, height=0.1) # height: peaks only above 0.1 will be recognized

                    # Error checking: if no peaks found, continue
                    if len(peaks) == 0:
                        continue

                    peaks_height = peaks[1]["peak_heights"] # np.array of y-value of peaks = power
                    peaks_pos = f[peaks[0]] # np.array of indeces on x-axis of peaks = frequency

                    # set the x-range for each frequency band
                    alpha_range = (peaks_pos >= 8) & (peaks_pos <= 12) # alpha_range will output a boolean of True values within the alpha range
                    lowBeta_range = (peaks_pos >= 13) & (peaks_pos <= 20)
                    highBeta_range = (peaks_pos >= 21) & (peaks_pos <= 35)
                    beta_range = (peaks_pos >= 13) & (peaks_pos <= 35)
                    narrowGamma_range = (peaks_pos >= 40) & (peaks_pos <= 90)

                    # make a list with all boolean masks of each frequency, so I can loop through
                    frequency_ranges = [alpha_range, lowBeta_range, highBeta_range, beta_range, narrowGamma_range]

                    # loop through frequency ranges and get the highest peak of each frequency band
                    for count, boolean in enumerate(frequency_ranges):

                        frequency = []
                        if count == 0:
                            frequency = "alpha"
                        elif count == 1:
                            frequency = "lowBeta"
                        elif count == 2:
                            frequency = "highBeta"
                        elif count == 3:
                            frequency = "beta"
                        elif count == 4:
                            frequency = "narrowGamma"
                        
                        # get all peak positions and heights within each frequency range
                        peaksinfreq_pos = peaks_pos[frequency_ranges[count]]
                        peaksinfreq_height = peaks_height[frequency_ranges[count]]

                        # Error checking: check first, if there is a peak in the frequency range
                        if len(peaksinfreq_height) == 0:
                            continue

                        # select only the highest peak within the alpha range
                        highest_peak_height = peaksinfreq_height.max()

                        ######## calculate psd average of +- 2 Hz from highest Peak ########
                        # 1) find psd values from -2Hz until + 2Hz from highest Peak by slicing and indexing the numpy array of all chosen psd values
                        peakIndex = np.where(chosenPsd == highest_peak_height) # np.where output is a tuple: index, dtype
                        peakIndexValue = peakIndex[0].item() # only take the index value of the highest Peak psd value in all chosen psd

                        # 2) go -2 and +3 indeces 
                        indexlowCutt = peakIndexValue-2
                        indexhighCutt = peakIndexValue+3   # +3 because the ending index is left out when slicing a numpy array

                        # 3) slice the numpy array of all chosen psd values, only get values from -2 until +2 Hz from highest Peak
                        psdArray5HzRangeAroundPeak = chosenPsd[indexlowCutt:indexhighCutt] # array only of psd values -2 until +2Hz around Peak = 5 values

                        # 4) Average of 5Hz Array
                        highest_peak_height_5Hzaverage = np.mean(psdArray5HzRangeAroundPeak)                       



                        # get the index of the highest peak y value to get the corresponding peak position x
                        ix = np.where(peaksinfreq_height == highest_peak_height)
                        highest_peak_pos = peaksinfreq_pos[ix].item()

                        # plot only the highest peak within each frequency band
                        axes[t].scatter(highest_peak_pos, highest_peak_height, s=15, marker='D')

                        # store highest peak values of each frequency band in a dictionary
                        highest_peak_dict[f'{tp}_{ch}_highestPEAK_{frequency}'] = [tp, ch, frequency, highest_peak_pos, highest_peak_height, highest_peak_height_5Hzaverage]




                    #################### PLOT THE CHOSEN PSD DEPENDING ON NORMALIZATION INPUT ####################

                    # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
                    axes[t].plot(f, chosenPsd, label=f"{ch}_{cond}")  # or np.log10(px)

                    # make a shadowed line of the sem
                    axes[t].fill_between(f, chosenPsd-chosenSem, chosenPsd+chosenSem, color='b', alpha=0.2)



    #################### PLOT SETTINGS ####################
    for ax in axes: 
        ax.legend(loc= 'upper right') # Legend will be in upper right corner
        ax.set(xlabel="Frequency", ylabel= chosen_ylabel, xlim=[-5, 60])
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')
    

    plt.show()
    fig.savefig(local_path + f"\sub{incl_sub}_{hemisphere}_{normalization}_{pickChannels}.png")
    
    # write DataFrame of all frequencies and psd values of each channel per timepoint
    # frequenciesDataFrame = pd.DataFrame({k: v[0] for k, v in f_rawPsd_dict.items()}) # Dataframe of frequencies: columns=single bipolar channel of one session
    # rawPsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_rawPsd_dict.items()}) # Dataframe of raw psd: columns=single bipolar channel of one session
    # semRawPsdDataFrame = pd.DataFrame({k: v[2] for k, v in f_rawPsd_dict.items()}) # Dataframe of sem of rawPsd: columns=single bipolar channel of one session


    #################### WRITE DATAFRAMES TO STORE VALUES ####################
    # write raw PSD Dataframe
    rawPSDDataFrame = pd.DataFrame(f_rawPsd_dict)
    rawPSDDataFrame.rename(index={0: "session", 1: "bipolarChannel", 2: "frequency", 3: "rawPSD", 4: "SEM_rawPSD"}, inplace=True) # rename the rows
    rawPSDDataFrame = rawPSDDataFrame.transpose() # Dataframe with 5 columns and rows for each single power spectrum

    # write DataFrame of normalized PSD to total Sum
    normPsdToTotalSumDataFrame = pd.DataFrame(f_normPsdToTotalSum_dict) # Dataframe of normalised to total sum psd: columns=single bipolar channel of one session
    normPsdToTotalSumDataFrame.rename(index={0: "session", 1: "bipolarChannel", 2: "frequency", 3: "normPsdToTotalSum", 4: "SEM_normPsdToTotalSum"}, inplace=True) # rename the rows
    normPsdToTotalSumDataFrame = normPsdToTotalSumDataFrame.transpose() # Dataframe with 5 columns and rows for each single power spectrum

    # write DataFrame of normalized PSD to Sum of PSD between 1 and 100 Hz
    normPsdToSum1to100HzDataFrame = pd.DataFrame(f_normPsdToSum1to100Hz_dict) # Dataframe of normalised to total sum psd: columns=single bipolar channel of one session
    normPsdToSum1to100HzDataFrame.rename(index={0: "session", 1: "bipolarChannel", 2: "frequency", 3: "normPsdToSumPsd1to100Hz", 4: "SEM_normPsdToSumPsd1to100Hz"}, inplace=True) # rename the rows
    normPsdToSum1to100HzDataFrame = normPsdToSum1to100HzDataFrame.transpose() # Dataframe with 5 columns and rows for each single power spectrum

    # write DataFrame of normalized PSD to Sum of PSD between 1 and 100 Hz
    normPsdToSum40to90DataFrame = pd.DataFrame(f_normPsdToSum40to90Hz_dict) # Dataframe of normalised to total sum psd: columns=single bipolar channel of one session
    normPsdToSum40to90DataFrame.rename(index={0: "session", 1: "bipolarChannel", 2: "frequency", 3: "normPsdToSum40to90Hz", 4: "SEM_normPsdToSum40to90Hz"}, inplace=True) # rename the rows
    normPsdToSum40to90DataFrame = normPsdToSum40to90DataFrame.transpose() # Dataframe with 5 columns and rows for each single power spectrum

    # write DataFrame of averaged psd values in each frequency band depending on the chosen normalization
    psdAverageDF = pd.DataFrame(psdAverage_dict) # Dataframe with 5 rows and columns for each single power spectrum
    psdAverageDF.rename(index={0: "session", 1: "bipolarChannel", 2: "frequencyBand", 3: f"averaged{normalization}"}, inplace=True) # rename the rows
    psdAverageDF = psdAverageDF.transpose() # Dataframe with 4 columns and rows for each single power spectrum


    # write DataFrame of frequency and psd values of the highest peak in each frequency band
    highestPEAKDF = pd.DataFrame(highest_peak_dict) # Dataframe with 5 rows and columns for each single power spectrum
    highestPEAKDF.rename(index={0: "session", 1: "bipolarChannel", 2: "frequencyBand", 3: "PEAK_frequency", 4:f"PEAK_{normalization}", 5: "highest_peak_height_5HzAverage"}, inplace=True) # rename the rows
    highestPEAKDF = highestPEAKDF.transpose() # Dataframe with 6 columns and rows for each single power spectrum



    return {
        "rawPsdDataFrame":rawPSDDataFrame,
        "normPsdToTotalSumDataFrame":normPsdToTotalSumDataFrame,
        "normPsdToSum1to100HzDataFrame":normPsdToSum1to100HzDataFrame,
        "normPsdToSum40to90HzDataFrame":normPsdToSum40to90DataFrame,
        f"averaged{normalization}": psdAverageDF,
        f"highestPEAK{normalization}": highestPEAKDF,
    }











#### watch out!! in this function you work with Dataframes!! so there are differences to the function above where you mostly work woth numpy arrays! ####
#### next task: not reuse Dataframes for Normalization but create another version of plotting normalized psd similar to the above function


def normalize_psd_toTotalSum(frequenciesDataFrame, rawPsdDataFrame):

    """
    subject = str e.g. 024 
    frequenciesDataFrame = Dataframe of all frequencies of a subject (1st of tuple from welch_psd_survey_m0s0)
    absolutePsdDataFrame = Dataframe of all frequencies of a subject (2nd of tuple from welch_psd_survey_m0s0)
    

    before using this function first run the method calculate_psd_survey_m0s0() to get the tuple with frequencies and psd of the certain subject 

    this function will normalize the psd values of each power spectrum by dividing each psd by its total sum
    it will also plot the relative psd values of every channel in seperate plots for each session (postop, fu3m, fu12m, fu18m) 
    """

    time_points = ['postop', 'fu3m', 'fu12m', 'fu18m']
    f_1to100Hz_dict = {} # dict with keys('postop_f_1to100Hz', 'fu3m_f_1to100Hz', 'fu12m_f_1to100Hz', 'fu18m_f_1to100Hz')
    psd_dict = {} # dict will be filled: keys('postop_relative_psd', 'fu3m_relative_psd', 'fu12_relative_psd', 'fu18m_relative_psd')
    f_relPsd_dict = {} # 
    highest_peak_dict = {}

    # just get Frequencies 1-100 Hz
    f_1to100Hz = frequenciesDataFrame[1:104] #.iloc[:,0] #only take first column

    # set layout for figures: using the object-oriented interface
    fig, axes = plt.subplots(len(time_points), 1, figsize=(15, 15)) # subplot(rows, columns, panel number)
    fig.tight_layout(pad=5.0) # space in between each plot

    for t, tp in enumerate(time_points):

        # the title of each plot is set to the timepoint e.g. "postop"
        axes[t].set_title(tp) 

        # select the right frequency and psd columns per timepoint and add them to the empty dictionaries
        f_1to100Hz_dict[f'{tp}_f_1to100Hz'] = f_1to100Hz.filter(like=tp) # filter DF by each session
        psd_dict[f'{tp}_psd'] = rawPsdDataFrame[1:104].filter(like=tp) # filter DF by each session across 1-100Hz

        # get channel names by getting the column names from the DataFrame stored as values in the psd_dict
        ch_names = psd_dict[f'{tp}_psd'].columns

        for i, ch in enumerate(ch_names):

            # get psd values from each channel column 
            absolute_psd = psd_dict[f'{tp}_psd'][ch] 
            f = f_1to100Hz_dict[f'{tp}_f_1to100Hz'][ch]


            ####### NORMALIZE PSD TO TOTAL SUM #######
            # normalize psd values to total sum of the same power spectrum
            totalSum_psd = absolute_psd.sum()
            rel_psd = absolute_psd.div(totalSum_psd)
            percentage_psd = rel_psd * 100 

            # save frequencies and relative psd values in a dictionary
            f_relPsd_dict[f'{tp}_{ch}'] = [f, percentage_psd]

            # calculate the SEM of psd values
            sem = np.std(percentage_psd)/np.sqrt(len(percentage_psd))

            # get y-axis label and limits
            axes[t].get_ylabel()
            axes[t].get_ylim()

            ######## PEAK DETECTION ########
            # find all peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
            peaks = scipy.signal.find_peaks(percentage_psd, height=0.1) # height: peaks only above 0.1 will be recognized
            peaks_height = peaks[1]["peak_heights"] # np.array of y-value of peaks = power
            peaks_pos = f[peaks[0]] # this is a pandas Series!! of indeces on x-axis of peaks = frequency

            # set the x-range for alpha, low beta and high beta
            alpha_range = (peaks_pos >= 8) & (peaks_pos <= 12) # alpha_range will output a boolean of True values within the alpha range
            lowBeta_range = (peaks_pos >= 13) & (peaks_pos <= 20)
            highBeta_range = (peaks_pos >= 21) & (peaks_pos <= 35)
            frequency_ranges = [alpha_range, lowBeta_range, highBeta_range]

            # loop through frequency ranges and get the highest peak of each frequency band
            for count, boolean in enumerate(frequency_ranges):

                # give each count of the loop a name, so I can use alpha, lowbeta and highbeta later in the dictionary
                frequency = []
                if count == 0:
                    frequency = "alpha"
                elif count == 1:
                    frequency = "lowBeta"
                elif count == 2:
                    frequency = "highBeta"
                
                # get all peak positions and heights within each frequency range
                peaksinfreq_pos = peaks_pos[frequency_ranges[count]] # select only the peak positions within the frequency range
                peaksinfreq_height = peaks_height[frequency_ranges[count]]

                # Error checking: check first, if there is a peak in the frequency range
                if len(peaksinfreq_height) == 0:
                    continue

                # select only the highest peak within the alpha range
                highest_peak_height = peaksinfreq_height.max()

                # get the index of the highest peak y value to get the corresponding peak position x
                ix = np.where(peaksinfreq_height == highest_peak_height)
                highest_peak_pos = peaksinfreq_pos.iloc[ix] # use .iloc here because peaksinfreq_pos is pandas Series

                # plot only the highest peak within each frequency band
                axes[t].scatter(highest_peak_pos, highest_peak_height, color='r', s=15, marker='D')

                # store highest peak values of each frequency band in a dictionary
                highest_peak_dict[f'{tp}_{ch}_highestPEAK_{frequency}'] = [highest_peak_pos, highest_peak_height]


            # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
            axes[t].plot(f, percentage_psd, label=ch)  # or np.log10(px)
            # make a shadowed line of the sem
            axes[t].fill_between(f, percentage_psd-sem, percentage_psd+sem, color='b', alpha=0.2)
                

    for ax in axes: 
        ax.legend(loc= 'upper right') # shows legend for each axes[t], loc sets the position of the spectrum
        ax.set(xlabel="Frequency", ylabel="relative PSD (% of total sum) +- SEM", ylim=(-1, 8)) # set y axis to -0.01 until 0.08(=8%)
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')


    plt.show() 

    # write DataFrame of frequencies and psd values of each channel per timepoint
    frequenciesrelDataFrame = pd.DataFrame({k: v[0] for k, v in f_relPsd_dict.items()}) # Dataframe of frequencies
    relativePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_relPsd_dict.items()}) # Dataframe of psd

    # write DataFrame of frequency and psd values of the highest peak in each frequency band
    highestrelPEAKDF = pd.DataFrame(highest_peak_dict) # Dataframe with 2 rows and columns each for one single power spectrum
    highestrelPEAKDF.rename(index={0: "PEAK_frequency", 1:"PEAK_absolutePSD"}, inplace=True) # rename the rows

    return {
        "frequenciesDataFrame":frequenciesrelDataFrame,
        "absolutePsdDataFrame": relativePsdDataFrame,
        "highestrelativePEAK": highestrelPEAKDF
        }






def perChannel_absolutePsd_noPickChannels(incl_sub, incl_session, tasks):

    """
    incl_sub = str e.g. 024 
    incl_session = 
    tasks = list e.g. ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']

    This function will first load the data from mainclass.PerceiveData using the input values.
    After loading the data it will calculate and plot the psd of each channel seperately in every timepoint.
    The frequencies and absolute psd values will be returned in a Dataframe as a tuple: frequenciesDataFrame, absolutePsdDataFrame
    
    Tasks: only one task is being plotted, a loop over tasks is missing because
    """

    sns.set()

    mainclass_sub = mainclass.PerceiveData(
        sub = incl_sub, 
        incl_modalities=["survey"],
        incl_session = incl_session,
        incl_condition = ["m0s0"],
        incl_task = ["rest"]
        )

    # results_path = findfolders.get_local_path(folder="results", sub=incl_sub)

    # add error correction for sub and task
    # tasks = ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
    f_psd_dict = {} # dictionary with tuples of frequency and psd for each channel and timepoint of a subject
    sem_dict = {}


    # get the channelnames of the first timepoint and the first task (e.g. postop, RestBSSuRingR -> 6 channels)
    task_ch_names = getattr(mainclass_sub.survey, incl_session[0])
    task_ch_names = task_ch_names.m0s0.rest.data[tasks[0]]

    # create grid for plots using the number of channelnames 
    # fig = plt.figure() -> figure is an instance of a single container containing all objects representing axes, graphics, text and labels    
    # axes = plt.axes() -> axes is a box which will contain the plot

    fig, axes = plt.subplots(len(task_ch_names.ch_names), 1, figsize=(20, 20)) # rows as many as channels, 1 column
    fig.tight_layout(pad=5.0)


    for t, tp in enumerate(incl_session):

        temp_data = getattr(mainclass_sub.survey, tp) # gets attribute e.g. of tp "postop" from modality_class with modality set to survey
        temp_data = temp_data.m0s0.rest.data[tasks[0]] # e.g. gets the mne loaded data from the BSSu, m0s0 perceived file with task "RestBSSuRingR"

        # sample frequency: 250 Hz
        fs = temp_data.info['sfreq']

        # set filter parameters for high-pass filter
        filter_order = 5 # in MATLAB spm_eeg_filter default=5 Butterworth
        frequency_cutoff = 5 # 5Hz high-pass filter

        # create the 5Hz high-pass filter
        b, a = scipy.signal.butter(filter_order, frequency_cutoff, btype='high', output='ba', fs=fs)

        # channel names 
        ch_names = temp_data.info.ch_names

        # make a plot for each channel of each timepoint
        for i, ch in enumerate(ch_names):

            # create the filtered signal
            filtered = scipy.signal.filtfilt(b, a, temp_data.get_data()[i, :])

            # transform the filtered time series data into power spectral density using Welch's method
            f, px = scipy.signal.welch(filtered, fs)  # Returns: f=array of sample frequencies, px= psd or power spectrum of x (amplitude)
            # density unit: V**2/Hz

            # store frequency and psd values in new dictionary
            f_psd_dict[f'{tp}_{ch}'] = [f, px]

            # calculate the SEM of psd values
            sem = np.std(px)/np.sqrt(len(px))
            sem_dict[f'sem_{tp}_{ch}'] = sem

            # find peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
            peaks = scipy.signal.find_peaks(px, height=0.1) # height: peaks only above 0.1 will be recognized
            peaks_height = peaks[1]["peak_heights"] # arraw of y-value of peaks = power
            peaks_pos = f[peaks[0]] # array of indeces on x-axis of peaks = frequency

            # get y-axis label and limits
            axes[i].get_ylabel()
            axes[i].get_ylim()

            # axes in row number of channel index, all in same column 1
            axes[i].set_title(ch) # the title of each plot is set to the channel e.g. "LFP_Stn_R_03"

            # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
            axes[i].plot(f, px, label=tp)  # or np.log10(px)

            # make a shadowed line of the sem
            axes[i].fill_between(f, px-sem, px+sem, color='b', alpha=0.2)
            axes[i].scatter(peaks_pos, peaks_height, color='r', s=15, marker='D')
    
    for ax in axes: 
        ax.legend() # shows legend for each axes[t]
        ax.set(xlabel="Frequency", ylabel="mV^2/Hz +- SEM")
        # mark vertical lines seperating alpha, low beta and high beta frequency bands
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')
    

    plt.show()
    
    # write DataFrame of frequencies and psd values of each channel per timepoint
    frequenciesDataFrame = pd.DataFrame({k: v[0] for k, v in f_psd_dict.items()}) # Dataframe of frequencies
    absolutePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_psd_dict.items()}) # Dataframe of psd

    return {
        "frequenciesDataFrame":frequenciesDataFrame,
        "absolutePsdDataFrame":absolutePsdDataFrame,
        "SEM":sem_dict
        }


    # for adding subplots use Figure.add_subplot()



def welch_absolutePsd_seperateChannels(incl_sub: str, incl_session: list, incl_condition: list, tasks: list, pickChannels: list):

    """
    incl_sub = str e.g. 024 
    incl_session = list ["postop", ]
    incl_condition = list ["m0s0", "m1s0"]
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

        for c, cond in enumerate(incl_condition):

            for tk, task in enumerate(tasks):
                
                #################### LOAD DATA ####################
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

                    # store frequencies and relative psd values in a dictionary
                    f_psd_dict[f'{tp}_{ch}'] = [f, px]

                    # calculate the SEM of psd values and store sem of each channel in dictionary
                    sem = np.std(px)/np.sqrt(len(px))
                    sem_dict[f'sem_{tp}_{ch}'] = sem

                
                    #################### PEAK DETECTION ####################

                    # find all peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
                    # X must be a 1D array
                    peaks = scipy.signal.find_peaks(px, height=0.01) # height: peaks only above 0.1 will be recognized
                    
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
                    axes[i].plot(f, px, label=f"{tp}_{cond}")  # or np.log10(px)

                    # make a shadowed line of the sem
                    axes[i].fill_between(f, px-sem, px+sem, color='b', alpha=0.2)
                    
    
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










# input are Dataframes

def normalize_totalSum_perChannelPSD(incl_sub, incl_session, tasks, frequenciesDataFrame, absolutePsdDataFrame):
    """
    subject = str e.g. 024 
    frequenciesDataFrame = Dataframe of all frequencies of a subject (1st of tuple from perChannel_psd)
    absolutePsdDataFrame = Dataframe of all frequencies of a subject (2nd of tuple from perChannel_psd)
    incl_session = ['postop', 'fu3m', 'fu12m', 'fu18m']
    

    before using this function first run the method perChannel_psd() to get the tuple with frequencies and psd of the certain subject 

    this function will normalize the psd values of each power spectrum by dividing each psd by its total sum
    it will also plot the relative psd values of every channel in seperate plots for each session (postop, fu3m, fu12m, fu18m) 
    """

    sns.set()

    mainclass_sub = mainclass.PerceiveData(
        sub = incl_sub, 
        incl_modalities=["survey"],
        incl_session = incl_session,
        incl_condition = ["m0s0"],
        incl_task = ["rest"]
        )

    f_1to100Hz_dict = {} # dict with keys('postop_f_1to100Hz', 'fu3m_f_1to100Hz', 'fu12m_f_1to100Hz', 'fu18m_f_1to100Hz')
    psd_dict = {} # dict will be filled: keys('postop_relative_psd', 'fu3m_relative_psd', 'fu12_relative_psd', 'fu18m_relative_psd')
    f_relPsd_dict = {} # 
    sem_dict = {}

    # just get Frequencies 1-100 Hz
    f_1to100Hz = frequenciesDataFrame[1:104] #.iloc[:,0] #only take first column

    # get the channelnames of the first timepoint and the first task (e.g. postop, RestBSSuRingR -> 6 channels)
    task_ch_names = getattr(mainclass_sub.survey, incl_session[0])
    task_ch_names = task_ch_names.m0s0.rest.data[tasks[0]]

    # create grid for plots using the number of channelnames 
    # fig = plt.figure() -> figure is an instance of a single container containing all objects representing axes, graphics, text and labels    
    # axes = plt.axes() -> axes is a box which will contain the plot

    fig, axes = plt.subplots(len(task_ch_names.ch_names), 1, figsize=(20, 20)) # rows as many as channels, 1 column
    fig.tight_layout(pad=5.0)

    for t, tp in enumerate(incl_session):

        # select the right frequency and psd columns per timepoint and add them to the empty dictionaries
        f_1to100Hz_dict[f'{tp}_f_1to100Hz'] = f_1to100Hz.filter(like=tp) # filter DF by each session
        psd_dict[f'{tp}_psd'] = absolutePsdDataFrame[1:104].filter(like=tp) # filter DF by each session across 1-100Hz

        # get channel names by getting the column names from the DataFrame stored as values in the psd_dict
        ch_names = psd_dict[f'{tp}_psd'].columns

        for i, ch in enumerate(ch_names):

            # split the string of ch -> after LFP to get rid of the session in the channel name
            substring_beforeAndAfter_LFP = ch.split('LFP_')


            # the title of each plot is set to the channel e.g. "LFP_STN_R_13"
            axes[i].set_title(substring_beforeAndAfter_LFP[1]) 

            # get psd values from each channel column 
            absolute_psd = psd_dict[f'{tp}_psd'][ch] 
            f = f_1to100Hz_dict[f'{tp}_f_1to100Hz'][ch]

            # normalize psd values to total sum of the same power spectrum
            totalSum_psd = absolute_psd.sum()
            rel_psd = absolute_psd.div(totalSum_psd)
            percentage_psd = rel_psd * 100 

            # store the frequencies and percentage psd values in a dictionary 
            f_relPsd_dict[f'{tp}_{ch}'] = [f, percentage_psd]

            # calculate the SEM of psd values and store the sem values in a dictionary
            sem = np.std(percentage_psd)/np.sqrt(len(percentage_psd))
            sem_dict[f'sem_{tp}_{ch}'] = sem

            # get y-axis label and limits
            axes[i].get_ylabel()
            axes[i].get_ylim()

            # add errorbars
            # axes[t].errorbar(f, px, yerr=0.8, fmt='.k', color='lightgrey', ecolor='lightgrey')


            # find peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
            # peaks = scipy.signal.find_peaks(rel_psd, height=0.1) # height: peaks only above 0.1 will be recognized
            # peaks_height = peaks[1]["peak_heights"] # arraw of y-value of peaks = power
            # peaks_pos = f_1to100Hz[peaks[0]] # array of indeces on x-axis of peaks = frequency

            # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
            axes[i].plot(f, percentage_psd, label=ch)  # or np.log10(px)
            # make a shadowed line of the sem
            axes[i].fill_between(f, percentage_psd-sem, percentage_psd+sem, color='b', alpha=0.2)
            #axes[t].scatter(peaks_pos, peaks_height, color='r', s=15, marker='D')
                

    for ax in axes: 
        ax.legend(loc= 'upper right') # shows legend for each axes[t], loc sets the position of the spectrum
        ax.set(xlabel="Frequency", ylabel="relative PSD (% of total sum) +- SEM", ylim=(-1, 8)) # set y axis to -0.01 until 0.08(=8%)
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')


    plt.show() 

    # write DataFrame of frequencies and psd values of each channel per timepoint
    frequenciesrelDataFrame = pd.DataFrame({k: v[0] for k, v in f_relPsd_dict.items()}) # Dataframe of frequencies
    relativePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_relPsd_dict.items()}) # Dataframe of psd

    return {
        "frequenciesDataFrame":frequenciesrelDataFrame,
        "absolutePsdDataFrame":relativePsdDataFrame,
        "SEM":sem_dict
        }