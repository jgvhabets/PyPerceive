"""
Extract Chronic DBS Data

extract peak-LFPs, timestamps, and frequencies
from chronic BrainSense Timeline recordings
(sampled every 10 minutes in +/- 2 Hz band)
"""

# import functions
import json
from numpy import array, nan, logical_and
from pandas import DataFrame, concat, isna

from PerceiveImport.methods.load_rawfile import load_sourceJSON
from PerceiveImport.methods import timezone_handling


def extract_chronic_from_JSON_list(sub, json_files,):
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
                          'contact', 'group_name', 'stimAmp']
    # create columns names for dataframes
    chron_cols = {}
    chron_cols['Left'] = chronic_df_columns[:1] + [f'{c}_Left' for c in chronic_df_columns[1:]]
    chron_cols['Right'] = chronic_df_columns[:1] + [f'{c}_Right' for c in chronic_df_columns[1:]]
    chron_cols['All'] = chronic_df_columns[:1] + chron_cols['Left'][1:] + chron_cols['Right'][1:]

    # create empty base chronic dataframe
    chron_df = create_empty_chronic_df(chronic_df_columns)

    for file in json_files:
        # get dicts (Left/right) with values extracted from every json-file
        print(f'\n...START extraction chronic LFPs from: {file}')
        (sense_settings,
            peak_times,
            peak_values,
            peak_stimAmps
        ) = extract_chronic_from_json(sub, file)

        if isinstance(sense_settings, str):
            if sense_settings == 'NO_SETTINGS':
                print(f'No Initial Group SensingChannel set in {file}')
                continue

        # continues if Sensing Channel and LFP-values were found 
        
        # convert values into temp-DataFrame
        for side in ['Left', 'Right']:
            values = []
            if len(peak_times[side]) == 0: continue  # skip sides without recordings
            for i, t in enumerate(peak_times[side]):
                # loop over every row with values and per row to list
                try:
                    values.append([
                        t,
                        peak_values[side][i],
                        sense_settings[side]['freq'],
                        sense_settings[side]['contacts'],
                        sense_settings[side]['group_name'],
                        peak_stimAmps[side][i]
                    ])
                except KeyError:
                    # happens when either freq, contacts or group_name
                    # are not present in side dict sense setings
                    values.append([
                        t,
                        peak_values[side][i], nan, nan, nan,
                        peak_stimAmps[side][i]
                    ])
                    if i == 0:
                        print('##### WARNING #####\n\t'
                              'added NaN values for sense settings'
                              f' for {side} side in {file}')
            # convert all rows into array for DataFrame creation
            values = array(values)
            file_df = DataFrame(data=values,
                                columns=chron_cols[side],
                                index=peak_times[side])
            file_df.index.name='utc_time'  # set index name
            # APPEND DATAFRAME FROM FILE TO OVERALL CHRONIC DATAFRAME
            idx_present = [new_i in chron_df.index for new_i in file_df.index]
            # add values per present index to ensure correct insertion            
            present_indices = file_df.index[idx_present]
            for ind in present_indices:
                chron_df.loc[ind, chron_cols[side]] = file_df.loc[ind].values
            # add values with new indices (if present)
            if sum(~array(idx_present)) > 0:
                chron_df = concat([chron_df, file_df[~array(idx_present)]], axis=0,)
    
    # correct timezone timestamps at end
    local_times = timezone_handling.convert_times_to_local(chron_df.index)
    chron_df['local_time'] = local_times

    # correct datatypes per column
    for i_col, col in enumerate(chron_df.keys()):
        if 'PSD' in col: chron_df[col] = [int(v) for v in chron_df[col]]
        if 'freq' in col or 'stimAmp' in col:
            chron_df[col] = [float(v) for v in chron_df[col]]
        

    return chron_df



