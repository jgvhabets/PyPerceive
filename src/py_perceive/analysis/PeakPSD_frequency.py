""" Peak PSD and Frequency """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import json
import os

import PerceiveImport.methods.find_folders as findfolders


# Matplotlib: set the style
plt.style.use('seaborn-whitegrid')

def highestPeakValues(incl_sub: str, hemisphere: str, frequencyBands: list, pickChannels: list, highestPeakDataframe: any, PeakAttribute: str ):

    """
    Restructuring Dataframe into different frequency bands and plotting Peak Frequencies or PSD 

    Input: 
        - sub: str e.g. ["024"]
        - hemisphere: str e.g. "Right"
        - frequencyBands = list e.g. ["alpha", "lowBeta", "highBeta"]
        - pickChannels = e.g. ['13', '02', '12', '01', '23', 
            '1A1B', '1B1C', '1A1C', '2A2B', '2B2C', '2A2C', 
            '1A2A', '1B2B', '1C2C']
        - highestPeakDataframe = pd.Dataframe (returned from BSSuAbsolutePsd or BSSuRelativePsd function)
        - PeakAttribute = PeakFrequency or PeakPsd

    """

    

    chan_freq_dict = {}
    local_path = findfolders.get_local_path(folder="figures", sub=incl_sub)

    # Layout: subplot for every frequency band, 1 column
    fig, axes = plt.subplots(len(frequencyBands), 1, figsize=(15, 15))
    fig.tight_layout(pad=5.0)

    for f, freq in enumerate(frequencyBands):

        for c, chan in enumerate(pickChannels):

            Dataframe_perChannelAndFrequency = highestPeakDataframe[highestPeakDataframe.index.str.contains(f"_{chan}_.*{freq}")] # select only rows containing the right channel and frequency band
            session = Dataframe_perChannelAndFrequency["session"]
            Peak_Frequency = Dataframe_perChannelAndFrequency["PEAK_frequency"]
            Peak_PSD = Dataframe_perChannelAndFrequency["PEAK_relativePSD"]

            # store filtered Dataframe of each channel and frequency band
            chan_freq_dict[f"{freq}_{chan}"] = Dataframe_perChannelAndFrequency # select only rows containing the right channel and frequency band

            # plot in each frequency band subplot
            axes[f].set_title(f"{freq}", fontsize=20)
            axes[f].get_ylabel()
            axes[f].get_ylim()

            # depending on PeakAttribute Input: plot either Peak frequencies or Peak Psd values
            if PeakAttribute == "PeakFrequency":

                axes[f].plot(session, Peak_Frequency, label=f"{chan}", marker="o")
            
            elif PeakAttribute == "PeakPsd":

                axes[f].plot(session, Peak_PSD, label=f"{chan}", marker="o")
                # axes[f].bar(session, Peak_PSD, width=0.1)


            # axes[f].hist(session, PeakFrequency, density=True, histtype="bar", label=f"{chan}")


    font = { "size": 16}

    for ax in axes:
        ax.legend(loc="upper right")
        ax.set_xlabel("Follow-up timepoints", fontdict=font)

        if PeakAttribute == "PeakFrequency":
            ax.set_ylabel("Frequency [Hz] of the Peak", fontdict=font)

        elif PeakAttribute == "PeakPsd":
            ax.set_ylabel("relative PSD [%] of the Peak", fontdict=font)
        

    #fig.write_image("PeakFrequencyOverTime.png",format="png", width=1000, height=600, scale=3)

    print(local_path)
    fig.savefig(local_path + f"\sub{incl_sub}_{hemisphere}_highestPeakValues_{PeakAttribute}_{pickChannels}.png")
    
    plt.show()