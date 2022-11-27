""" main function to upload and filter a metadata Dataframe and output a selection of paths to .mat files"""

# import packages
import os 

import pandas as pd
import xlrd

import PerceiveImport.FilterInput as filterinput


sub = filterinput.FilterInput["sub"]

def add_matfiles_toDF():


def load_metadata(sub):    
    path_local = 'c:\\Users\\jebe12\\Research\\Longterm_beta_project\\Data'
    dict_metadata = {}
    for s in sub:    
        subject_path = os.path.join(path_local, f'sub-{s}')
        metadata = pd.read_excel(os.path.join(subject_path, f'metadata_{s}.xlsx'), sheet_name="recordingInfo")

def add_paths_toDF():
    


def filter_sub():


def filter_modality():


def filter_session():


def filter_task():



