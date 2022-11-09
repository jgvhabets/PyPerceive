""" List of all subjects  """

import os

import PerceiveImport.methods.find_project_folder as find_folder

def subject_list():
    """ 
    subject_list is a method that creates a list of all subject folders inside of your Data folder 
    """
    _, data_folder = find_folder.find_project_folder()
    subject_list = os.listdir(os.chdir(data_folder))

    print(subject_list)
