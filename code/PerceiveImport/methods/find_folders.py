import os

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