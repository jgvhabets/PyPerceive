""" Condition Class"""



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
    
    #sub = str
    condition: str
    metaClass: any


    def __post_init__(self,):

        allowed_tasks = ["RestBSSuRingR", "RestBSSuRingL", "RestBSSuSegmInterR", "RestBSSuSegmInterL",  "RestBSSuSegmIntraR", "RestBSSuSegmIntraL", "RestBSSt", "FingerTapBSSt", "UPDRSBSSt"]

        # get the list of paths of the .mat filenames and the preselected PerceiveMetadata DataFrame from the Metadata_Class
        matpath_list = self.metaClass.matpath_list 
        metadata_selection = self.metaClass.metadata_selection 


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
        for path in matpath_list:
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

        for task in self.metaClass.incl_task:

            # Error checking: if stim is not in allowed_stimulation -> Error message
            assert task in allowed_tasks, (
                f'inserted modality ({task}) should'
                f' be in {allowed_tasks}'
            )

            setattr(
                self,
                task,
                taskclass.taskClass(
                    task = task,
                    metaClass = self.metaClass
                )
            )  