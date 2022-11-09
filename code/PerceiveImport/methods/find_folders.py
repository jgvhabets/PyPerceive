import os

def find_project_folder():
    """
    find_project_folder is a method to find the folder "PyPerceive_Project" on your computer

    Return: tuple[str, str] -> project_path, data_path
    to only use one str use _ -> example: project_folder, _ = find_project_folder()
    """
    path = os.getcwd()
    while path[-18:] != 'PyPerceive_Project':
        path = os.path.dirname(path)
    
    data_path = os.path.join(path, 'Data')
    return path, data_path