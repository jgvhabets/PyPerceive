import os
import numpy as np

def find_project_folder():
    """
    find_project_folder is a function to find the folder "PyPerceive_Project" on your local computer

    Return: tuple[str, str] -> project_path, data_path
    to only use one str use _ -> example: project_folder, _ = find_project_folder()
    """

    # from the cwd get path to PyPerceive_Project (=Git Repository)
    project_path = os.getcwd()
    while project_path[-18:] != 'PyPerceive_Project':
        project_path = os.path.dirname(project_path)
    
    data_path = os.path.join(project_path, 'Data')
    
    return project_path, data_path

def get_onedrive_path(
    folder: str = 'onedrive', sub: str = None
    ):
    """
    Device and OS independent function to find
    the synced-OneDrive folder where data is stored
    Folder has to be in ['onedrive', 'DATA-TEST', 'perceivedata', 'results']
    """

    folder_options = [
        'onedrive', 'perceivedata', 'results', 'raw_perceive'
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

    # get the onedrive folder containing "onedrive" and "charit" and add it to the path
    onedrive_f = [
        f for f in os.listdir(path) if np.logical_and(
            'onedrive' in f.lower(),
            'charit' in f.lower())
            ]

    path = os.path.join(path, onedrive_f[0]) # path is now leading to Onedrive folder


    # add the folder DATA-Test to the path and from there open the folders depending on input folder
    datapath = os.path.join(path, 'DATA_TEST')
    if folder == 'onedrive': 
        return datapath

    elif folder == 'perceivedata':
        return os.path.join(datapath, 'perceivedata')

    elif folder == 'results': # must be data or figures
        return os.path.join(datapath, 'results')
    
    elif folder == "raw_perceive": # containing all relevant perceive .mat files
        return os.path.join(datapath, "perceivedata", f"sub-{sub}", "raw_perceive")