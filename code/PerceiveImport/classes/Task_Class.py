""" Task Class """


from dataclasses import dataclass
#import mne 

# import PerceiveImport.classes.Metadata_Class as metaclass

@dataclass (init=True, repr=True)
class taskClass:
    """
    Task Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - task: "RestBSSuRingR", # BrainSense Survey Rest, Ring contacts 23, 01, 12, 02, 13, 03, right hemisphere
                "RestBSSuRingL", # BrainSense Survey Rest, Ring contacts 23, 01, 12, 02, 13, 03, left hemisphere
                "RestBSSuSegmInterR", # BrainSense Survey Rest, Segment contacts 1C2C, 1B2B, 1A2A (inter levels), right hemisphere
                "RestBSSuSegmInterL", # BrainSense Survey Rest, Segment contacts 1C2C, 1B2B, 1A2A (inter levels), left hemisphere
                "RestBSSuSegmIntraR", # BrainSense Survey Rest, Segment contacts 2A2C, 2B2C, 2A2B, 1A1C, 1B1C, 1A1B (intra levels), right hemisphere
                "RestBSSuSegmIntraL", # BrainSense Survey Rest, Segment contacts 2A2C, 2B2C, 2A2B, 1A1C, 1B1C, 1A1B (intra levels), left hemisphere
                "RestBSSt", # BrainSense Streaming Rest
                "FingerTapBSSt", # BrainSense Streaming Finger tapping
                "UPDRSBSSt", # BrainSense Streaming UPDRS
        - metaClass:

    Returns:
        - 
    
    """
    
    #sub = str
    task: str
    metaClass: any



    def __post_init__(self,):

        # get matpaths and PerceiveMetadata_selection from the Metadata_Class
        matpath_list = self.metaClass.matpath_list 
        metadata_selection = self.metaClass.metadata_selection 

        #select the PerceiveMetadata DataFrame for the correct task:
        self.metadata_selection = metadata_selection[metadata_selection["task"] == self.task].reset_index(drop=True)
        matfile_list = self.metadata_selection["Perceive_filename"].to_list() # make a matfile_list of the values of the column "Perceive_filename" from the new selection of the Metadata DataFrame

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
        

        #self.data = mne.
    

        
    

