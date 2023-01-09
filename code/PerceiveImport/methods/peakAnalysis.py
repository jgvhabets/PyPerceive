""" PEAK Analysis """

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
 
        
            #################### CREATE A BUTTERWORTH FILTER ####################

            # set filter parameters for band-pass filter
            filter_order = 5 # in MATLAB spm_eeg_filter default=5 Butterworth
            frequency_cutoff_low = 5 # 5Hz high-pass filter
            frequency_cutoff_high = 95 # 95 Hz low-pass filter
            fs = temp_data.info['sfreq'] # sample frequency: 250 Hz

            # create the filter
            b, a = scipy.signal.butter(filter_order, (frequency_cutoff_low, frequency_cutoff_high), btype='bandpass', output='ba', fs=fs)

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

                # store frequencies 1-100Hz and relative psd values in a dictionary
                f_psd_dict[f'{tp}_{ch}'] = [f, rel_psd]
                
                # get y-axis label and limits
                axes[t].get_ylabel()
                axes[t].get_ylim()

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
                    axes[t].scatter(highest_peak_pos, highest_peak_height, color='r', s=15, marker='D')

                    # store highest peak values of each frequency band in a dictionary
                    highest_peak_dict[f'{tp}_{ch}_highestPEAK_{frequency}'] = [highest_peak_pos, highest_peak_height]


                # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
                axes[t].plot(f, rel_psd, label=ch)  # or np.log10(px)

                # make a shadowed line of the sem
                axes[t].fill_between(f, rel_psd-sem, rel_psd+sem, color='b', alpha=0.2)

    
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


