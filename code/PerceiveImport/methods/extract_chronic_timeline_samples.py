"""
Extract Chronic DBS Data

extract peak-LFPs, timestamps, and frequencies
from chronic BrainSense Timeline recordings
(sampled every 10 minutes in +/- 2 Hz band)
"""

# import functions
import json
from numpy import array, nan, logical_and, unique
from pandas import DataFrame, concat, isna
from dataclasses import dataclass, field
from itertools import compress
from datetime import datetime as dt

from PerceiveImport.methods.timezone_handling import (
    convert_times_to_local
)
from PerceiveImport.methods.load_rawfile import load_sourceJSON


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
        - overall_snap_list: list with one event dataclass per
            recorded event, duplicates removed.
    """
    # create overall empty base and columns chronic dataframe
    overall_chron_df, chron_cols = create_empty_chronic_df()
    overall_snap_list = []

    # loop over all josn files
    for file in json_files:
        # get dicts (Left/right) with values extracted from every json-file
        print(f'\n...START extraction chronic LFPs from: {file}')
        (sense_settings,
         overall_chron_df,
         overall_snap_list
        ) = extract_chronic_from_json(sub=sub, json_filename=file,
                                      overall_chron_df=overall_chron_df,
                                      chron_cols=chron_cols,
                                      overall_snap_list=overall_snap_list)

        if isinstance(sense_settings, str):
            if sense_settings == 'NO_SETTINGS':
                print(f'No Initial Group SensingChannel set in {file}')
                continue
    
    # remove duplicate events
    overall_snap_list = select_unique_events(overall_snap_list)

    # correct timezone timestamps at end
    local_times = convert_times_to_local(overall_chron_df.index)
    overall_chron_df['local_time'] = local_times
    # sort dataframe on utc timestamp index
    overall_chron_df = sort_chronic_df(overall_chron_df)

    # correct datatypes per column in chronic df
    for i_col, col in enumerate(overall_chron_df.keys()):
        if 'PSD' in col:
            overall_chron_df[col] = [int(v) for v in overall_chron_df[col]]
        if 'freq' in col or 'stimAmp' in col:
            overall_chron_df[col] = [float(v) for v in overall_chron_df[col]]
    

    return overall_chron_df, overall_snap_list


def sort_chronic_df(chron_df):
    """
    sorting dataframe on utc times, also converts
    utc time index into datetime timestamps
    """
    dtimes = [dt.strptime(t[:-1], '%Y-%m-%dT%H:%M:%S')
              for t in chron_df.index[:]]
    chron_df['utc_datetimes'] = dtimes
    chron_df = chron_df.set_index('utc_datetimes')
    chron_df = chron_df.sort_index()

    return chron_df


def create_empty_chronic_df(
    chronic_df_columns = ['local_time', 'PSD', 'freq',
                          'contact', 'group_name', 'stimAmp']
):
    # create columns names for dataframes    
    chron_cols = {}
    chron_cols['Left'] = chronic_df_columns[:1]+ [f'{c}_Left' for c in chronic_df_columns[1:]]
    chron_cols['Right'] = chronic_df_columns[:1]+ [f'{c}_Right' for c in chronic_df_columns[1:]]
    chron_cols['All'] = chronic_df_columns[:1] + chron_cols['Left'][1:] + chron_cols['Right'][1:]

    chron_df = DataFrame(columns=chron_cols['All'],)
    chron_df.index.name='utc_time'

    return chron_df, chron_cols


def extract_chronic_from_json(sub, json_filename, overall_chron_df,
                              chron_cols, overall_snap_list):
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
        - overall_chronc_df: every time added;
        - overall_snap_list: everything added
        
        # dict with ['Left', 'Right'], if available,
        #     Left is list with power values;
        # - peak_stimAmps: dict with ['Left', 'Right'], if available,
        #     Left is list with stim amplitude in mA
    """
    # load json-data
    dat = load_sourceJSON(sub, json_filename)

    # get frequency, contact, groupname
    sense_settings = get_sensing_freq_and_contacts(dat)

    # check for empty settings
    if isinstance(sense_settings, bool):
        if not sense_settings:
            return 'NO_SETTINGS', overall_chron_df, overall_snap_list
    
    # check for presence of SensingChannel
    elif logical_and(len(sense_settings['Left']) == 0,
                     len(sense_settings['Right']) == 0):
        # no sensing channel defined in Initial Groups of JSON
        return 'NO_SETTINGS', overall_chron_df, overall_snap_list

    # continues if SensingChannel was defined in Initial Groups

    # get LFP-values and timestamps, and parallel stimAmps (dicts with Left and Right)
    peak_times, peak_values, peak_stimAmps = get_chronic_LFPs_and_times(dat)
    # add extracted chronic values to overall-DataFrame
    overall_chron_df = add_chronic_values2df(
        sense_settings=sense_settings,
        chron_df=overall_chron_df, chron_cols=chron_cols,
        peak_times=peak_times,
        peak_values=peak_values,
        peak_stimAmps=peak_stimAmps,
        json_file=json_filename)

    # get SnapShot LFP-values and timestamps, and parallel stimAmps (dicts with Left and Right)
    new_snaps = get_snapshotEvents(dat, sub, sense_settings)
    print(f'JSON-file: {json_filename}: # new events: {len(new_snaps)}')
    if len(new_snaps) >= 1: overall_snap_list.extend(new_snaps)

    return sense_settings, overall_chron_df, overall_snap_list


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
    peak_values, peak_times, stim_amps = {}, {}, {}
    for s in ['Left', 'Right']:
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
    for side in ['Left', 'Right']:
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


