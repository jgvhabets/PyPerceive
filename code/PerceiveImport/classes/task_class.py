""" Task Class """

import pandas as pd
from dataclasses import dataclass
from numpy import unique
import warnings

from PerceiveImport.classes.run_class import runClass
import PerceiveImport.classes.contact_class as contactclass


@dataclass (init=True, repr=True)
class taskClass:
    """
    Task Class 
    
    parameters:
        - sub: e.g. "021"
        - modality: "survey", "streaming", "timeline", "indefiniteStreaming" set in condition_class
        - session: "postop", "fu3m", "fu12m", "fu18m", "fu24m" set in condition_class
        - condition: "m0s0", "m1s0", "m0s1", "m1s1" set in condition_class
        - task: "rest", "fingerTap", "rota", "updrs", "monopolar" set in condition_class
        - contact: a list of contacts to include ["RingR", "SegmIntraR", "SegmInterR", "RingL", "SegmIntraL", "SegmInterL", "Bip02", "Bip13", "Ring", "Segments"]
        - metaClass: all original attributes set in Main_Class
        - meta_table: selected meta_table set in condition_class

    Returns:
        - sel_meta_table: session selected meta_table 
        - self.data: dictionary,  keys will be named after task, values will be the raw data of one perceived .mat file loaded with mne.io.read_raw_fieldtrip
    
    """
    
    sub : str
    modality: str
    session: str
    condition: str
    task: str
    metaClass: any
    meta_table: pd.DataFrame
    import_json: bool = False


    def __post_init__(self,):

        if self.modality.lower() == 'survey':
        
            allowed_contacts = [
                "RingR", "SegmIntraR", "SegmInterR",
                "RingL", "SegmIntraL", "SegmInterL", 
            ]

            # continue to next class: Contact_Class and set the attribute of the new selection of metaClass
            for cont in self.metaClass.incl_contact:

                # Error checking: if stim is not in allowed_stimulation -> Error message
                assert cont.lower() in [c.lower() for c in allowed_contacts], (
                    f'inserted contact ({cont}) should'
                    f' be in {allowed_contacts}'
                )
                
                # select out only meta_table for current session
                sel = [cont.lower() in s.lower() for s in self.meta_table["contacts"]]
                sel_meta_table = self.meta_table[sel].reset_index(drop=True)

                if len(sel_meta_table) == 0:
                    continue

                # set the task value for each task
                setattr(
                    self,
                    cont,
                    contactclass.contactClass(
                        sub=self.sub,
                        modality=self.modality,
                        session=self.session,
                        condition=self.condition,
                        task=self.task,
                        contact=cont,
                        metaClass=self.metaClass,
                        meta_table=sel_meta_table,
                    )
                )  

        # for "streaming" modality skip Contact class and go directly to Run_Class
        elif self.modality.lower() == 'streaming':
            
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
                        run=run_n,
                        metaClass=self.metaClass,
                        meta_table=sel_meta_table,
                        import_json = self.import_json
                    )
                )


        # for "indefiniteStreaming" modality skip Contact class and go directly to Run_Class
        elif self.modality.lower() == 'indefinitestreaming':
            
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
                        run=run_n,
                        metaClass=self.metaClass,
                        meta_table=sel_meta_table,
                        import_json = self.import_json
                    )
                )

