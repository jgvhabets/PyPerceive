### create a Session class """

from dataclasses import dataclass

# import PerceiveImport.classes.Metadata_Class as metaclass
import PerceiveImport.classes.Condition_Class as condclass
#import PerceiveImport.classes.Task_Class as taskclass

@dataclass (init=True, repr=True)
class sessionClass:
    """
    timing Class 
    
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
        matpath_list = self.metaClass.matpath_list 
        metadata_selection = self.metaClass.metadata_selection 

        #select for timing, save the selection in PerceiveMetadata_selection 
        # make a list out of the matfilenames in the first column "Perceive_filename"
        
        self.metadata_selection = []
        matfile_list = []

        # if input is in exisiting sessions of metadata
        # create a seperate metadata_selection for each timepoint
        session_list = metadata_selection['session'].unique().tolist() # list of the existing sessions in metadata column "session"
        self.session_dict = {} 

        for sessionInput in self.metaClass.incl_session:

            assert sessionInput in session_list, (
                f'inserted session ({sessionInput}) has not been recorded'
                f' and can not be found in the metadata, which only contains sessions {session_list}'
                )

            # save metadata_selection Dataframe of each timepoint in seperate dataframes
            self.session_dict["Metadata_{0}".format(sessionInput)] =  metadata_selection[metadata_selection['session'] == sessionInput].reset_index(drop=True)
        


        # self.metadata_selection = metadata_selection[metadata_selection["session"] == self.session].reset_index(drop=True)
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
            self.metadata_selection
        )

        setattr(
            self.metaClass,
            "matpath_list",
            self.matpath_list
            )
        


        for cond in self.metaClass.incl_condition:

            assert cond in allowed_condition, (
                f'inserted modality ({cond}) should'
                f' be in {allowed_condition}'
            )

            setattr(
                self,
                cond,
                condclass.conditionClass(
                    condition = cond,
                    metaClass = self.metaClass
                )
            )  


        # jump to stim class
        # for stim in self.metaClass.incl_stim:

        #     # Error checking: if stim is not in allowed_stimulation -> Error message
        #     assert stim in allowed_stimulation, (
        #         f'inserted modality ({stim}) should'
        #         f' be in {allowed_stimulation}'
        #     )

        #     setattr(
        #         self,
        #         stim,
        #         stimclass.stimulationClass(
        #             stimulation = stim,
        #             metaClass = self.metaClass
        #         )
        #     ) 


        # # jump to task class
        # for task in self.metaClass.incl_task:

        #     # Error checking: if stim is not in allowed_stimulation -> Error message
        #     assert task in allowed_task, (
        #         f'inserted modality ({task}) should'
        #         f' be in {allowed_task}'
        #     )

        #     setattr(
        #         self,
        #         task,
        #         taskclass.taskClass(
        #             task = task,
        #             metaClass = self.metaClass
        #         )
        #     )   



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

