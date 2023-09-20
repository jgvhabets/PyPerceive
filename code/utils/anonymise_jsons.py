"""
Anonymise Percept JSON files
"""

import json
import os
from numpy import logical_and




def anonymise_jsons():
    """
    Run from command line in PyPerceive folder (cd, working directory)

    Command: python code/utils/anonymise_jsons.py
    """

    anom_code = '_ANOM'

    path = get_onedrive_path('onedrive')  # gives PerceptDataStructured
    
     
    path = os.path.join(path, 'json_test')

    #    TODO:
    # go to source_data, loop over folder
    # for f in os.listdir(path):
    #     if not os.path.isdir(os.path.join(path, f)): continue
    # if FOLDER STARTSWITH SUB, loop over files in folder
    # if file endswith json, without ANOM_CODE, etc


    ####### possible loop #######
    # for folder in os.listdir(path):

    #     if not os.path.isdir(os.path.join(path, folder)):
    #         continue

    #     if folder.startswith('sub-'):
    #         sub_dir = os.path.join(path, folder) # subject folder
            
    #         # loop over files in sub-folder
    #         for f in os.listdir(sub_dir):

    #             if f.endswith('.json'):
                    
    #                 # check if JSON is already anonymised
    #                 if f[-10:-5] == anom_code:
    #                     print(f'file {f} already converted')
    #                     continue

    #                 else:
    #                     with open(os.path.join(path, file), 'r') as f:
    #                         json_dict = json.load(f)

    #                     del(json_dict['PatientInformation'])

    #                     new_fname = file.split('.')[0] + anom_code + '.json'

    #                     with open(os.path.join(path, new_fname), 'w') as f:
    #                         json.dump(json_dict, f)
                        
    #                     os.remove(os.path.join(path, file))

                

    for file in os.listdir(path):
        # loop over all files in folder
        if file.endswith('.json'):
            
            if file.split('.')[0].endswith(anom_code):
                print(f'file {file} already converted')
                continue
            
            with open(os.path.join(path, file), 'r') as f:
                json_dict = json.load(f)

            del(json_dict['PatientInformation'])

            new_fname = file.split('.')[0] + anom_code + '.json'

            with open(os.path.join(path, new_fname), 'w') as f:
                json.dump(json_dict, f)
            
            os.remove(os.path.join(path, file))



def get_onedrive_path(
    folder: str = 'onedrive', sub: str = None
):
    """
    Device and OS independent function to find
    the synced-OneDrive folder where data is stored
    Folder has to be in ['onedrive', 'Percept_Data_structured', 'sourcedata']
    """

    folder_options = [
        'onedrive', 'sourcedata'
        ]

    # Error checking, if folder input is in folder options
    if folder.lower() not in folder_options:
        raise ValueError(
            f'given folder: {folder} is incorrect, '
            f'should be {folder_options}')

    # from your cwd get the path and stop at 'Users'
    path = os.getcwd()

    while os.path.dirname(path)[-5:] != 'Users':
        path = os.path.dirname(path) # path is now leading to Users/username

    
    
    ####### in a specific case, if the Percept_Data_structured folder is in a specific directory #######
    if 'Charité - Universitätsmedizin Berlin' in os.listdir(path):

        path = os.path.join(path, 'Charité - Universitätsmedizin Berlin')

        # add the folder DATA-Test to the path and from there open the folders depending on input folder
        datapath = os.path.join(path, 'AG Bewegungsstörungen - Percept - Percept_Data_structured')
        if folder == 'onedrive': 
            return datapath

        elif folder == 'sourcedata':
            return os.path.join(datapath, 'sourcedata')

    ####### this should be the general case #######
    else:
        # get the onedrive folder containing "onedrive" and "charit" and add it to the path
        onedrive_f = [
            f for f in os.listdir(path) if np.logical_and(
                'onedrive' in f.lower(),
                'charit' in f.lower())
                ]

        path = os.path.join(path, onedrive_f[0]) # path is now leading to Onedrive folder


        # add the folder DATA-Test to the path and from there open the folders depending on input folder
        path = os.path.join(path, 'Percept_Data_structured')
        if folder == 'onedrive':

            assert os.path.exists(path), f'wanted path ({path}) not found'
            
            return path

        elif folder == 'sourcedata':

            path = os.path.join(path, 'sourcedata')
            if sub: path = os.path.join(path, f'sub-{sub}')

            assert os.path.exists(path), f'wanted path ({path}) not found'
                
            return path
    


if __name__ == '__main__':

    anonymise_jsons()

