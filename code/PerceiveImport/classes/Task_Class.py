""" Task Class """

import pandas as pd
from dataclasses import dataclass


import PerceiveImport.methods.load_matfile as load_matfile

@dataclass (init=True, repr=True)
class taskClass:
    """
    Task Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - task:
        - metaClass:

    Returns:
        - 
    
    """
    
    sub : str
    modality: str
    session: str
    condition: str
    task: str
    metaClass: any
    meta_table: pd.DataFrame


    def __post_init__(self,):

        self.data = {}
        for row, fname in enumerate(self.meta_table['perceiveFilename']):

            dict_name = self.meta_table.iloc[row]['task']
            self.data[dict_name] = load_matfile.load_matfile(self.sub, fname)

            print('LOADED', fname)
    

        
    

