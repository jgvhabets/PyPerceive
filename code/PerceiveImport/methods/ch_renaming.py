"""
Renaming Perceive Channelnames to
BIDS-Retune convention
"""

from mne import rename_channels

# dictionary of all possible channel names as keys, new channel names (Retune standard) as values
def get_rename_mapping():
    
    ch_renaming = {
        'LFP_Stn_0_3_RIGHT_RING':"LFP_R_03_STN_MT",
        'LFP_Stn_1_3_RIGHT_RING':"LFP_R_13_STN_MT",
        'LFP_Stn_0_2_RIGHT_RING':"LFP_R_02_STN_MT",
        'LFP_Stn_1_2_RIGHT_RING':"LFP_R_12_STN_MT",
        'LFP_Stn_0_1_RIGHT_RING':"LFP_R_01_STN_MT",
        'LFP_Stn_2_3_RIGHT_RING':"LFP_R_23_STN_MT",
        'LFP_Stn_0_3_LEFT_RING':"LFP_L_03_STN_MT",
        'LFP_Stn_1_3_LEFT_RING':"LFP_L_13_STN_MT",
        'LFP_Stn_0_2_LEFT_RING':"LFP_L_02_STN_MT",
        'LFP_Stn_1_2_LEFT_RING':"LFP_L_12_STN_MT",
        'LFP_Stn_0_1_LEFT_RING':"LFP_L_01_STN_MT",
        'LFP_Stn_2_3_LEFT_RING':"LFP_L_23_STN_MT",
        'LFP_Stn_1_A_1_B_RIGHT_SEGMENT':"LFP_R_1A1B_STN_MT",
        'LFP_Stn_1_B_1_C_RIGHT_SEGMENT':"LFP_R_1B1C_STN_MT",
        'LFP_Stn_1_A_1_C_RIGHT_SEGMENT':"LFP_R_1A1C_STN_MT",
        'LFP_Stn_2_A_2_B_RIGHT_SEGMENT':"LFP_R_2A2B_STN_MT",
        'LFP_Stn_2_B_2_C_RIGHT_SEGMENT':"LFP_R_2B2C_STN_MT",
        'LFP_Stn_2_A_2_C_RIGHT_SEGMENT':"LFP_R_2A2C_STN_MT",
        'LFP_Stn_1_A_1_B_LEFT_SEGMENT':"LFP_L_1A1B_STN_MT",
        'LFP_Stn_1_B_1_C_LEFT_SEGMENT':"LFP_L_1B1C_STN_MT",
        'LFP_Stn_1_A_1_C_LEFT_SEGMENT':"LFP_L_1A1C_STN_MT",
        'LFP_Stn_2_A_2_B_LEFT_SEGMENT':"LFP_L_2A2B_STN_MT",
        'LFP_Stn_2_B_2_C_LEFT_SEGMENT':"LFP_L_2B2C_STN_MT",
        'LFP_Stn_2_A_2_C_LEFT_SEGMENT':"LFP_L_2A2C_STN_MT",
        'LFP_Stn_1_A_2_A_RIGHT_SEGMENT':"LFP_R_1A2A_STN_MT",
        'LFP_Stn_1_B_2_B_RIGHT_SEGMENT':"LFP_R_1B2B_STN_MT",
        'LFP_Stn_1_C_2_C_RIGHT_SEGMENT':"LFP_R_1C2C_STN_MT",
        'LFP_Stn_1_A_2_A_LEFT_SEGMENT':"LFP_L_1A2A_STN_MT",
        'LFP_Stn_1_B_2_B_LEFT_SEGMENT':"LFP_L_1B2B_STN_MT",
        'LFP_Stn_1_C_2_C_LEFT_SEGMENT':"LFP_L_1C2C_STN_MT",
        "LFP_Stn_R_03":"LFP_R_03_STN_MT",
        "LFP_Stn_R_13":"LFP_R_13_STN_MT",
        "LFP_Stn_R_02":"LFP_R_02_STN_MT",
        "LFP_Stn_R_12":"LFP_R_12_STN_MT",
        "LFP_Stn_R_01":"LFP_R_01_STN_MT",
        "LFP_Stn_R_23":"LFP_R_23_STN_MT",
        "LFP_Stn_L_03":"LFP_L_03_STN_MT",
        "LFP_Stn_L_13":"LFP_L_13_STN_MT",
        "LFP_Stn_L_02":"LFP_L_02_STN_MT",
        "LFP_Stn_L_12":"LFP_L_12_STN_MT",
        "LFP_Stn_L_01":"LFP_L_01_STN_MT",
        "LFP_Stn_L_23":"LFP_L_23_STN_MT",
        'LFP_Stn_R_1A1B':"LFP_R_1A1B_STN_MT",
        'LFP_Stn_R_1B1C':"LFP_R_1B1C_STN_MT",
        'LFP_Stn_R_1A1C':"LFP_R_1A1C_STN_MT",
        'LFP_Stn_R_2A2B':"LFP_R_2A2B_STN_MT",
        'LFP_Stn_R_2B2C':"LFP_R_2B2C_STN_MT",
        'LFP_Stn_R_2A2C':"LFP_R_2A2C_STN_MT",
        'LFP_Stn_L_1A1B':"LFP_L_1A1B_STN_MT",
        'LFP_Stn_L_1B1C':"LFP_L_1B1C_STN_MT",
        'LFP_Stn_L_1A1C':"LFP_L_1A1C_STN_MT",
        'LFP_Stn_L_2A2B':"LFP_L_2A2B_STN_MT",
        'LFP_Stn_L_2B2C':"LFP_L_2B2C_STN_MT",
        'LFP_Stn_L_2A2C':"LFP_L_2A2C_STN_MT",
        'LFP_Stn_R_1A2A':"LFP_R_1A2A_STN_MT", 
        'LFP_Stn_R_1B2B':"LFP_R_1B2B_STN_MT", 
        'LFP_Stn_R_1C2C':"LFP_R_1C2C_STN_MT",
        'LFP_Stn_L_1A2A':"LFP_L_1A2A_STN_MT", 
        'LFP_Stn_L_1B2B':"LFP_L_1B2B_STN_MT", 
        'LFP_Stn_L_1C2C':"LFP_L_1C2C_STN_MT" 
    }


    return ch_renaming


def custom_mne_renaming(mneRaw):
    """"
    Function allows to rename full chnames,
    but also part of ch_names
    """

    rename_dict = {}

    chnames = mneRaw.ch_names.copy()

    rename_map = get_rename_mapping()

    chs_to_change = [c for c in chnames if c in rename_map.keys()]

    for ch_change in chs_to_change:

        sel = [ch_change in name for name in chnames]

        for i, name in enumerate(chnames):

            if sel[i]:
                rename_dict[name] = name.replace(
                    ch_change, rename_map[ch_change]
                )


    # # # rename channels using mne and the new selected mapping dictionary
    rename_channels(
        info=mneRaw.info,
        mapping=rename_dict,
        allow_duplicates=False
    )

    return mneRaw
