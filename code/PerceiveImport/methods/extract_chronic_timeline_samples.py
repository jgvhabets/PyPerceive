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

    # get LFP-values and timestamps (dicts with Left and Right)
    peak_times, peak_values = get_chronic_LFPs_and_Times(dat)

    # get frequency


    return peak_times, peak_values

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
    """
    sides = ['Left', 'Right']

    peak_values, peak_times = {}, {}
    for s in sides:
        peak_values[s] = []
        peak_times[s] = []

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
    
    return peak_times, peak_values

