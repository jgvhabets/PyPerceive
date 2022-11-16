""" Medication Class"""



from dataclasses import dataclass

import PerceiveImport.classes.Metadata_Class as metaclass
import PerceiveImport.classes.Medication_Class as medclass

@dataclass (init=True, repr=True)
class medicationClass:
    """
    timing Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - timing: "Postop", "3MFU", "12MFU", "18MFU", "24MFU"

    Returns:
        - 
    
    """
    
    sub = str
    medication = str
    metaClass = any


    def __post_init__(self,):

        allowed_stimulation = ["Off", "On"]

        matpath_list = metaclass.MetadataClass.matpath_list # get the list of paths of the .mat filenames from the Metadata_Class

        PerceiveMetadata_selection = metaclass.MetadataClass.PerceiveMetadata_selection # get the preselected PerceiveMetadata DataFrame selection stored in the MetadataClass


        #select for timing:
        self.PerceiveMetadata_selection = PerceiveMetadata_selection[PerceiveMetadata_selection["timing"] == self.timing]
        
        matfile_list = self.PerceiveMetadata_selection["Perceive_filename"].to_list() # make a matfile_list of the values of the column "Perceive_filename" from the new selection of the Metadata DataFrame

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
            metaclass.MetadataClass(
                PerceiveMetadata_selection = self.PerceiveMetadata_selection)
        )

        setattr(
            self.metaClass,
            "matpath_list",
            metaclass.MetadataClass(
                matpath_list = self.matpath_list)
        )

        for med in metaclass.MetadataClass.incl_medication:

            assert med in allowed_medication, (
                f'inserted modality ({med}) should'
                f' be in {allowed_medication}'
            )

            setattr(
                self,
                med,
                medclass.timingClass( 
                    sub = self.sub,
                    timing = tim,
                    metaClass = self.metaClass
                )
            )  