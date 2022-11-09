""" loading the selection of matfiles with MNE """

import mne
import mne_bids


# load selected files
def load_selection(matfiles):
    for file in matfiles[1]:  # matfiles[1] stores a list of the selected .mat paths 
        raw = mne.io.read_raw_fieldtrip(
            file,
            info={},
            data_name='data'
            )
        
# store every loaded file in a different variable
# e.g. matfile1, matfile2, matfile3 etc
    