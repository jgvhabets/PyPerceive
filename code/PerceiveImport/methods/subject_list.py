""" Create list of all subject folders inside of "Data" folder """

Import import PerceiveImport.methods.find_folders as find_folder

def find_subjects():
    """
    find_subjects is a method creating a list of all subject folders within your "Data" folder
    
    """
    _, data_path = find_folder.find_project_folder()
    subject_list = os.listdir(data_path)

    print(subject_list)
