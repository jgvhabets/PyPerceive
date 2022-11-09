import os

def find_project_folder():
    """
    DOC STRING
    """
    path = os.getcwd()
    while path[-18:] != 'PyPerceive_Project':
        path = os.path.dirname(path)
    
    data_path = os.path.join(path, 'Data')
    return path, data_path