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
 * @file ${example_read_data.py} 
 * @brief This example shows how to read data from a .Poly5 file. Next to this, 
 * the channel reordering strategy for the Textile HD-EMG grid is demonstrated.
 * Finally, conversion to an MNE-Python object is shown.
 *
 */


'''

import sys
from os.path import join, dirname, realpath, exists
import json
import numpy as np
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiFileFormats.file_readers import Poly5Reader

data=Poly5Reader()
# When no arguments are given, a pop-up window allows you to select the file you want to read. 
# You can also use data=Poly5Reader(full_path) to load a file. Note that the full file path is required here.

# Extract the samples and channel names from the Poly5Reader object
samples = data.samples
ch_names = data.ch_names

#%% Reordering textile grid channels

isTextileGrid = False

if isTextileGrid:
    # Specify type of conversion that needs to be applied
    type_grid = '32ch textile grid large'
    
    # Get the HD-EMG conversion file
    config_file = join(modules_dir, 'TMSiSDK','_resources','HD_EMG_grid_channel_configuration.json')
    # Open the file if it exists, notify the user if it does not
    if exists(config_file):
        # Get the HD-EMG conversion table
        with open(config_file) as json_file:
            conversion_data = json.load(json_file)
    channel_conversion_list = np.array(conversion_data[type_grid]['channel_conversion']) - 1
    
    # Change the ordering of the first 32 channels (all channels on the textile grid)
    samples[0:32,:] = samples[channel_conversion_list,:]
    ch_names[0:32] = [ch_names[i] for i in channel_conversion_list]
    
    print(ch_names)

#%% Conversion to MNE raw array

toMNE = False

if toMNE:
    mne_object = data.read_data_MNE()
    
    # Retrieve the MNE RawArray info and sample data
    info_mne = mne_object.info
    samples_mne = mne_object._data
    
    mne_object.plot(start = 5, duration = 5, n_channels = 2)