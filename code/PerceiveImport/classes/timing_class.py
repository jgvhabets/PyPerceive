### create a Timing class """

from dataclasses import dataclass

import os

import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.classes.Metadata_Class as metaclass

@dataclass (init=True, repr=True)
class timingClass:
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
    timing = str
    metaClass = any


    def __post_init__(self,):

        #_, self.data_path = find_folder.find_project_folder()
        #self.subject_path = os.path.join(self.data_path, self.sub)

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

