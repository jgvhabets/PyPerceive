"""
Anonymise Percept JSON files
"""

import json
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'PerceiveImport'))

from numpy import logical_and

from PerceiveImport.methods import find_folders


def anonymise_jsons():
    """
    Run from command line in PyPerceive folder (cd, working directory)

    Command: python code/utils/anonymise_jsons.py
    """

    anom_code = '_ANOM'

    path = find_folders.get_onedrive_path('onedrive')  # gives PerceptDataStructured
    
     
    path = os.path.join(path, 'sourcedata')


    for folder in os.listdir(path):

        if not os.path.isdir(os.path.join(path, folder)):
            continue

        if folder.startswith('sub-'):
            sub_dir = os.path.join(path, folder) # subject folder
            
            # loop over files in sub-folder
            for filename in os.listdir(sub_dir):
                
                if not filename.endswith('.json'): continue
                
                # check if JSON is already anonymised
                if anom_code in filename:
                    print(f'file {filename} already converted')
                    continue

                with open(os.path.join(sub_dir, filename), 'r') as f:
                    json_dict = json.load(f)

                del(json_dict['PatientInformation'])

                new_fname = filename.split('.')[0] + anom_code + '.json'

                with open(os.path.join(sub_dir, new_fname), 'w') as f:
                    json.dump(json_dict, f)
                
                os.remove(os.path.join(sub_dir, filename))

                print(f"Anonimysed JSON: {new_fname}")

        print(f"Finished folder {folder}")    


if __name__ == '__main__':

    anonymise_jsons()

