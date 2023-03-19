"""
Extract Chronic DBS Data

extract peak-LFPs, timestamps, and frequencies
from chronic BrainSense Timeline recordings
(sampled every 10 minutes in +/- 2 Hz band)
"""

# import functions
import json
from numpy import array
from pandas import DataFrame, concat

from PerceiveImport.methods.load_rawfile import load_sourceJSON
from PerceiveImport.methods import timezone_handling


def extract_chronic_from_JSON_list(
    sub, json_files,
    # chron_df=None
):
    """
    create one dataframe with chronic Percept data
    from one subject based on a list of json file (data needs
    to be stored structurally for load_source_JSON() within
    extract_chronic_from_json())

    Input:
        - sub (str)
        - json_files (list)
        # - chron_df: optionally dataframe to add to
    
    Returns:
        - chron_df: DataFrame with all data, index is utc_time,
            columns are local_time, PSD, freq, contact, group_name,
            and stim_amp for all available sensed samples per side
    """
    # if not isinstance(chron_df, pd.DataFrame):
    chronic_df_columns = ['local_time', 'PSD', 'freq',
                            'contact', 'group_name', 'stim_amp']
    # create columns names for dataframes
    chron_cols = {}
    chron_cols['Left'] = chronic_df_columns[:1]+ [f'{c}_Left' for c in chronic_df_columns[1:]]
    chron_cols['Right'] = chronic_df_columns[:1]+ [f'{c}_Right' for c in chronic_df_columns[1:]]
    chron_cols['All'] = chronic_df_columns[:1] + chron_cols['Left'][1:] + chron_cols['Right'][1:]

    # create empty base chronic dataframe
    chron_df = create_empty_chronic_df(chronic_df_columns)

    for file in json_files:
        # get dicts (Left/right) with values extracted from every json-file
        try:
            (sense_settings,
             peak_times,
             peak_values,
             peak_stimAmps
            ) = extract_chronic_from_json(sub, file)
        except:
            print(f'{file} FAILED')
        
        # convert values into temp-DataFrame
        for side in ['Left', 'Right']:
            values = []
            if len(peak_times[side]) == 0: continue  # skip sides without recordings
            for i, t in enumerate(peak_times[side]):
                # loop over every row with values and per row to list
                values.append([
                    t,  # TODO: convert to local timezone from utc 
                    peak_values[side][i],
                    sense_settings[side]['freq'],
                    sense_settings[side]['contacts'],
                    sense_settings[side]['group_name'],
                    peak_stimAmps[side][i]
                ])
            values = array(values)  # convert all rows into array for DataFrame creation
            file_df = DataFrame(data=values,
                            columns=chron_cols[side],
                            index=peak_times[side])
            file_df.index.name='utc_time'  # set index name
            # APPEND DATAFRAME FROM FILE TO OVERALL CHRONIC DATAFRAME
            idx_present = [new_i in chron_df.index for new_i in file_df.index]
            # add values with present index to existing rows with same indices
            chron_df.loc[file_df.index[idx_present],
                         chron_cols[side]] = file_df.values[idx_present]
            # add values with new indices (if present)
            if sum(~array(idx_present)) > 0:
                chron_df = concat([chron_df, file_df[~array(idx_present)]], axis=0,)
            
            print(chron_df.shape)
    
    # correct timezone timestamps at end
    local_times = timezone_handling.convert_times_to_local(chron_df.index)
    chron_df['local_time'] = local_times

    return chron_df



def create_empty_chronic_df(chronic_df_columns):
    chron_cols = {}
    chron_cols['Left'] = chronic_df_columns[:1]+ [f'{c}_Left' for c in chronic_df_columns[1:]]
    chron_cols['Right'] = chronic_df_columns[:1]+ [f'{c}_Right' for c in chronic_df_columns[1:]]
    chron_cols['All'] = chronic_df_columns[:1] + chron_cols['Left'][1:] + chron_cols['Right'][1:]

    chron = DataFrame(columns=chron_cols['All'],)
    chron.index.name='utc_time'

    return chron


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
        - sense_settings: dict with ['Left', 'Right'], if available,
            Left is dict with ['freq', 'contacts', 'group_name'];
        - peak_times: dict with ['Left', 'Right'], if available,
            Left is list with string-timestamps;
        - peak_values: dict with ['Left', 'Right'], if available,
            Left is list with power values;
        - peak_stimAmps: dict with ['Left', 'Right'], if available,
            Left is list with stim amplitude in mA
    """
    # load json-data
    dat = load_sourceJSON(sub, json_filename)

    # get LFP-values and timestamps, and parallel stimAmps (dicts with Left and Right)
    peak_times, peak_values, peak_stimAmps = get_chronic_LFPs_and_Times(dat)

    # get frequency, contact, groupname
    sense_settings = get_sensing_freq_and_contacts(dat)
    print(json_filename)
    print(peak_times)

    return sense_settings, peak_times, peak_values, peak_stimAmps

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
            print(f'\nAdd session {k} from {side} hemisphere')
        
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
        print('\n\t### WARNING ###\n\tNo SensingChannel in active group'
              ', sensing info from NON-ACTIVE group is taken')

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