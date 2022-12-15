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
 * @file ${synchronisation.py} 
 * @brief Class that can be used to synchronize data from multiple devices 
 * collected with LSL's LabRecorder application.
 *
 */


'''

import numpy as np
from scipy import interpolate
from copy import deepcopy

from TMSiFileFormats.file_readers.xdf_reader import Xdf_Reader
from TMSiFileFormats.file_formats.xdf_file_writer import XdfWriter


class TMSiSynchronisation():
    """ TMSiSynchronisation class can be used to synchronize data from multiple 
    devices using LSL timestamped .XDF files"""
    def __init__(self, files_in, output_file):
        self._all_synced = False
        if files_in[0].lower().endswith(".xdf"):
            self.file_type = "xdf"
            self._initialize_synch_xdf(files_in, output_file)
            return
        
    def _initialize_synch_xdf(self, files_in, output_file):
        """Method that initialises the input and output file"""
        # Read in the original data file
        self.master_file = Xdf_Reader(filename = files_in[0])
        self.output_file = output_file
        
    def synch_and_save(self, master_signal):
        """Method that performs all necessary steps to synchronise the .xdf file
        and save the synchronised data to a new file"""
        
        # Create handle to original file
        self.master_signal = master_signal
        
        # Retrieve the timestamps for both streams in the file
        self._get_master_timestamp()
        
        # Synchronise the two data streams based on the information of the two timestamps arrays
        self._synch_xdf()
        
        # Initialise the metadata associated with the new file
        self.synchronize_info()
        
        # Create the handle to an XDF-writer object
        self.file_writer = XdfWriter(self.output_file, add_ch_locs = None)
        
        # Save the synchronised data to the created .xdf file. 
        self.file_writer.save_offline(self.info_synced, self.samples_synced)

    def synchronize_info(self):
        """Method that retrieves the metadata of the newly created, synced .xdf 
        file."""
        stream_info = self.master_file.get_stream_info()
        if stream_info is not None:
            self.info_synced = deepcopy(stream_info[self.master_signal])
            self.info_synced["channel_count"] = [str(len(self.samples_synced))]
            self.info_synced["name"][0] = self.info_synced["name"][0] + " SYNCHRONIZED"
            self.info_synced["desc"][0]["channels"][0]["channel"] = []
            channel_counter = 0
            for n_info in range(len(stream_info)):
                for channel in stream_info[n_info]["desc"][0]["channels"][0]["channel"]:
                    self.info_synced["desc"][0]["channels"][0]["channel"].append(deepcopy(channel))
                    self.info_synced["desc"][0]["channels"][0]["channel"][-1]["label"][0] = \
                        "Dev_{}_{}".format(
                            n_info, 
                            self.info_synced["desc"][0]["channels"][0]["channel"][-1]["label"][0])
                    self.info_synced["desc"][0]["channels"][0]["channel"][-1]["index"][0] = str(channel_counter)
                    channel_counter = channel_counter + 1

    def synchronize_data(self, master_signal = 1):
        """Data synchronisation consists of: loading data, finding the relevant 
        parts of the data, correct the time axis and synchronising data using 
        data interpolation
        """
        while not self._all_synced:
            if hasattr(self, "file_type") and self.file_type == "xdf":
                self.synch_and_save(master_signal)
                self._all_synced = True
            else:
                print("Can't synchronise file, as an invalid file type is provided.")
                break

    def _get_master_timestamp(self):
        """Method that finds the overlapping part of the timestamps between the 
        different streams, so that a shared timestamps array can be initialised.
        Based on this array, interpolation can be performed, resulting in a 
        synchronised data array"""
        
        # Retrieve all timestamps from the file
        timestamps = self.master_file.time_stamps[:]
        
        # Initialise the start and end, based off the first timestamp array
        new_beginning = timestamps[0][0]
        new_ending = timestamps[0][-1]
        
        # Update the start and/or end point, if one of the streams has non-overlapping
        # start or end timestamps otherwise.
        for ts in timestamps:
            if ts[0] > new_beginning:
                new_beginning = ts[0]
            if ts[-1] < new_ending:
                new_ending = ts[-1]
                
        # Create the new master timestamp array, based on the selected master signal
        self.master_timestamps = [x for x in timestamps[self.master_signal] if x >= new_beginning if x <= new_ending]  
    
    def _synch_xdf(self):
        """Method that synchronises the data streams, based off cubic spline 
        interpolation. Interpolation is done over the range of the master 
        timestamps that has been created in the previous step."""
        
        # Find the number of channels (used in metadata, as well as tracking progress)
        self.n_channels = 0
        for _signal in self.master_file.data:
            self.n_channels = self.n_channels + len(_signal.ch_names)
        
        # Initialise a new sample vector
        self.samples_synced = np.zeros((self.n_channels, len(self.master_timestamps)), dtype=float)
        
        # Initialise a progress counter
        signal_counter = 0
        
        # Loop over all channels and all streams
        for n_signal in range(len(self.master_file.time_stamps)):
            for n_channel in range(len(self.master_file.data[n_signal].ch_names)):
                # Create a cubic spline interpolation function based on the original data
                f=interpolate.interp1d(
                    self.master_file.time_stamps[n_signal], 
                    self.master_file.data[n_signal][n_channel][0][0], kind='cubic')
                
                # Retrieve new data based on the interpolation function and created timestamps
                self.samples_synced[signal_counter,:] = f(self.master_timestamps)
                
                # Track progress of synchronisation procedure
                signal_counter = signal_counter + 1
                print("\rsynchronization progress: {:.2f}%".format(100 * signal_counter / self.n_channels), end="\r")
        print("\rSynchronisation done, writing to file...\n")
    
    
    def close(self):
        """ Close all files when ready"""
        self._all_synced = True
        for file in self.files:
            self.files[file].close()
        self.file_writer.close()


