""" Session Class """

import pandas as pd
from dataclasses import dataclass

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
    
    #sub = str
    session: str
    metaClass: any


    def __post_init__(self,):

        allowed_condition = ["M0S0", "M1S0", "M0S1", "M1S1"]
        #allowed_task = ["Rest", "UPDRS", "DirectionalStimulation", "FatigueTest"]

        

        # get the list of paths of the .mat filenames and the preselected PerceiveMetadata DataFrame from the Metadata_Class
        metadata_selection = self.metaClass.metadata_selection 

        # attempt to output a concatenated version of a dataframe if self.metaClass.incl_session > 1
        # session_dict = {}

        # for sessionInput in self.metaClass.incl_session:
    
        #     session_dict["Metadata_{0}".format(sessionInput)] =  metadata_selection[metadata_selection['session'] == sessionInput].reset_index(drop=True)
        #     # dictionary {"Metadata_Postop": Metadata_selection Postop, ...}
        
        # # from dictionary concatenate all dataframes together to one dataframe -> pd.concat
        # self.metadata_selection = pd.concat(session_dict.values(), ignore_index=True).reset_index(drop=True)
        
        # # select the input sessions, save the selection in metadata_selection 
        # self.matpath_list = []
        # matfile_list = self.metadata_selection["perceiveFilename"]

        # for path in self.metaClass.matpath_list:
        #     for f in matfile_list:
        #         if f in path:
        #             self.matpath_list.append(path)

        
        self.metadata_selection = metadata_selection[metadata_selection["session"] == self.session].reset_index(drop=True)
        
        #make a list out of the matfilenames in the first column "perceiveFilename"
        matfile_list = self.metadata_selection["perceiveFilename"].to_list() # make a matfile_list of the values of the column "Perceive_filename" from the new selection of the Metadata DataFrame

        #select from the matpath_list from the MetadataClass 
        #only append paths with the selected .mat filenames to the new self.matpath_list
        self.matpath_list = []
        for path in self.metaClass.matpath_list:
            for f in matfile_list:
                if f in path:
                    self.matpath_list.append(path)
        #einfacherer Weg ???


        # store the new values of the selected matpaths and DataFrame selection to the attributes stored in Metadata_Class
        setattr(
            self.metaClass,
            "metadata_selection",
            self.metadata_selection
        )

        setattr(
            self.metaClass,
            "matpath_list",
            self.matpath_list
            )
        
        condition_list = metadata_selection['condition'].unique().tolist() # list of the existing conditions in metadata column "condition"

        for cond in self.metaClass.incl_condition:

            assert cond in allowed_condition, (
                f'inserted modality ({cond}) should'
                f' be in {allowed_condition}'
            )

            # assert cond in condition_list, (
            #     f'inserted session ({cond}) has not been recorded'
            #     f' and can not be found in the metadata, which only contains sessions {condition_list}'
            #     )

            setattr(
                self,
                cond,
                condclass.conditionClass(
                    condition = cond,
                    metaClass = self.metaClass
                )
            )  

