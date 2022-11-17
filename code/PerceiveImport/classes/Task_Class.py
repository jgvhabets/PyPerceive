""" Task Class """


from dataclasses import dataclass

# import PerceiveImport.classes.Metadata_Class as metaclass

@dataclass (init=True, repr=True)
class taskClass:
    """
    Task Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - task: "Rest", "DirectionalStimulation", "FatigueTest"
        - metaClass:

    Returns:
        - 
    
    """
    
    sub = str
    task = str
    metaClass = any


    def __post_init__(self,):

        # get matpaths and PerceiveMetadata_selection from the Metadata_Class
        matpath_list = self.metaClass.matpath_list 
        PerceiveMetadata_selection = self.metaClass.PerceiveMetadata_selection 

        #select the PerceiveMetadata DataFrame for the correct task:
        self.PerceiveMetadata_selection = PerceiveMetadata_selection[PerceiveMetadata_selection["task"] == self.task]
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
    

        # load the selection of .matfiles in self.matpath_list
    

