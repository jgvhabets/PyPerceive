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
    while project_path[-10:] != 'pyPerceive':
        project_path = os.path.dirname(project_path)
    
    data_path = os.path.join(project_path, 'data')
    
    return project_path, data_path


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



def get_local_path(folder: str, sub: str = None):
    """
    find_project_folder is a function to find the folder "Longterm_beta_project" on your local computer

    """

    folder_options = [
        'Research', 'Longterm_beta_project', 'results', 'figures'
        ]

    # Error checking, if folder input is in folder options
    #if folder.lower() not in folder_options:
        # raise ValueError(
        #     f'given folder: {folder} is incorrect, '
        #     f'should be {folder_options}')

    # from your cwd get the path and stop at 'Users'
    path = os.getcwd()

    while os.path.dirname(path)[-5:] != 'Users':
        path = os.path.dirname(path) # path is now leading to Users/username

    # get the Research folder and add it to the path

    path = os.path.join(path, 'Research') # path is now leading to Research folder


    # add the folder to the path and from there open the folders depending on input folder
    if folder == 'Research':
        return path

    elif folder == 'Longterm_beta_project': 
        return os.path.join(path, "Longterm_beta_project")

    elif folder == 'results':
        return os.path.join(path, "Longterm_beta_project", "results", f"sub-{sub}")

    elif folder == 'figures':
        return os.path.join(path, "Longterm_beta_project", "figures", f"sub-{sub}")
