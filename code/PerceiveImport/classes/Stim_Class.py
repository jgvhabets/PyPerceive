""" Stimulation Class """

from dataclasses import dataclass

# import PerceiveImport.classes.Metadata_Class as metaclass
import PerceiveImport.classes.Task_Class as taskclass

@dataclass (init=True, repr=True)
class stimulationClass:
    """
    Stimulation Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - stimulation: "On", "Off"
        - metaClass:

    Returns:
        - 
    
    """
    
    #sub = str
    stimulation: str
    metaClass: any


    def __post_init__(self,):

        allowed_task = ["Rest", "DirectionalStimulation", "FatigueTest"]

        # get the list of paths of the .mat filenames and the preselected PerceiveMetadata DataFrame from the Metadata_Class
        matpath_list = self.metaClass.matpath_list 
        PerceiveMetadata_selection = self.metaClass.PerceiveMetadata_selection 


        #select the PerceiveMetadata DataFrame for the correct medication:
        self.PerceiveMetadata_selection = PerceiveMetadata_selection[PerceiveMetadata_selection["stimulation"] == self.stimulation]
        matfile_list = self.PerceiveMetadata_selection["Perceive_filename"].to_list() # make a matfile_list of the values of the column "Perceive_filename" from the new selection of the Metadata DataFrame

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
            "PerceiveMetadata_selection",
            self.PerceiveMetadata_selection)

        setattr(
            self.metaClass,
            "matpath_list",
            self.matpath_list)


        for task in self.metaClass.incl_task:

            # Error checking: if stim is not in allowed_stimulation -> Error message
            assert task in allowed_task, (
                f'inserted modality ({task}) should'
                f' be in {allowed_task}'
            )

            setattr(
                self,
                task,
                taskclass.taskClass(
                    task = task,
                    metaClass = self.metaClass
                )
            )  