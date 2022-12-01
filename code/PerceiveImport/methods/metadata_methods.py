""" main function to upload and filter a metadata Dataframe and output a selection of paths to .mat files"""

# import packages
import os 

import pandas as pd
import xlrd

import mne 
import mne_bids

# import PerceiveImport.FilterInput as filterinput
import PerceiveImport.methods.find_folders as find_folder


## sub = filterinput.FilterInput["sub"]


def perceiveFilename_path_toExcel(sub):
    """ perceiveFilename_path_Excel() method:
    This method saves all matfiles with corresponding paths from a chosen subject (e.g. "021) to a new Excel sheet.
    Choose the recording modality ("rec_modality" = "Streaming", "Survey", "Timeline").

    The matfilenames and corresponding paths will be inserted in the same row.
    The 'metadata_{sub}_perceiveFilename_path.xlsx' file be saved.
    
    """


    path_017_local = 'c:\\Users\\jebe12\\Research\\Longterm_beta_project\\Data\\sub-017'
    # perceivedata = find_folder.get_onedrive_path("perceivedata")
    # subject_path = os.path.join(self.perceivedata, f'sub-{sub}')

    
    modality_dict = {
            "Survey": "LMTD",
            "Streaming": "BSTD", 
            "Timeline": "CHRONIC"
        }

    filename_path_tuple = []

    # create a new DF with 2 columns: 'perceiveFilename', 'path_to_perceive'
    # walk through all existing perceived folders and select the .mat files of all modalities given in modality_dict
    for root, dirs, files in os.walk(path_017_local): # walking through every root, directory and file of the given path
        for file in files: # looping through every file 
            for mod in modality_dict:
                if file.endswith(".mat") and modality_dict[mod] in file: # filter matfiles only for relevant modalities
                    filename_path_tuple.append([file, os.path.join(root, file)])


    # create new excel table only with perceiveFilenames and paths
    MetadataDF = pd.DataFrame(filename_path_tuple, columns=['perceiveFilename', 'path_to_perceive'])
    MetadataDF.to_excel(os.path.join(path_017_local, f'metadata_{sub}_perceiveFilename_path.xlsx'), sheet_name="perceiveFilename_path", index=False)

    return MetadataDF


# load metadata of a defined subject as Dataframe from Excel
# sub = str of one subject
def load_metadata_matpath(sub):    
    # perceivedata = find_folder.get_onedrive_path("perceivedata")
    # subject_path = os.path.join(perceivedata, f'sub-{sub}')

    path_local = 'c:\\Users\\jebe12\\Research\\Longterm_beta_project\\Data'

    subject_path = os.path.join(path_local, f'sub-{sub}')
    metadata = pd.read_excel(os.path.join(subject_path, f'metadata_{sub}.xlsx'), sheet_name="recordingInfo")
    
    matpaths_random = []
    for root, dirs, files in os.walk(subject_path): # walking through every root, directory and file of the given path
        for file in files: # looping through every file 
            for f in metadata["perceiveFilename"]:
                if file == f:
                    matpaths_random.append(os.path.join(root, file))

    # matpath_list is in different order to idx from metadata, therefore add a new column to metadata and add paths corresponding to correct files
    # add new column "path_to_perceive" to Dataframe, input path as value, if tail=filename in path equals filename in perceiveFilename
    for path in matpaths_random:
    
        head, tail = os.path.split(path) # head = only the filename at the end of the path
        metadata.loc[metadata["perceiveFilename"] == tail, "path_to_perceive"] = path # df.loc[df.["cloumnname1"] condition, "newcolumn"] = values in newcolumn

    # get matpath_list in correct order from the new metadata column "path_to_perceive"
    matpath_list = metadata["path_to_perceive"].to_list()

    return metadata, matpath_list



# this function filters a metadata from input, which includes a column with paths already!!: modality=list, metadata=pd.DataFrame
# and outputs a new filtered matpath_selection and metadata_selection
def filter_modality(modality, metadata):
    modality_dict = {
            "Survey": "LMTD",
            "Streaming": "BSTD", 
            "Timeline": "CHRONIC"
        }
    
    matpath_selection = []
    matfile_list = []
        
    for filename in metadata["perceiveFilename"]:
        if modality_dict[modality] in filename:
            matfile_list.append(filename)
    
    metadata_selection = metadata[metadata["perceiveFilename"].isin(matfile_list)].reset_index(drop=True)
    matpath_selection = metadata_selection["path_to_perceive"].to_list()

    return metadata_selection, matpath_selection





def filter_session(session, metadata):

    metadata_selection = metadata[metadata["session"] == session].reset_index(drop=True)
    matpath_selection = metadata_selection["path_to_perceive"].to_list()
   
    return metadata_selection, matpath_selection





def filter_condition(condition, metadata):

    metadata_selection = metadata[metadata["condition"] == condition].reset_index(drop=True)
    matpath_selection = metadata_selection["path_to_perceive"].to_list()
   
    return metadata_selection, matpath_selection
  



def filter_task(task, metadata):
    metadata_selection = metadata[metadata["session"] == task].reset_index(drop=True)
    matpath_selection = metadata_selection["path_to_perceive"].to_list()
   
    return metadata_selection, matpath_selection
   


def load_mne_raw(matpath_selection):

    data = {}
    count = -1

    for f in matpath_selection:  # matselection stores a list of the selected .mat paths 
    
        count +=1

        data["raw_{0}".format(count)] = mne.io.read_raw_fieldtrip(
            f,
            info={},
            data_name='data'
            )
    
    return data

