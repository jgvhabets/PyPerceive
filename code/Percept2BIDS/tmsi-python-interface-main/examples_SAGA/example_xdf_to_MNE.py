'''
(c) 2022 Twente Medical Systems International B.V., Oldenzaal The Netherlands

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#######  #     #   #####   #
   #     ##   ##  #        
   #     # # # #  #        #
   #     #  #  #   #####   #
   #     #     #        #  #
   #     #     #        #  #
   #     #     #  #####    #

/**
 * @file ${example_xdf_to_MNE.py} 
 * @brief This example shows how to read data from a Xdf-file to an MNE-object.
 */


'''

import sys
from os.path import join, dirname, realpath
import mne

ipython = get_ipython()
ipython.magic("matplotlib qt")

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiFileFormats.file_readers import Xdf_Reader

reader=Xdf_Reader(add_ch_locs=True)
# When no filename is given, a pop-up window allows you to select the file you want to read. 
# You can also use reader=Xdf_Reader(full_path) to load a file. Note that the full file path is required here.
# add_ch_locs can be used to include TMSi EEG channel locations (in case xdf-file does not contain channel locations)

# An XDF-file can consist of multiple streams. The output data is of the tuple type, to allow for multi stream files.
mne_object, timestamps = reader.data, reader.time_stamps

# Extract data from the first stream
samples = mne_object[0]._data


#%% Basis plotting commands with MNE
mne_object[0].plot_sensors(ch_type='eeg', show_names=True) 
mne_object[0].plot(start=0, duration=5, n_channels=5, title='Xdf Plot') 
mne_object[0].plot_psd(fmin = 1, fmax = 100, picks = 'eeg')