def create_empty_chronic_df(chronic_df_columns):
    chron_cols = {}
    chron_cols['Left'] = chronic_df_columns[:1]+ [f'{c}_Left' for c in chronic_df_columns[1:]]
    chron_cols['Right'] = chronic_df_columns[:1]+ [f'{c}_Right' for c in chronic_df_columns[1:]]
    chron_cols['All'] = chronic_df_columns[:1] + chron_cols['Left'][1:] + chron_cols['Right'][1:]

    chron = DataFrame(columns=chron_cols['All'],)
    chron.index.name='utc_time'

    return chron


def extract_chronic_from_json(sub, json_filename):
    """
    Main function to extract bandwidth peaks from
    chronic 'Timeline' data, including timestamps,
    LFP values, and Frequencies.

    Include only chronic data if there is a SensingChannel
    defined in the Initial Group Settings.
    This will prevent the inclusion of 'chronic' data points
    which are recorded during telemtry sessions while
    BSStreaming was active, without BS being active
    during the time prior to telemetry.

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

    # get frequency, contact, groupname
    sense_settings = get_sensing_freq_and_contacts(dat)

    # check for empty settings
    if isinstance(sense_settings, bool):
        if not sense_settings:
            return 'NO_SETTINGS', 'NA', 'NA', 'NA'

    # check for presence of SensingChannel
    if logical_and(len(sense_settings['Left']) == 0,
                   len(sense_settings['Right']) == 0):
        # no sensing channel defined in Initial Groups of JSON
        return 'NO_SETTINGS', 'NA', 'NA', 'NA'

    # continues if SensingChannel was defined in Initial Groups

    # get LFP-values and timestamps, and parallel stimAmps (dicts with Left and Right)
    peak_times, peak_values, peak_stimAmps = get_chronic_LFPs_and_times(dat)

    # get SnapShot LFP-values and timestamps, and parallel stimAmps (dicts with Left and Right)
    TO_DO = get_chronic_LFPs_and_times(dat)

    return sense_settings, peak_times, peak_values, peak_stimAmps


def get_chronic_LFPs_and_times(dat):
    """
    JSON structure used for chronic passive LFP data extraction:
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
    
    # check if any chronic LFPs are present
    if 'LFPTrendLogs' not in dat['DiagnosticData'].keys():
        print(f'\tNo chronic LFPs present, although settings were found'
              ' (LFPTrendLogs missing in DiagnosticData)')
        # returns empty dictionaries
        return peak_times, peak_values, stim_amps

    # collect present session per side
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


def get_chronic_SnapshotEvents(dat):
    """
    actively induced LFP SnapShot extraction:
        DiagnosticData contains LfpFrequencySnapshotEvents
            - ...

    Input:
        - dat: imported JSON-file
    
    Returns:
        - ...
    """
    if 'LfpFrequencySnapshotEvents' in dat['DiagnosticData'].keys():
        print('extract snapshots')
    
    return 'TODO'

def get_sensing_freq_and_contacts(dat):
    """
    JSON structure used for data extraction:
    'Groups' contains 'Initial' containing Group-Info.
    Groups contains these variable: [
        'GroupId', 'GroupName', 'ActiveGroup',
        'Mode', 'AdjustableParameter',
        'ProgramSettings', 'GroupSettings']
    if Sensing was activated, Group['ProgramSettings]
    contains 'SensingChannel' with list per set
    SensingChannel

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
    
    # CHECK FOR EMPTY GROUPS
    if len(groups) == 0: return False

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
              ', sensing info from NON-ACTIVE group is searched')

        # search for sensing channel in other groups
        # here the user should know that the Medtronic-
        # JSON-file doesnot provide 100% certainty about
        # the active program during the time of sensing
        for group_i in range(len(groups)):

            if group_i == act_group_i: continue  # skip active channel

            if not 'SensingChannel' in groups[group_i]['ProgramSettings'].keys():
                print(f'no sensing channel in group index {group_i}')
                continue
            # if SensingChannel is present in keys
            group_settings = groups[group_i]['ProgramSettings']
            group_name = groups[group_i]["GroupId"]
            
            print('\n\t### WARNING #2 ###\n\tSensingChannel from'
              f' inactive group {group_name} is taken')

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