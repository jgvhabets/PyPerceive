""" insert selected .mat files to an existing PerceiveMetadata.xlsx sheet """
import os
import pandas as pd


import PerceiveImport.methods.find_folders as find_folder

import warnings
import shutil



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
    MetadataDF.to_excel(os.path.join(subject_path, f'metadata_{sub}_perceiveFilename_path.xlsx'), sheet_name="perceiveFilename_path", index=False)

    return MetadataDF
       
    # bei LMTD filenames
    # if LMTD in filename and _ses- to _run- identical to other LMTD filenames -> append _1, _2 etc to file and run os.walk again


def read_excel_wOut_warning(path: str, sheet_name: None):
    """
    Load data from an Excel file, and surpress warning
    bceause of Excel-Dropdown menus
    """
    warnings.simplefilter(action='ignore', category=UserWarning)
    return pd.read_excel(path, sheet_name=sheet_name)



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
  






    # # load existing .xlsx file
    # wb = load_workbook('Perceive_Metadata.xlsx')
    # ws = wb.active # this gets the current active worksheet

    # # list I want to append to a specific column
    # matfile_list, _ = matfiles.select_matfiles(sub, rec_modality) 
    
    # # find the max row number from your Excel sheet
    # max_rows = ws.max_row

    # # define the start in +1 row after the last row in PerceiveMetadata.xlsx
    # row_start = max_rows + 1
    # column_index = 1 # define the column where to insert list

    # for i, value in enumerate(matfile_list, start=row_start):
    #     ws.cell(row=i, column=column_index).value = value

    # wb.save("Perceive_Metadata.xlsx")


# def insert_sub_to_Excel():
#     wb = load_workbook('Perceive_Metadata.xlsx')
#     ws = wb.active # this gets the current active worksheet



#     wb.save("Perceive_Metadata.xlsx")



# def insert_recmod_to_Excel():
#     wb = load_workbook('Perceive_Metadata.xlsx')
#     ws = wb.active # this gets the current active worksheet

#     rec_modality_dict = {
#         "Survey": "LMTD",
#         "Streaming": "BrainSense",
#         "Timeline": "CHRONIC"
#         }
    
#     for file in ws.iter_cols(min_col=1, max_col=1): # loop through every filename in column 1
#         if rec_modality_dict.values() in file:
#             print(rec_modality_dict.keys) # how can I specify to only get a specific key to a value in file???
    
#     # how can I add a specific key from rec_modality_dict to column 3 in a specific row??

#     wb.save("Perceive_Metadata.xlsx")

