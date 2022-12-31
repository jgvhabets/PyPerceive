""" power spectral density methods """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import scipy
from scipy.signal import butter, filtfilt, freqz

import json
import os

import PerceiveImport.classes.main_class as mainclass
import PerceiveImport.methods.find_folders as findfolders





def welch_psd_survey_m0s0(incl_sub, incl_modalities, incl_session, incl_condition, incl_task, tasks):
    """
    subject = str e.g. 024 
    tasks = list e.g. ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']

    before using this function first load the data of the certain subject using 
    e.g. sub024 = mainclass.PerceiveData()

    this function will plot the psd of every channel for each timepoint 
    """

    sns.set()

    mainclass_sub = mainclass.PerceiveData(
        sub = incl_sub, 
        incl_modalities=incl_modalities,
        incl_session = incl_session,
        incl_condition = incl_condition,
        incl_task = incl_task
        )

    # results_path = findfolders.get_local_path(folder="results", sub=incl_sub)

    time_points = incl_session
    # add error correction for sub and task
    # tasks = ['RestBSSuRingR', 'RestBSSuSegmInterR', 'RestBSSuSegmIntraR','RestBSSuRingL', 'RestBSSuSegmInterL', 'RestBSSuSegmIntraL']
    f_psd_dict = {} # dictionary with tuples of frequency and psd for each channel and timepoint of a subject


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

            # set filter parameters for high-pass filter
            filter_order = 5 # in MATLAB spm_eeg_filter default=5 Butterworth
            frequency_cutoff = 5 # 5Hz high-pass filter

            # create the filter
            b, a = scipy.signal.butter(filter_order, frequency_cutoff, btype='high', output='ba', fs=fs)

            # the title of each plot is set to the timepoint e.g. "postop"
            axes[t].set_title(tp)  

            # create signal per channel with Welch´s method and plot
            for i, ch in enumerate(temp_data.info.ch_names):
                
                # create the filtered signal
                filtered = scipy.signal.filtfilt(b, a, temp_data.get_data()[i, :])

                # transform the filtered time series data into power spectral density using Welch's method
                f, px = scipy.signal.welch(filtered, fs)  # Returns: f=array of sample frequencies, px= psd or power spectrum of x (amplitude)
                # density unit: V**2/Hz

                # store frequency and psd values in new dictionary
                f_psd_dict[f'{tp}_{ch}'] = [f, px]


                # get y-axis label and limits
                axes[t].get_ylabel()
                axes[t].get_ylim()

                # add errorbars
                # axes[t].errorbar(f, px, yerr=0.8, fmt='.k', color='lightgrey', ecolor='lightgrey')


                # find peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
                peaks = scipy.signal.find_peaks(px, height=0.1) # height: peaks only above 0.1 will be recognized
                peaks_height = peaks[1]["peak_heights"] # arraw of y-value of peaks = power
                peaks_pos = f[peaks[0]] # array of indeces on x-axis of peaks = frequency

                # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
                axes[t].plot(f, px, label=ch)  # or np.log10(px)
                axes[t].scatter(peaks_pos, peaks_height, color='r', s=15, marker='D')
    
    for ax in axes: 
        ax.legend() # shows legend for each axes[t]
        ax.set(xlabel="Frequency")
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')
    

    plt.show()
    
    # write DataFrame of frequencies and psd values of each channel per timepoint
    frequenciesDataFrame = pd.DataFrame({k: v[0] for k, v in f_psd_dict.items()}) # Dataframe of frequencies
    absolutePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_psd_dict.items()}) # Dataframe of psd

    return frequenciesDataFrame, absolutePsdDataFrame




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

            # normalize psd values to total sum of the same power spectrum
            totalSum_psd = absolute_psd.sum()
            rel_psd = absolute_psd.div(totalSum_psd)
            percentage_psd = rel_psd * 100 

            # 
            f_relPsd_dict[f'{tp}_{ch}'] = [f, percentage_psd]

            # get y-axis label and limits
            axes[t].get_ylabel()
            axes[t].get_ylim()

            # add errorbars
            # axes[t].errorbar(f, px, yerr=0.8, fmt='.k', color='lightgrey', ecolor='lightgrey')


            # find peaks: peaks is a tuple -> peaks[0] = index of frequency?, peaks[1] = dictionary with keys("peaks_height") 
            # peaks = scipy.signal.find_peaks(rel_psd, height=0.1) # height: peaks only above 0.1 will be recognized
            # peaks_height = peaks[1]["peak_heights"] # arraw of y-value of peaks = power
            # peaks_pos = f_1to100Hz[peaks[0]] # array of indeces on x-axis of peaks = frequency

            # .plot() method for creating the plot, axes[0] refers to the first plot, the plot is set on the appropriate object axes[t]
            axes[t].plot(f, percentage_psd, label=ch)  # or np.log10(px)
            #axes[t].scatter(peaks_pos, peaks_height, color='r', s=15, marker='D')
                

    for ax in axes: 
        ax.legend(loc= 'upper right') # shows legend for each axes[t], loc sets the position of the spectrum
        ax.set(xlabel="Frequency", ylabel="relative PSD (% of total sum)", ylim=(-1, 8)) # set y axis to -0.01 until 0.08(=8%)
        ax.axvline(x=8, color='darkgrey', linestyle='--')
        ax.axvline(x=13, color='darkgrey', linestyle='--')
        ax.axvline(x=20, color='darkgrey', linestyle='--')
        ax.axvline(x=35, color='darkgrey', linestyle='--')


    plt.show() 

    # write DataFrame of frequencies and psd values of each channel per timepoint
    frequenciesrelDataFrame = pd.DataFrame({k: v[0] for k, v in f_relPsd_dict.items()}) # Dataframe of frequencies
    relativePsdDataFrame = pd.DataFrame({k: v[1] for k, v in f_relPsd_dict.items()}) # Dataframe of psd

    return frequenciesrelDataFrame, relativePsdDataFrame