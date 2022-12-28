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





def calculate_psd_surveym0s0(incl_sub, incl_modalities, incl_session, incl_condition, incl_task, tasks):
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

    results_path = findfolders.get_local_path(folder="results", sub=incl_sub)

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

                # transform the filtered time series data into power spectral density using Welch
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
        ax.axvline(x=13, color='r', linestyle='--')
        ax.axvline(x=35, color='r', linestyle='--')
        # ax.set(xlim=(10, 40), ylim=(-10, 4), xlabel="Frequency", ylabel="log10 Power")

    plt.show()
    
    # write DataFrame of frequencies and psd values of each channel per timepoint
    df_frequencies = pd.DataFrame({k: v[0] for k, v in f_psd_dict.items()})
    df_psdValues = pd.DataFrame({k: v[1] for k, v in f_psd_dict.items()})

    # write DF to json file
    df_frequencies.to_json(os.path.join(results_path, f'{incl_sub}_frequencies.json'), orient='columns', path_or_buf=f'{incl_sub}_frequencies.json')

    return df_frequencies, df_psdValues
