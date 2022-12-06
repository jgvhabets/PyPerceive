""" Condition Class"""


import pandas as pd
from dataclasses import dataclass

import copy

# import PerceiveImport.classes.Metadata_Class as metaclass
import PerceiveImport.classes.Task_Class as taskclass

@dataclass (init=True, repr=True)
class conditionClass:
    """
    condition Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - condition: "M0S0", "M1S0", "M0S1", "M1S1"

    Returns:
        - 
    
    """
    
    sub : str
    condition: str
    metaClass: any


    def __post_init__(self,):

        allowed_tasks = ["Rest", "FT", "UPDRS"]

        # select all rows with the chosen condition in the column "condition" of the metadata DF
        sel = [self.condition == cond for cond in self.metaClass.metadata["condition"]]
        sel_meta_df = self.metaClass.metadata[sel].reset_index(drop=True)
        
        # create a copy of the metaclass metadata which will stay the same and won´t be modified by other classes
        self.sel_meta_df = copy.deepcopy(sel_meta_df)

        #store the new selection of the DataFrame into Metadata_Class
        setattr(self.metaClass, "metadata", sel_meta_df)


        # continue to next class: Task_Class and set the attribute of the new selection of metaClass
        for task in self.metaClass.incl_task:

            # Error checking: if stim is not in allowed_stimulation -> Error message
            assert task in allowed_tasks, (
                f'inserted modality ({task}) should'
                f' be in {allowed_tasks}'
            )

            # set the task value for each task
            setattr(
                self,
                task,
                taskclass.taskClass(
                    sub = self.sub,
                    task = task,
                    metaClass = self.metaClass
                )
            )  