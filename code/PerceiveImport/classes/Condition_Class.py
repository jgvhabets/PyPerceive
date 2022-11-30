""" Condition Class"""


import pandas as pd
from dataclasses import dataclass

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

        allowed_tasks = ["RestBSSuRingR", "RestBSSuRingL", "RestBSSuSegmInterR", "RestBSSuSegmInterL",  "RestBSSuSegmIntraR", "RestBSSuSegmIntraL", "RestBSSt", "FingerTapBSSt", "UPDRSBSSt"]

        # get the preselected PerceiveMetadata DataFrame from the Metadata_Class
        metadata_selection = self.metaClass.metadata_selection 

        # # attempt to output a concatenated version of a dataframe if self.metaClass.incl_condition > 1
        # condition_dict = {}

        # for conditionInput in self.condition:
        #     condition_dict["Metadata_{0}".format(conditionInput)] =  metadata_selection[metadata_selection['condition'] == conditionInput].reset_index(drop=True)
        #     # dictionary {"Metadata_M0S0": Metadata_selection M0S0, ...}
        
        # # from dictionary concatenate all dataframes together to one dataframe -> pd.concat
        # self.metadata_selection = pd.concat(condition_dict.values(), ignore_index=True).reset_index(drop=True)
        
        # # select the input sessions, save the selection in metadata_selection 
        # self.matpath_list = []
        # matfile_list = self.metadata_selection["perceiveFilename"]

        # # select only the paths included in the new matfile_list from paths of preselected matpath_list in MetaClass
        # for path in self.metaClass.matpath_list:
        #     for f in matfile_list:
        #         if f in path:
        #             self.matpath_list.append(path)


        #select the PerceiveMetadata DataFrame for the correct condition:
        
        # if "M0" in self.condition:
        #     metadata_selection_M0 = metadata_selection[metadata_selection["medState"] == "On"]
        
        # elif "M1" in self.condition: 
        #     metadata_selection_M1 = metadata_selection[metadata_selection["medState"] == "Off"]

        # else 
        

        self.metadata_selection = metadata_selection[metadata_selection["condition"] == self.condition].reset_index(drop=True)
        matfile_list = self.metadata_selection["perceiveFilename"].to_list() # make a matfile_list of the values of the column "Perceive_filename" from the new selection of the Metadata DataFrame

        # select from the matpath_list from the MetadataClass 
        # only append paths with the selected .mat filenames to the new self.matpath_list
        self.matpath_list = []
        for path in self.metaClass.matpath_list:
            for f in matfile_list:
                if f in path:
                    self.matpath_list.append(path)
        # einfacherer Weg ???


        # store the new values of the selected matpaths and DataFrame selection to the attributes stored in Metadata_Class
        
        setattr(
            self.metaClass,
            "metadata_selection",
            self.metadata_selection)

        setattr(
            self.metaClass,
            "matpath_list",
            self.matpath_list)

        #task_list = metadata_selection['task'].unique().tolist() # list of the existing sessions in metadata column "session"

        for task in self.metaClass.incl_task:

            # Error checking: if stim is not in allowed_stimulation -> Error message
            assert task in allowed_tasks, (
                f'inserted modality ({task}) should'
                f' be in {allowed_tasks}'
            )

            # assert task in task_list, (
            #     f'inserted session ({task}) has not been recorded'
            #     f' and can not be found in the metadata, which only contains sessions {task_list}'
            #     )

            setattr(
                self,
                task,
                taskclass.taskClass(
                    sub = self.sub,
                    task = task,
                    metaClass = self.metaClass
                )
            )  