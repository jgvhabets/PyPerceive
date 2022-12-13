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
 * @file ${example_synchronise_xdf.py} 
 * @brief This function shows how to synchronise two data streams 
 * in an .xdf file, that has been collected with the 
 * LSL-based LabRecorder application.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiProcessing.synchronisation import TMSiSynchronisation

# Define the input and output file
input_file = join(measurements_dir, "your_input_file.xdf")
output_file = join(measurements_dir, "your_output_file.xdf")

# Initialise the synchronisation tool by passing the desired input file and output file
sync_tool = TMSiSynchronisation(files_in = [input_file], 
                                output_file = output_file)

# Select which of the data streams is to be handled as the master stream. 
# Implicitly, the other stream(s) are considered to be a slave, on which time axis
# correction is performed. 
sync_tool.synchronize_data(master_signal = 1)

