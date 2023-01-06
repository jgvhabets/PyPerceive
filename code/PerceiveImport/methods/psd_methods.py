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

import PerceiveImport.classes.main_class as mainclass
import PerceiveImport.methods.find_folders as findfolders





def welch_psd_survey_m0s0(incl_sub, incl_session, tasks):
    """
    incl_sub = str e.g. "024"
    incl_session = list ["postop", "fu3m", "fu12m", "fu18m", "fu24m"]
    tasks = list ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']

    This function will first load the data from mainclass.PerceiveData using the input values.
    After loading the data the signal will be high-pass filtered by a Butterworth Filter of fifth order.
    
    From the filtered signal the psd values of every channel for each timepoint will be calculated by using Welch's method.

    For each frequency band alpha (), low beta () and high beta (), the highest Peak values (frequency and psd) will be seleted and saved in a DataFrame.

    All frequencies and relative psd values, as well as the values for the highest PEAK in each frequency band will be returned as a Dataframe in a dictionary: 
    {"frequenciesDataFrame":frequenciesDataFrame,
    "absolutePsdDataFrame":absolutePsdDataFrame,
    "SEM":sem_dict,
    "highestPEAK": highestPEAKDF,
    }
    """

    sns.set()

    mainclass_sub = mainclass.PerceiveData(
        sub = incl_sub, 
        incl_modalities= ["survey"],
        incl_session = incl_session,
        incl_condition = ["m0s0"],
        incl_task = ["rest"]
        )

    # results_path = findfolders.get_local_path(folder="results", sub=incl_sub)

    # tasks = ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
    time_points = incl_session
    # add error correction for sub and task??
    
    f_psd_dict = {} # dictionary with tuples of frequency and psd for each channel and timepoint of a subject
    sem_dict = {}
    highest_peak_dict = {}

    # set layout for figures: using the object-oriented interface
    fig, axes = plt.subplots(len(time_points), 1, figsize=(15, 15)) # subplot(rows, columns, panel number)
    fig.tight_layout(pad=5.0)

    for t, tp in enumerate(time_points):
        # t is indexing time_points, tp are the time_points

        for tk, task in enumerate(tasks): 
            # tk is indexing task, task is the input task

            # apply loop over channels
            temp_data = getattr(mainclass_sub.survey, tp) # gets attribute e.g. of tp "postop" from modality_class with modality set to survey
            temp_data = temp_data.m0s0.rest.data[tasks[tk]] # gets the mne loaded data from the perceive .mat BSSu, m0s0 file with task "RestBSSuRingR"


            # sample frequency: 250 Hz
            fs = temp_data.info['sfreq'] 


            #################### CREATE A BUTTERWORTH FILTER ####################

            # set filter parameters for high-pass filter
            filter_order = 5 # in MATLAB spm_eeg_filter default=5 Butterworth
            frequency_cutoff = 5 # 5Hz high-pass filter

            # create the filter
            b, a = scipy.signal.butter(filter_order, frequency_cutoff, btype='high', output='ba', fs=fs)

            # the title of each plot is set to the timepoint e.g. "postop"
            axes[t].set_title(tp)  

            # channels of Interest
            # only plot Right or Left
            # if hemisphere == "Right":

            # only plot channel of Interest
            # if ch_name in channelsOfInterest:


            # create signal per channel with Welch´s method and plot
            for i, ch in enumerate(temp_data.info.ch_names):
                
                #################### FILTER ####################

                # filter the signal by using the above defined butterworth filter
                filtered = scipy.signal.filtfilt(b, a, temp_data.get_data()[i, :]) # .get_data()

                #################### GET PSD VALUES BY USING wELCH'S METHOD ####################

                # transform the filtered time series data into power spectral density using Welch's method
                f, px = scipy.signal.welch(filtered, fs)  # Returns: f=array of sample frequencies, px= psd or power spectrum of x (amplitude)
                # density unit: V**2/Hz

                # store frequency and psd values in a dictionary
                f_psd_dict[f'{tp}_{ch}'] = [f, px]

                # calculate the SEM of psd values and store sem of each channel in dictionary
                sem = np.std(px)/np.sqrt(len(px))
                sem_dict[f'sem_{tp}_{ch}'] = sem
                

                # get y-axis label and limits
                axes[t].get_ylabel()
                axes[t].get_ylim()

                #################### PEAK DETECTION ####################
                # find all peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
                peaks = scipy.signal.find_peaks(px, height=0.1) # height: peaks only above 0.1 will be recognized

                # Error checking: if no peaks found, continue
                if len(peaks) == 0:
                    continue

                peaks_height = peaks[1]["peak_heights"] # np.arraw of y-value of peaks = power
                peaks_pos = f[peaks[0]] # np.array of indeces on x-axis of peaks = frequency

                # set the x-range for alpha, low beta and high beta
                alpha_range = (peaks_pos >= 8) & (peaks_pos <= 12) # alpha_range will output a boolean of True values within the alpha range
                lowBeta_range = (peaks_pos >= 13) & (peaks_pos <= 20)
                highBeta_range = (peaks_pos >= 21) & (peaks_pos <= 35)
                frequency_ranges = [alpha_range, lowBeta_range, highBeta_range]

                # loop through frequency ranges and get the highest peak of each frequency band
                for count, boolean in enumerate(frequency_ranges):

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
                    highest_peak_pos = peaksinfreq_pos[ix].item()

                    # plot only the highest peak within each frequency band
                    axes[t].scatter(highest_peak_pos, highest_peak_height, color='r', s=15, marker='D')

                    # store highest peak values of each frequency band in a dictionary
                    highest_peak_dict[f'{tp}_{ch}_highestPEAK_{frequency}'] = [highest_peak_pos, highest_peak_height]


                # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
                axes[t].plot(f, px, label=ch)  # or np.log10(px)

                # make a shadowed line of the sem
                axes[t].fill_between(f, px-sem, px+sem, color='b', alpha=0.2)

    
    for ax in axes: 
        ax.legend() # shows legend for each axes[t]
        ax.set(xlabel="Frequency", ylabel="mV^2/Hz +- SEM")
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')
    

    plt.show()
    
    # write DataFrame of all frequencies and psd values of each channel per timepoint
    frequenciesDataFrame = pd.DataFrame({k: v[0] for k, v in f_psd_dict.items()}) # Dataframe of frequencies
    absolutePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_psd_dict.items()}) # Dataframe of psd

    # write DataFrame of frequency and psd values of the highest peak in each frequency band
    highestPEAKDF = pd.DataFrame(highest_peak_dict) # Dataframe with 2 rows and columns each for one single power spectrum
    highestPEAKDF.rename(index={0: "PEAK_frequency", 1:"PEAK_absolutePSD"}, inplace=True) # rename the rows

    return {
        "frequenciesDataFrame":frequenciesDataFrame,
        "absolutePsdDataFrame":absolutePsdDataFrame,
        "SEM":sem_dict,
        "highestPEAK": highestPEAKDF,
        }



