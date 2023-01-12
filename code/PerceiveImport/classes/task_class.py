""" Task Class """

import pandas as pd
from dataclasses import dataclass


import PerceiveImport.methods.load_matfile as load_matfile

@dataclass (init=True, repr=True)
class taskClass:
    """
    Task Class 
    
    parameters:
        - sub: e.g. "021"
        - modality: "survey", "streaming", "timeline", "indefiniteStreaming" set in condition_class
        - session: "postop", "fu3m", "fu12m", "fu18m", "fu24m" set in condition_class
        - condition: "m0s0", "m1s0", "m0s1", "m1s1" set in condition_class
        - task: "rest", "tapping", "rota", "updrs", "monopolar" set in condition_class
        - metaClass: all original attributes set in Main_Class
        - meta_table: selected meta_table set in condition_class

    Returns:
        - sel_meta_table: session selected meta_table 
    
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
    

        
    