def add_chronic_values2df(sense_settings, peak_times,
                          peak_values, peak_stimAmps,
                          json_file, chron_df, chron_cols):
    """
    Convert extracted chronic times, values, and
    stim-settings into dataframe
    """
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
                            f' for {side} side in {json_file}')
        
        # convert all rows into array for DataFrame creation
        values = array(values)
        file_df = DataFrame(data=values,
                            columns=chron_cols[side],
                            index=peak_times[side])
        file_df.index.name='utc_time'  # set index name
        
        # APPEND side-DATAFRAME FROM FILE TO OVERALL CHRONIC DATAFRAME
        idx_present = [new_i in chron_df.index for new_i in file_df.index]
        
        # add values per present index to ensure correct insertion            
        present_indices = file_df.index[idx_present]
        for ind in present_indices:
            chron_df.loc[ind, chron_cols[side]] = file_df.loc[ind].values
        
        # add values with new indices (if present)
        if sum(~array(idx_present)) > 0:
            chron_df = concat([chron_df, file_df[~array(idx_present)]], axis=0,)
    
    return chron_df


def get_snapshotEvents(dat, sub: str, sense_settings: dict,
                       LFP_events_key: str = 'LfpFrequencySnapshotEvents'):
    """
    actively induced LFP SnapShot extraction:
        DiagnosticData contains LfpFrequencySnapshotEvents
            - ...

    Input:
        - dat: imported JSON-file
    
    Returns:
        - ...
    """
    snap_list_out = []

    if LFP_events_key in dat['DiagnosticData'].keys():
        event_list = dat['DiagnosticData'][LFP_events_key]
        if len(event_list) == 0:
            print('event list is empty')
            return snap_list_out
        
        for event in event_list:
            snap_class = singleSnapshotEvent(sub=sub,
                                             sensing_settings=sense_settings,
                                             json_event_dict=event)
            snap_list_out.append(snap_class)
            print(f'created snap class, t={snap_class.time}'
                  f', contains LFP: {snap_class.contains_LFP}\n')
            
    # check if any chronic LFPs are present
    else:
        print(f'\tNo snapshot Events present, although settings were found'
              f' ({LFP_events_key} missing in DiagnosticData)')
    
    return snap_list_out


def select_unique_events(list_all_events):
    """
    selects out duplicates in LFP-events. Medtronic tablet stores
    the LFP data in Events only during the first connection,
    afterwards the event will still be stored every connection,
    but WITHOUT LFP-data. Therefore, many time duplicate arrise
    of Events without LFP data. 
    """
    # first take all unique events with LFP data
    lfp_events = [e for e in list_all_events if e.contains_LFP]
    uniq_lfp_times, uniq_lfp_idx = unique([e.time for e in lfp_events],
                                          return_index=True)
    uniq_lfp_events = list(array(lfp_events)[uniq_lfp_idx])
    # get all unique events W7O LFP data, not included yet
    nolfp_events = [e for e in list_all_events if not e.contains_LFP]
    uniq_nolfp_times, uniq_noLFP_idx = unique(
        [e.time for e in nolfp_events],
        return_index=True
    )
    uniq_nolfp_events = list(array(nolfp_events)[uniq_noLFP_idx])
    uniq_nolfp_events = [e for e in uniq_nolfp_events
                         if e.time not in uniq_lfp_times]
    # add events WITH and W/O LFP data
    all_uniq_events = uniq_lfp_events
    all_uniq_events.extend(uniq_nolfp_events)

    return all_uniq_events


@dataclass(init=True,)
class singleSnapshotEvent:
    """
    Stores all data for one single actively
    induced snapshot (Ereignis) event
    """
    sub: str
    sensing_settings: list
    json_event_dict: dict
    contains_LFP: bool = False
    LFP_events_key: str = field(
        default_factory=lambda:
        'LfpFrequencySnapshotEvents'
    )
    convert_times_local: bool = True

    def __post_init__(self,):
        self.time = self.json_event_dict['DateTime']
        if self.convert_times_local:
            self.time = convert_times_to_local(self.time)
        self.name = self.json_event_dict['EventName']
        # add neurophys if present
        if self.LFP_events_key in self.json_event_dict.keys():
            self.contains_LFP = True
            # get dict with present hemispheres
            ephys_temp = self.json_event_dict[self.LFP_events_key]
            # loop over hemispheres
            for side in ephys_temp.keys():
                lfp_side = side.split('.')[1].lower()  # get current hemisphere
                lfp_t = ephys_temp[side]['DateTime']  # get time of lfp, is 30 sec's of vs t_event (?)
                if self.convert_times_local:
                    lfp_t = convert_times_to_local(lfp_t)
                setattr(self,
                        f'lfp_{lfp_side}',
                        {'time': lfp_t,
                         'group': ephys_temp[side]['GroupId'],
                         'psd': ephys_temp[side]['FFTBinData'],
                         'freq': ephys_temp[side]['Frequency']})
                


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