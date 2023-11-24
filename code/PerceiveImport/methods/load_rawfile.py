""" 
loading the selection of raw files
    - .mat files loaded with MNE
    - .json files loaded with json.loads()
 """

from os.path import join, exists
from os import listdir
from mne.io import read_raw_fieldtrip
import json
import numpy as np

import PerceiveImport.methods.find_folders as find_folder


def load_matfile(sub: str, filename: str):
    """"
    Reads (perceived) .mat-file in FieldTrip
    structure using mne-function
    
    Input:
        - sub: str code of sub
        - filename: str of only .mat-filename
    
    Returns:
        - data: mne-object of .mat file
    """

    # Error check: 
    # Error if sub str is not exactly 3 letters e.g. 024
    assert len(sub) == 3, f'Subject string ({sub}) INCORRECT' 
    
    # Error if filename doesn´t end with .mat
    assert filename[-4:] == '.mat', (
        f'filename no .mat INCORRECT extension: {filename}'
    )

    # find the path to the raw_perceive folder of a subject
    datapath = find_folder.get_onedrive_path("sourcedata")
    datapath = join(datapath, f'sub-{sub}')
    
    data = read_raw_fieldtrip(
        join(datapath, filename),
        info={}, # add info here
        data_name='data',  # name of heading dict/ variable of original MATLAB object
    )
    
    return data


def find_all_present_jsons(sub):
    """
    get a list of all JSONs available in
    sourcedata
    """
    # search main source code subjects folder
    datapath = find_folder.get_onedrive_path("sourcedata")
    source_path = join(datapath, f'sub-{sub}')
    json_files = [file for file in listdir(source_path)
                  if file.endswith(".json")]
    # search additoinal raw jsons folder if present
    extra_json_path = join(source_path, 'raw_jsons')
    if exists(extra_json_path):
        json_files.extend([file for file in listdir(extra_json_path)
                            if file.endswith(".json")])
    # remove duplicates
    json_files = list(set(json_files))
    
    return json_files


def load_sourceJSON(sub: str, filename: str):

    """
    Reads source JSON file 

    Input:
        - subject = str, e.g. "024"
        - fname = str of filename, e.g. "Report_Json_Session_Report_20221205T134700.json"

    Returns: 
        - data: json.loads() loaded JSON file

    """

    # Error check: 
    # Error if sub str is not exactly 3 letters e.g. 024
    assert len(sub) == 3, f'Subject string ({sub}) INCORRECT' 
    
    # Error if filename doesn´t end with .mat
    assert filename[-5:] == '.json', (
        f'filename no .json INCORRECT extension: {filename}'
    )


    # find the path to the folder with raw JSONs of a subject
    datapath = find_folder.get_onedrive_path("sourcedata")
    json_path = join(datapath, f'sub-{sub}') # same path as to perceive files, all in sourcedata folder

    if exists(join(json_path, filename)):
        with open(join(json_path, filename), 'r') as f:
            json_object = json.loads(f.read())
        return json_object

    elif exists(join(json_path, 'raw_jsons', filename)):
        with open(join(json_path,'raw_jsons', filename), 'r') as f:
            json_object = json.loads(f.read())
        return json_object
    
    anom_name = filename.split('.')[0] + '_ANOM' + '.json'
    if exists(join(json_path, anom_name)):
        with open(join(json_path, anom_name), 'r') as f:
            json_object = json.loads(f.read())
        return json_object
    
    else:
        raise ValueError(f'JSON file ({filename}) not found '
                         f'in {json_path}, and "raw_jsons" folder')
    


def check_and_correct_lfp_missingData_in_json(streaming_data: dict):
    """"
    Function checks missing packets based on start and endtime
    of first and last received packets, and the time-differences
    between consecutive packets. In case of a missing packet,
    the missing time window is filled with NaNs.

    TODO: debug for BRAINSENSELFP OR SURVEY, STREAMING?
    BRAINSENSETIMEDOMAIN DATA STRUCTURE works?
    """
    Fs = streaming_data['SampleRateInHz']
    ticksMsec = convert_list_string_floats(streaming_data['TicksInMses'])
    ticksDiffs = np.diff(np.array(ticksMsec))
    data_is_missing = (ticksDiffs != 250).any()
    packetSizes = convert_list_string_floats(streaming_data['GlobalPacketSizes'])
    lfp_data = streaming_data['TimeDomainData']

    if data_is_missing:
        print('LFP Data is missing!! perform function to fill NaNs in')
    else:
        print('No LFP data missing based on timestamp '
            'differences between data-packets')

    data_length_ms = ticksMsec[-1] + 250 - ticksMsec[0]  # length of a pakcet in milliseconds is always 250
    data_length_samples = int(data_length_ms / 1000 * Fs) + 1  # add one to calculate for 63 packet at end
    new_lfp_arr = np.array([np.nan] * data_length_samples)

    # fill nan array with real LFP values, use tickDiffs to decide start-points (and where to leave NaN)

    # Add first packet (data always starts with present packet)
    current_packetSize = int(packetSizes[0])
    if current_packetSize > 63:
        print(f'UNKNOWN TOO LARGE DATAPACKET IS CUTDOWN BY {current_packetSize - 63} samples')
        current_packetSize = 63  # if there is UNKNOWN TOO MANY DATA, only the first 63 samples of the too large packets are included

    new_lfp_arr[:current_packetSize] = lfp_data[:current_packetSize]
    # loop over every distance (index for packetsize is + 1 because first difference corresponds to seconds packet)
    i_lfp = current_packetSize  # index to track which lfp values are already used
    i_arr = current_packetSize  # index to track of new array index
    
    i_packet = 1

    for diff in ticksDiffs:
        if diff == 250:
            # only lfp values, no nans if distance was 250 ms
            current_packetSize = int(packetSizes[i_packet])

            # in case of very rare TOO LARGE packetsize (there is MORE DATA than expected based on the first and last timestamps)
            if current_packetSize > 63:
                print(f'UNKNOWN TOO LARGE DATAPACKET IS CUTDOWN BY {current_packetSize - 63} samples')
                current_packetSize = 63

            new_lfp_arr[
                i_arr:int(i_arr + current_packetSize)
            ] = lfp_data[i_lfp:int(i_lfp + current_packetSize)]
            i_lfp += current_packetSize
            i_arr += current_packetSize
            i_packet += 1
        else:
            print('add NaNs by skipping')
            msecs_missing = (diff - 250)  # difference if one packet is missing is 500 ms
            
            secs_missing = msecs_missing / 1000
            samples_missing = int(secs_missing * Fs)
            # no filling with NaNs, bcs array is created full with NaNs
            i_arr += samples_missing  # shift array index up by number of NaNs left in the array
    
    # correct in case one sample too many was in array shape
    if np.isnan(new_lfp_arr[-1]): new_lfp_arr = new_lfp_arr[:-1]

    return new_lfp_arr


def convert_list_string_floats(
    string_list
):
    try:
        floats = [float(v) for v in string_list.split(',')]
    except:
        floats = [float(v) for v in string_list[:-1].split(',')]

    return floats



# #LFPMontage (sSurvey) is list with 30 sensed events -> different Survey Configs
# # plot PSD
# plt.plot(dat['LFPMontage'][2]['LFPFrequency'],
#          dat['LFPMontage'][2]['LFPMagnitude'])