""" Session Class """

import pandas as pd
from dataclasses import dataclass

import copy

# import PerceiveImport.classes.Metadata_Class as metaclass
import PerceiveImport.classes.condition_class as condclass
#import PerceiveImport.classes.Task_Class as taskclass

@dataclass (init=True, repr=True)
class sessionClass:
    """
    session Class 
    
    parameters:
        - sub: e.g. "021"
        - modality: "survey", "streaming", "timeline", "indefiniteStreaming" set in modality_class
        - session: "postop", "fu3m", "fu12m", "fu18m", "fu24m" set in modality_class
        - metaClass: all original attributes set in Main_Class
        - meta_table: selected meta_table set in modality_class

    Returns:
        - sel_meta_table: session selected meta_table 
    
    """
    
    sub : str
    modality: str
    session: str
    metaClass: any
    meta_table: pd.DataFrame


    def __post_init__(self,):        
        
        allowed_condition = ["m0s0", "m1s0", "m0s1", "m1s1"]
        # continue to next class: Condition_Class and set the attribute of the new selection of metaClass
        for cond in self.metaClass.incl_condition:

            assert cond in allowed_condition, (
                f'inserted condition ({cond}) should'
                f' be in {allowed_condition}'
            )

            sel = [cond.lower() == c.lower() for c in self.meta_table["condition"]]
            sel_meta_table = self.meta_table[sel].reset_index(drop=True)
            
            # if no files are left after selecting, dont make new class
            if len(sel_meta_table) == 0:
                continue

            # set the condition value for each condition 
            setattr(
                self,
                cond,
                condclass.conditionClass(
                    sub=self.sub,
                    modality=self.modality,
                    session=self.session,
                    condition=cond,
                    metaClass=self.metaClass,
                    meta_table=sel_meta_table,
                ),
            )  

