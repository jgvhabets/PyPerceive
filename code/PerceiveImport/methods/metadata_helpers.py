"""Import MetaData from metadata Tables"""

# import public packages
import os
import pandas as pd
from numpy import array
import warnings
import shutil

# import own functions
import PerceiveImport.methods.find_folders as find_folder



def read_excel_wOut_warning(path: str, sheet_name: None):
    """
    Load data from an Excel file, and surpress warning
    bceause of Excel-Dropdown menus
    """
    warnings.simplefilter(action='ignore', category=UserWarning)
    return pd.read_excel(path, sheet_name=sheet_name)


def clean_metadata_nanRows(
    table: pd.DataFrame, warn = False, sub = None):

    nan_rows = [
        pd.isna(table.iloc[row]).any()
        for row in range(table.shape[0])
    ]
    
    # return if no rows contain NaNs
    if sum(nan_rows) == 0: return table

    # correct if rows contain NaNs
    if warn: print(f'\n\t### WARNING: NaNs in Metadata Table sub-{sub} ###')

    for f in table["perceiveFilename"][nan_rows]:

        if warn: print(f'NaNs in: {f}')

    table = table[~array(nan_rows)].reset_index(drop=True)

    return table


def perceiveFilename_path_toExcel(sub):
    """ insert_matfiles_to_Excel() method:
    This method inserts all matfiles from a chosen subject (e.g. "021) to the first column of the Perceive_Metadata Excel sheet.
    Choose the recording modality ("rec_modality" = "Streaming", "Survey", "Timeline", "IndefiniteStreaming") of your choice.

    The matfilenames will be inserted after the last edited row of the .xlsx sheet.
    The Perceive_Metadata.xlsx file be saved.
    
    """
    perceivedata = find_folder.get_onedrive_path("perceivedata")
    subject_path = os.path.join(perceivedata, f'sub-{sub}')

    modality_abbreviations = {
            "survey": "LMTD",
            "streaming": "BrainSense", 
            "timeline": "CHRONIC",
            "indefiniteStreaming": "IS"
        }

    filename_path_tuple = []

    # append to matfile_list all .mat files with correct modality of subject
    for root, dirs, files in os.walk(subject_path): # walking through every root, directory and file of the given path
        for file in files: # looping through every file 
            for mod in modality_abbreviations:
                if file.endswith(".mat") and modality_abbreviations[mod] in file: # filter matfiles only for relevant modalities
                    filename_path_tuple.append([file, os.path.join(root, file)])


    # create new excel table only with perceiveFilenames and paths
    MetadataDF = pd.DataFrame(filename_path_tuple, columns=['perceiveFilename', 'path_to_perceive'])
    MetadataDF.to_excel(
        os.path.join(
            subject_path,
            f'metadata_{sub}_perceiveFilename_path.xlsx'
        ),
        sheet_name="perceiveFilename_path",
        index=False
    )

    return MetadataDF


def perceive_files_to_raw_perceive(sub):
    """ select all perceived .mat files from all sub-XX folders within the Data directory
    
    copy and paste all selected files with the correct modality_abbreviations into a raw_perceive folder

    """

    # get directory to Excel file with perceive filenames and paths
    perceivedata = find_folder.get_onedrive_path("perceivedata")
    subject_path = os.path.join(perceivedata, f'sub-{sub}')
    meta_table = pd.read_excel(os.path.join(subject_path, f'metadata_{sub}_perceiveFilename_path.xlsx'))

    # define directory to folder raw_perceive, where files will be "paste"
    raw_perceive = os.path.join(subject_path, "raw_perceive")
        
    # get paths to perceived files from meta_table 
    perceive_path = meta_table["path_to_perceive"]

    # copy paths and paste perceived files into new folder: raw_perceive
    
    for file in perceive_path:
        shutil.copy(file, raw_perceive)
  
