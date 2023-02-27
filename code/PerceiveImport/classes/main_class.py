"""Main Class"""

# import packages
import os 
from dataclasses import dataclass, field
import pandas as pd
from numpy import array

# import self-created packages
import PerceiveImport.methods.find_folders as find_folder
import PerceiveImport.methods.metadata_helpers as metaHelp
import PerceiveImport.classes.metadata_class as metadata
import PerceiveImport.classes.modality_class as modalityClass


import warnings

def read_excel_wOut_warning(path: str, sheet_name: None):
    """
    Load data from an Excel file, and surpress warning
    bceause of Excel-Dropdown menus
    """
    warnings.simplefilter(action='ignore', category=UserWarning)
    return pd.read_excel(path, sheet_name=sheet_name)


@dataclass(init=True, repr=True) 
class PerceiveData:
    """
    Main class to store Percept data
    
    parameters:
        - sub: number of subject e.g. "021" (make sure to use exactly three digits)
        - incl_modalities: a list of recording modalities to include ["survey", "streaming", "timeline", "indefiniteStreaming"] 
        - incl_timing: a list of timing sessions to include ["postop", "fu3m", "fu12m", "fu18m", "fu20m", "fu22m", "fu23m", "fu24m"]
        - incl_cond: a list of conditions to include  ["m0s0", "m1s0", "m0s1", "m1s1"]
        - incl_task: a list of tasks to include ["rest", "fingerTap", "fingerTapLeftHand", "fingerTapRightHand", "rota", "updrs", "WalkingMoveArt", "ChangingPositionMoveArt", "HeadMovementsMoveArt", "ArmMovementsMoveArt"]
        - incl_contact: a list of contacts to include ["RingR", "SegmIntraR", "SegmInterR", "RingL", "SegmIntraL", "SegmInterL", "Bip02", "Bip13", "Ring", "Segments"]

    post-initialized parameters:
    
    Returns:
        - 
    """
    
    # these fields will be initialized 
    sub: str             # note that : is used, not =  
    incl_modalities: list = field(default_factory=lambda: ["survey", "streaming", "timeline", "indefiniteStreaming"])  # default:_ if no input is given -> automatically input the full list
    incl_session: list = field(default_factory=lambda: ["postop", "fu3m", "fu12m", "fu18m", "fu20m", "fu22m", "fu23m", "fu24m"])
    incl_condition: list = field(default_factory=lambda: ["m0s0", "m1s0", "m0s1", "m1s1"])
    incl_task: list = field(default_factory=lambda: ["rest", "fingerTap", "fingerTapLeftHand", "fingerTapRightHand", "rota", "updrs", "WalkingMoveArt", "ChangingPositionMoveArt", "HeadMovementsMoveArt", "ArmMovementsMoveArt"])
    incl_contact: list = field(default_factory=lambda: ["RingR", "SegmIntraR", "SegmInterR", "RingL", "SegmIntraL", "SegmInterL", "Bip02", "Bip13", "Ring", "Segments"])
    import_json: bool = False
    warn_for_metaNaNs: bool = True

    # note that every defined method contains (self,) don´t forget the comma after self!
    def __post_init__(self,):  # post__init__ function runs after class initialisation
        
        allowed_modalities = ["survey", "streaming", "timeline", "indefiniteStreaming"] # this shows allowed values for incl_modalities

        self.perceivedata = find_folder.get_onedrive_path("sourcedata")
        self.subject_path = os.path.join(self.perceivedata, f'sub-{self.sub}')
        self.meta_table = metaHelp.read_excel_wOut_warning(
            os.path.join(
                self.subject_path,
                f'metadata_{self.sub}_perceiveFiles.xlsx'
            ),
            sheet_name="recordingInfo"
        )
        # clean rows with NaNs in MetaData Table
        self.meta_table = metaHelp.clean_metadata_nanRows(
            table=self.meta_table, warn=self.warn_for_metaNaNs, sub=self.sub
        )
        
        # define and store all variables in self.metaClass, from where they can continuously be called and modified from further subclasses
        self.metaClass = metadata.MetadataClass(
            sub = self.sub,
            incl_modalities = self.incl_modalities,
            incl_session = self.incl_session,
            incl_condition = self.incl_condition,
            incl_task = self.incl_task,
            incl_contact = self.incl_contact,
            orig_meta_table = self.meta_table,
        )

        # loop through every modality input in the incl_modalities list 
        # and set the modality value for each modality
        for mod in self.incl_modalities:

            assert mod in allowed_modalities, (
                f'inserted modality ({mod}) should'
                f' be in {allowed_modalities}'
            )

            modality_abbreviations_dict = {
                "survey": "LMTD",
                "streaming": "BrainSense", 
                "timeline": "CHRONIC",
                "indefiniteStreaming": "IS"
            }

            # select all rows with modality abbreviations in filename
            abbr = modality_abbreviations_dict[mod]  # current modality abbreviations
            sel = [abbr in fname for fname in self.metaClass.orig_meta_table["perceiveFilename"]]
            sel_meta_table = self.metaClass.orig_meta_table[sel].reset_index(drop=True)
            
            # if no files after selection, dont create subclasses
            if len(sel_meta_table) == 0:
                continue

            setattr(
                self, 
                mod, 
                modalityClass.Modality(
                    sub=self.sub,
                    modality=mod,
                    metaClass=self.metaClass,
                    meta_table=sel_meta_table,
                    import_json=self.import_json)
            )
            

