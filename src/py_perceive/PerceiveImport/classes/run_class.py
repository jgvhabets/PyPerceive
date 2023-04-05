"""Run Class """

# import public packages
import pandas as pd
from dataclasses import dataclass
import warnings

# import own functions
import py_perceive.PerceiveImport.methods.load_rawfile as load_rawfile
from py_perceive.PerceiveImport.methods.ch_renaming import custom_mne_renaming

@dataclass (init=True, repr=True)
class runClass:
    """
    Run Class 
    
    parameters:
        - sub: e.g. "021"
        - modality: "survey", "streaming", "timeline", "indefiniteStreaming" set in condition_class
        - session: "postop", "fu3m", "fu12m", "fu18m", "fu24m" set in condition_class
        - condition: "m0s0", "m1s0", "m0s1", "m1s1" set in condition_class
        - task: "rest", "tapping", "rota", "updrs", "monopolar" set in condition_class
        - contact: a list of contacts to include ["RingR", "SegmIntraR", "SegmInterR", "RingL", "SegmIntraL", "SegmInterL", "Bip02", "Bip13", "Ring", "Segments"]
        - run: numerical order when recordings are performed multiple times
        - metaClass: all original attributes set in Main_Class
        - meta_table: selected meta_table set in condition_class

    Returns:
        - self.data: dictionary,  keys will be named after task, values will be the raw data of one perceived .mat file loaded with mne.io.read_raw_fieldtrip
    
    """
    
    sub : str
    modality: str
    session: str
    condition: str
    task: str
    run : str
    metaClass: any
    meta_table: pd.DataFrame
    contact: str = None
    import_json: bool = False


    def __post_init__(self,):

        ############ LOAD MATLAB FILES ############
        fname = self.meta_table['perceiveFilename'][0]
            
        # suppress RuntimeWarning
        warnings.simplefilter(action='ignore', category=RuntimeWarning)

        # load with mne.read_raw_fieldtrip()
        mne_raw = load_rawfile.load_matfile(self.sub, fname)
        
        # rename (parts of) ch names with bids Retune convention
        mne_raw = custom_mne_renaming(mne_raw)

        setattr(
            self,
            'data',
            mne_raw
        )


        if self.import_json:
            ############ LOAD SOURCE JSON FILES ############
            self.sourceJSON = {} # keys will be named after task, values will be the raw JSON file of the correct row of metadata
            
            fname = self.meta_table['report'][0]
  
            setattr(
                self,
                'json',
                load_rawfile.load_sourceJSON(self.sub, fname)
            )



        
    

