"""Run Class """

# import public packages
import pandas as pd
import numpy as np
from dataclasses import dataclass
import warnings

# import own functions
import PerceiveImport.methods.load_rawfile as load_rawfile
from PerceiveImport.methods.ch_renaming import custom_mne_renaming

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

        if not self.import_json:
            ############ LOAD MATLAB FILES ############
            fname = self.meta_table['perceiveFilename'][0]
            print(f'file name in runClass {fname}')
            # suppress RuntimeWarning
            warnings.simplefilter(action='ignore', category=RuntimeWarning)

            # load with mne.read_raw_fieldtrip()
            mne_raw = load_rawfile.load_matfile(self.sub, fname)
            print('mne raw loaded')
            # rename (parts of) ch names with bids Retune convention
            mne_raw = custom_mne_renaming(mne_raw)
            print('mne raw renamed')
            setattr(self, 'data', mne_raw)

        elif self.import_json:
            ############ LOAD SOURCE JSON FILES ############
            prc_data_codes = {
                'signal_test': 'CalibrationTests',
                'streaming': 'BrainSenseTimeDomain',
                'survey': 'LfpMontageTimeDomain',
                'indef_streaming': 'IndefiniteStreaming'
            }
            
            self.json_name = self.meta_table['report'][0]
            print('JSON name', self.json_name)
  
            # create attribute with full JSON content
            json_data = load_rawfile.load_sourceJSON(self.sub, self.json_name)
            setattr(self, 'json', json_data)

            # HERE WE HAVE TO EXTRACT THE RELEVANT INFO
            list_of_streamings = json_data[prc_data_codes[self.modality.lower()]]
            n_streamings = len(list_of_streamings)

            # CHOOSE DESIRED STREAMING DATA IN JSON TO IMPORT: FIND IN META DATA TABLE
            list_of_streamings = json_data[prc_data_codes[self.modality]]
            n_streamings = len(list_of_streamings)  # the JSON contains # n_streamings

            # the recording table should be used to find the correct order of the recordings, for the required/requested streaming file
            ### find Modality (Streaming)-recordings within this json, by using json_name
            temp = self.metaClass.orig_meta_table[self.metaClass.orig_meta_table['report'] == self.json_name]  # select on JSON name
            print(temp.keys())
            temp = temp[temp['contacts'] == 'Bip']  # select BS-Streamings (Bip)  # TODO: take into account incorrect documentation here (e.g. exclude all Survey codes)
            temp = temp.reset_index(drop=True)

            ### each Streaming recording contains 2 dictionaries in JSON, one for LEFT electrode, one for RIGHT electrode
            N_TABLE = temp.shape[0] * 2
            N_JSON = n_streamings

            assert N_TABLE == N_JSON, 'not matching number of Streaming-files in table vs JSON'
            print(f'CORRECT, {N_TABLE} bilateral recordings led to {N_JSON} files!')

            ### find order of required recording: match table with required meta-data of recording
            order_check = [
                (temp['session'] == self.session).values,
                (temp['condition'] == self.condition).values,
                (temp['task'] == self.task).values
            ]
            # find n-recording which is true for all objects
            N_REC = np.where(np.all(order_check, axis=0))[0][0]
            I_REC = [N_REC * 2, N_REC * 2 + 1]  # ASSUMING THAT EVERY REC LEADS TO TWO (BILAT) FILES
            SEL_STREAMS = [list_of_streamings[i] for i in I_REC]

            self.clean_lfp = [check_and_correct_lfp_missings_in_json(s) for s in SEL_STREAMS]



        
    

