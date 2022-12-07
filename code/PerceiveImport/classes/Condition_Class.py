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
    
    sub: str
    modality: str
    session: str
    condition: str
    metaClass: any
    meta_table: pd.DataFrame


    def __post_init__(self,):

        allowed_tasks = ["rest", "tapping", "updrs", "monopolar"]

        # continue to next class: Task_Class and set the attribute of the new selection of metaClass
        for task in self.metaClass.incl_task:

            # Error checking: if stim is not in allowed_stimulation -> Error message
            assert task.lower() in [t.lower() for t in allowed_tasks], (
                f'inserted modality ({task}) should'
                f' be in {allowed_tasks}'
            )

            # select out only meta_table for current session
            sel = [task.lower() in s.lower() for s in self.meta_table["task"]]
            sel_meta_table = self.meta_table[sel].reset_index(drop=True)

            if len(sel_meta_table) == 0:
                continue

            # set the task value for each task
            setattr(
                self,
                task,
                taskclass.taskClass(
                    sub=self.sub,
                    modality=self.modality,
                    session=self.session,
                    condition=self.condition,
                    task=task,
                    metaClass=self.metaClass,
                    meta_table=sel_meta_table,
                )
            )  