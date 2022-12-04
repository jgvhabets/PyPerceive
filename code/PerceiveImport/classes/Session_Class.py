""" Session Class """

import pandas as pd
from dataclasses import dataclass

import copy

# import PerceiveImport.classes.Metadata_Class as metaclass
import PerceiveImport.classes.Condition_Class as condclass
#import PerceiveImport.classes.Task_Class as taskclass

@dataclass (init=True, repr=True)
class sessionClass:
    """
    session Class 
    
    parameters:
        - sub:
        - session: "Postop", "FU3M", "FU12M", "FU18M", "FU24M"
        - metaClass: 

    Returns:
        - 
    
    """
    
    sub : str
    session: str
    metaClass: any


    def __post_init__(self,):

        allowed_condition = ["M0S0", "M1S0", "M0S1", "M1S1"]

        # select all rows with the chosen session in the column "session" of the metadata DF
        #sel = [self.metaClass.metadata["session"] == self.session]
        sel = [self.session == ses for ses in self.metaClass.metadata["session"]]
        sel_meta_df = self.metaClass.metadata[sel].reset_index(drop=True)
        

        # create a copy of the metaclass metadata which will stay the same and won´t be modified by other classes
        self.sel_meta_df = copy.deepcopy(sel_meta_df)


        #store the new selection of the DataFrame into Metadata_Class
        setattr(self.metaClass, "metadata", sel_meta_df)

        # loop through every condition input in the incl_condition list 
        # and set the condition value for each condition
        for cond in self.metaClass.incl_condition:

            assert cond in allowed_condition, (
                f'inserted modality ({cond}) should'
                f' be in {allowed_condition}'
            )

            # assert cond in condition_list, (
            #     f'inserted conditions ({cond}) has not been recorded'
            #     f' and can not be found in the metadata, which only contains conditions {condition_list}'
            #     )

            setattr(
                self,
                cond,
                condclass.conditionClass(
                    sub = self.sub,
                    condition = cond,
                    metaClass = self.metaClass
                )
            )  

