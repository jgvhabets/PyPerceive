### create a Timing class """

from dataclasses import dataclass

import PerceiveImport.classes.Metadata_Class as metaclass
import PerceiveImport.classes.Medication_Class as medclass

@dataclass (init=True, repr=True)
class timingClass:
    """
    timing Class 
    
    parameters:
        - sub:
        - timing: "Postop", "3MFU", "12MFU", "18MFU", "24MFU"
        - metaClass: 

    Returns:
        - 
    
    """
    
    sub = str
    timing = str
    metaClass = any


    def __post_init__(self,):

        allowed_medication = ["Off", "On"]

        
        # get the list of paths of the .mat filenames and the preselected PerceiveMetadata DataFrame from the Metadata_Class
        matpath_list = metaclass.MetadataClass.matpath_list 
        PerceiveMetadata_selection = metaclass.MetadataClass.PerceiveMetadata_selection 

        #select for timing, save the selection in PerceiveMetadata_selection 
        # make a list out of the matfilenames in the first column "Perceive_filename"
        self.PerceiveMetadata_selection = PerceiveMetadata_selection[PerceiveMetadata_selection["timing"] == self.timing]
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
                medclass.medicationClass( 
                    sub = self.sub,
                    medication = med,
                    metaClass = self.metaClass
                )
            )  





        #PerceiveMetadata_wb = load_workbook('Perceive_Metadata.xlsx')
        #PerceiveMetadata_ws = PerceiveMetadata_wb.active # this gets the current active worksheet


        # if matfilename from column matfile (1) in self.matfile_list (from RecModality Class)
        # AND cell in column timing (4) == self.timing
        # the add matfile to self.matfile_list
        # else delete matfile from self.matfile list

        # get rownumbers row_x - row_y of self.matfile_list (of chosen RecModality)
        # for name in column4 from row_x - row_y:
        #     if cell == self.timing:
        #         append matfilename(row_of_cell,column1) to self.matfile_list

        # for file in self.matfile_list:
        #     if cell in column_timing(4) in same row == self.timing:
        #         self.matfile_list.keep(file)
        #     else:
        #         self.matfile_list.delete(file)
        
        
        # is it possible to detect the path of a unique path? then we don´t have to safe the 

