""" contact Class """

import pandas as pd
from numpy import unique
from dataclasses import dataclass
import warnings

# import py_perceive.PerceiveImport.methods.load_rawfile as load_rawfile
from py_perceive.PerceiveImport.classes.run_class import runClass


@dataclass (init=True, repr=True)
class contactClass:
    """
    Contact Class 
    
    parameters:
        - sub: e.g. "021"
        - modality: "survey", "streaming", "timeline", "indefiniteStreaming" set in condition_class
        - session: "postop", "fu3m", "fu12m", "fu18m", "fu24m" set in condition_class
        - condition: "m0s0", "m1s0", "m0s1", "m1s1" set in condition_class
        - task: "rest", "tapping", "rota", "updrs", "monopolar" set in condition_class
        - contact: a list of contacts to include ["RingR", "SegmIntraR", "SegmInterR", "RingL", "SegmIntraL", "SegmInterL", "Bip02", "Bip13", "Ring", "Segments"]
        - metaClass: all original attributes set in Main_Class
        - meta_table: selected meta_table set in condition_class

    Returns:
        - self.data: dictionary,  keys will be named after task, values will be the raw data of one perceived .mat file loaded with mne.io.read_raw_fieldtrip
    
    """
    
    sub : str
    modality: str
    session: str
    condition: str
    task: str
    contact: str
    metaClass: any
    meta_table: pd.DataFrame
    import_json: bool = False


    def __post_init__(self,):

        # loop over available runs
        runs = unique(self.meta_table['run'])

        for run_n in runs:
            
            # select out only meta_table for current session
            sel = [run_n == s for s in self.meta_table["run"]]
            sel_meta_table = self.meta_table[sel].reset_index(drop=True)

            if len(sel_meta_table) == 0:
                continue

            setattr(
                self,
                f'run{run_n}',
                runClass(
                    sub=self.sub,
                    modality=self.modality,
                    session=self.session,
                    condition=self.condition,
                    task=self.task,
                    contact=self.contact,
                    run=run_n,
                    metaClass=self.metaClass,
                    meta_table=sel_meta_table,
                    import_json = self.import_json
                )
            )

        
    

