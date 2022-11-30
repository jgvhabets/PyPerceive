""" loading the selection of matfiles with MNE """

import mne
import mne_bids

# import PerceiveImport.methods.select_matfiles as matfiles


# input: list of matpath from metadata Dataframe column "path_to_perceive"
def load_perceiveFile(matpath_list):
    data = {}
    count = -1

    for path in matpath_list:
    
        count +=1

        data["raw_{0}".format(count)] = mne.io.read_raw_fieldtrip(
            path,
            info={},
            data_name='data'
            )


# # load selected files
# def load_timingdatatypematfiles(sub, timing, rec_modality):
#     matselection = matfiles.select_mat_timing_datatype(sub, timing, rec_modality)
#     for file in matselection[1]:  # matselection[1] stores a list of the selected .mat paths 
#         raw = mne.io.read_raw_fieldtrip(
#             file,
#             info={},
#             data_name='data'
#             )
#         return raw
        
# # store every loaded file in a different variable
# # e.g. matfile1, matfile2, matfile3 etc

# def load_datatypematfiles(sub, rec_modality):
#     matselection = matfiles.select_matdatatype(sub, rec_modality)
#     for file in matselection[1]:  # matselection[1] stores a list of the selected .mat paths 
#         raw = mne.io.read_raw_fieldtrip(
#             file,
#             info={},
#             data_name='data'
#             )
#         return raw


# def load_timingmatfiles(sub, timing):
#     matselection = matfiles.select_mattiming(sub, timing)
#     for file in matselection[1]:  # matselection[1] stores a list of the selected .mat paths 
#         raw = mne.io.read_raw_fieldtrip(
#             file,
#             info={},
#             data_name='data'
#             )
#         return raw