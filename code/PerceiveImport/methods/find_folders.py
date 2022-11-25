import os
import numpy as np

def find_project_folder():
    """
    find_project_folder is a method to find the folder "PyPerceive_Project" on your computer

    Return: tuple[str, str] -> project_path, data_path
    to only use one str use _ -> example: project_folder, _ = find_project_folder()
    """
    project_path = os.getcwd()
    while project_path[-18:] != 'PyPerceive_Project':
        project_path = os.path.dirname(project_path)
    
    data_path = os.path.join(project_path, 'Data')
    
    return project_path, data_path

def get_onedrive_path(
    folder: str
    ):
    """
    Device and OS independent function to find
    the synced-OneDrive folder where data is stored
    Folder has to be in ['onedrive', 'DATA-TEST', 'perceivedata', 'results']
    """

    folder_options = [
        'onedrive', 'perceivedata', 'results'
        ]

    if folder.lower() not in folder_options:
        raise ValueError(
            f'given folder: {folder} is incorrect, '
            f'should be {folder_options}')

    path = os.getcwd()

    while os.path.dirname(path)[-5:] != 'Users':

        path = os.path.dirname(path) # path is now Users/username


    onedrive_f = [
        f for f in os.listdir(path) if np.logical_and(
            'onedrive' in f.lower(),
            'charit' in f.lower())
            ]

    path = os.path.join(path, onedrive_f[0])


    datapath = os.path.join(path, 'DATA-TEST')
    if folder == 'onedrive': 
        return datapath

    elif folder == 'perceivedata':
        return os.path.join(datapath, 'perceivedata')

    elif folder == 'results': # must be data or figures
        return os.path.join(datapath, 'results')