def welch_normalizedPsdToTotalSum_survey_m0s0(incl_sub, incl_session, tasks):
    """
    incl_sub = str e.g. "024"
    incl_session = list ["postop", "fu3m", "fu12m", "fu18m", "fu24m"]
    tasks = list ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']

    This function will first load the data from mainclass.PerceiveData using the input values.
    After loading the data the signal will be high-pass filtered by a Butterworth Filter of fifth order.
    
    From the filtered signal the psd values of every channel for each timepoint will be calculated by using Welch's method.

    For each frequency band alpha (), low beta () and high beta (), the highest Peak values (frequency and psd) will be seleted and saved in a DataFrame.

    All frequencies and relative psd values, as well as the values for the highest PEAK in each frequency band will be returned as a Dataframe in a dictionary: 
    {"frequenciesDataFrame":frequenciesDataFrame,
    "absolutePsdDataFrame":absolutePsdDataFrame,
    "SEM":sem_dict,
    "highestPEAK": highestPEAKDF,
    }
    """

    sns.set()

    mainclass_sub = mainclass.PerceiveData(
        sub = incl_sub, 
        incl_modalities= ["survey"],
        incl_session = incl_session,
        incl_condition = ["m0s0"],
        incl_task = ["rest"]
        )

    # results_path = findfolders.get_local_path(folder="results", sub=incl_sub)

    # tasks = ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
    time_points = incl_session
    # add error correction for sub and task
    # tasks = ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
    f_psd_dict = {} # dictionary with tuples of frequency and psd for each channel and timepoint of a subject
    sem_dict = {}
    highest_peak_dict = {}

    # set layout for figures: using the object-oriented interface
    fig, axes = plt.subplots(len(time_points), 1, figsize=(15, 15)) # subplot(rows, columns, panel number)
    fig.tight_layout(pad=5.0)

    for t, tp in enumerate(time_points):
        # t is indexing time_points, tp are the time_points

        for tk, task in enumerate(tasks): 
            # tk is indexing task, task is the input task

            # apply loop over channels
            temp_data = getattr(mainclass_sub.survey, tp) # gets attribute e.g. of tp "postop" from modality_class with modality set to survey
            temp_data = temp_data.m0s0.rest.data[tasks[tk]] # gets the mne loaded data from the perceive .mat BSSu, m0s0 file with task "RestBSSuRingR"
 

            # sample frequency: 250 Hz
            fs = temp_data.info['sfreq'] 

            #################### CREATE A BUTTERWORTH FILTER ####################

            # set filter parameters for high-pass filter
            filter_order = 5 # in MATLAB spm_eeg_filter default=5 Butterworth
            frequency_cutoff = 5 # 5Hz high-pass filter

            # create the filter
            b, a = scipy.signal.butter(filter_order, frequency_cutoff, btype='high', output='ba', fs=fs)

            # the title of each plot is set to the timepoint e.g. "postop"
            axes[t].set_title(tp)  

            # channels of Interest
            # only plot Right or Left
            # if hemisphere == "Right":

            # only plot channel of Interest
            # if ch_name in channelsOfInterest:


            # create signal per channel with Welch´s method and plot
            for i, ch in enumerate(temp_data.info.ch_names):
                
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

                #################### SELECT FREQUENCIES only from 1 to 100 Hz ####################

                # use numpy.logical_and to create a boolean array indicating which values are between 1 and 100
                mask_frequency1to100 = np.logical_and(f >= 1, f <= 100)

                # select only the frequency values that meet the condition 1-100Hz
                f_1to100Hz = f[mask_frequency1to100]

                # now select the corresponding psd values by using the same boolean mask
                rel_psd_1to100Hz = rel_psd[mask_frequency1to100]

                # store frequencies 1-100Hz and relative psd values in a dictionary
                f_psd_dict[f'{tp}_{ch}'] = [f_1to100Hz, rel_psd_1to100Hz]
                
                # get y-axis label and limits
                axes[t].get_ylabel()
                axes[t].get_ylim()

                #################### PEAK DETECTION ####################

                # find all peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
                # X must be a 1D array
                peaks = scipy.signal.find_peaks(rel_psd_1to100Hz, height=0.01) # height: peaks only above 0.1 will be recognized
                
                # Error checking: if no peaks found, continue
                if len(peaks) == 0:
                    continue

                # get the heights(=y values) and positions(=x values) of all peaks
                peaks_height = peaks[1]["peak_heights"] # np.array of y-value of peaks = power
                peaks_pos = f_1to100Hz[peaks[0]] # np.array of indeces on x-axis of peaks = frequency

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
                    axes[t].scatter(highest_peak_pos, highest_peak_height, color='r', s=15, marker='D')

                    # store highest peak values of each frequency band in a dictionary
                    highest_peak_dict[f'{tp}_{ch}_highestPEAK_{frequency}'] = [highest_peak_pos, highest_peak_height]


                # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
                axes[t].plot(f_1to100Hz, rel_psd_1to100Hz, label=ch)  # or np.log10(px)

                # make a shadowed line of the sem
                # axes[t].fill_between(f, rel_psd_1to100Hz-sem, rel_psd_1to100Hz+sem, color='b', alpha=0.2)

    
    for ax in axes: 
        ax.legend() # shows legend for each axes[t]
        ax.set(xlabel="Frequency", ylabel="relative PSD to total sum in %")
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')
    

    plt.show()
    
    # write DataFrame of all frequencies and psd values of each channel per timepoint
    frequenciesDataFrame = pd.DataFrame({k: v[0] for k, v in f_psd_dict.items()}) # Dataframe of frequencies
    absolutePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_psd_dict.items()}) # Dataframe of psd

    # write DataFrame of frequency and psd values of the highest peak in each frequency band
    highestPEAKDF = pd.DataFrame(highest_peak_dict) # Dataframe with 2 rows and columns each for one single power spectrum
    highestPEAKDF.rename(index={0: "PEAK_frequency", 1:"PEAK_relativePSD"}, inplace=True) # rename the rows

    return {
        "frequenciesDataFrame":frequenciesDataFrame,
        "absolutePsdDataFrame":absolutePsdDataFrame,
        "SEM":sem_dict,
        "highestPEAK": highestPEAKDF,
        }






#### watch out!! in this function you work with Dataframes!! so there are differences to the function above where you mostly work woth numpy arrays! ####
#### next task: not reuse Dataframes for Normalization but create another version of plotting normalized psd similar to the above function


def normalize_psd_toTotalSum(frequenciesDataFrame, absolutePsdDataFrame):

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
        psd_dict[f'{tp}_psd'] = absolutePsdDataFrame[1:104].filter(like=tp) # filter DF by each session across 1-100Hz

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


def perChannel_psd(incl_sub, incl_session, tasks):

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