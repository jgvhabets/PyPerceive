"""
Extract Chronic DBS Data

extract peak-LFPs, timestamps, and frequencies
from chronic BrainSense Timeline recordings
(sampled every 10 minutes in +/- 2 Hz band)
"""

# import functions
import json

from PerceiveImport.methods.load_rawfile import load_sourceJSON

def extract_chronic_from_json(
    sub, json_filename
):
    """
    Main function to extract bandwidth peaks from
    chronic 'Timeline' data, including timestamps,
    LFP values, and Frequencies

    Input:
        - sub: e.g. '001'
        - json_filename: string containing the filename
            to extract from
    
    Returns:
        - df: pd dataframe containing times, LFP_left,
            freq_left, lfp_right, freq_right
    """
    # load json-data
    dat = load_sourceJSON(sub, json_filename)

    # get LFP-values and timestamps, and parallel stimAmps (dicts with Left and Right)
    peak_times, peak_values, peak_stimAmps = get_chronic_LFPs_and_Times(dat)

    # get frequency, contact, groupname
    sense_settings = get_sensing_freq_and_contacts(dat)
    print(sense_settings)

    return peak_times, peak_values, peak_stimAmps

def get_chronic_LFPs_and_Times(
    dat
):
    """
    JSON structure used for data extraction:
        DiagnosticData contains LFPTrendLogs
            - DateTime is timestamp
            - LFP is peak PSD in microVolt
            - AmplitudeInMilliAmps is stimulation amplitude

    Input:
        - dat: imported JSON-file
    
    Returns:
        - peak_times: dict with Left and Right
        - peak_values: dict with Left and Right
        - stim_amps: dict with Left and Right stim-
            amplitude parallel to recorded powers
    """
    sides = ['Left', 'Right']

    peak_values, peak_times, stim_amps = {}, {}, {}
    for s in sides:
        peak_values[s] = []
        peak_times[s] = []
        stim_amps[s] = []

    # collect present session per side
    # date_keys = {}
    for side in sides:
        # skip hemispheres not present
        if f'HemisphereLocationDef.{side}' not in dat['DiagnosticData']['LFPTrendLogs'].keys():
            print(f'{side} hemisphere not present')
            continue
        
        # if hemisphere is present
        hemi = dat['DiagnosticData']['LFPTrendLogs'][f'HemisphereLocationDef.{side}']
        
        # loop over present sessions
        for k in hemi.keys():
            print(f'Add session {k} from {side} hemisphere')
        
            # loop over present samples
            for sample in hemi[k]:
                peak_times[side].append(sample['DateTime'])
                peak_values[side].append(sample['LFP'])
                stim_amps[side].append(sample['AmplitudeInMilliAmps'])
    
    return peak_times, peak_values, stim_amps


def get_sensing_freq_and_contacts(dat):
    """
    JSON structure used for data extraction:
    'Groups' contains 'Initial' containing Group-Info.
    Groups contains these variable: [
        'GroupId', 'GroupName', 'ActiveGroup',
        'Mode', 'AdjustableParameter',
        'ProgramSettings', 'GroupSettings']
    if Sensing was activated, Group['ProgramSettings]
    contains 'SensingChannel'

    Input:
        - dat: imported JSON-file
    
    Returns:
        - peak_times: dict with Left and Right
        - peak_values: dict with Left and Right
        - stim_amps: dict with Left and Right stim-
            amplitude parallel to recorded powers
    """
    sense_settings = {}
    sides = ['Left', 'Right']
    for s in sides: sense_settings[s] = {}

    groups = dat['Groups']['Initial']  # groups[0]['GroupId'] -> 'GroupIdDef.GROUP_A' 

    # find active group
    for group_i in range(len(groups)):
        if groups[group_i]['ActiveGroup']:
            act_group_i = group_i
            act_group_name = groups[group_i]["GroupId"]
    
    # first try to extract freq and contact from active group
    group_settings = groups[act_group_i]['ProgramSettings']
    if 'SensingChannel' in group_settings.keys():
        # SensingChannel present in active group
        for i_ch in range(len(group_settings["SensingChannel"])):
            # loop over channels present (left / right)
            freq = group_settings["SensingChannel"][i_ch][
                'SensingSetup']['FrequencyInHertz']
            sense_side = group_settings["SensingChannel"][i_ch][
                'HemisphereLocation'].split('.')[1]
            contacts = group_settings["SensingChannel"][i_ch][
                'SensingSetup']['ChannelSignalResult']['Channel']
            sense_settings[sense_side] = {'freq': freq,
                                          'contacts': contacts,
                                          'group_name': act_group_name}
        
    else:
        print('\n\tNo SensingChannel in active group')

        # search for sensing channel in other groups
        # here the user should know that the Medtronic-
        # JSON-file doesnot provide 100% certainty about
        # the active program during the time of sensing
        for group_i in range(len(groups)):
            if group_i == act_group_i: continue  # skip active channel

            if not 'SensingChannel' in groups[group_i]['ProgramSettings'].keys():
                continue
            # if SensingChannel is present in keys
            group_settings = groups[group_i]['ProgramSettings']
            group_name = groups[group_i]["GroupId"]

            for i_ch in range(len(group_settings["SensingChannel"])):
                # loop over channels present (left / right)
                freq = group_settings["SensingChannel"][i_ch][
                    'SensingSetup']['FrequencyInHertz']
                sense_side = group_settings["SensingChannel"][i_ch][
                    'HemisphereLocation'].split('.')[1]
                contacts = group_settings["SensingChannel"][i_ch][
                    'SensingSetup']['ChannelSignalResult']['Channel']
                sense_settings[sense_side] = {'freq': freq,
                                            'contacts': contacts,
                                            'group_name': group_name}
                
    return sense_settings