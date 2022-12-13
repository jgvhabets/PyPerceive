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
 * @file ${example_wifi_measurement.py} 
 * @brief This example shows how to perform a measurement over the wireless 
 * interface, while data is backed up to the SD card. Finally, the full 
 * recording is downloaded from the device.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

import time
from PySide2 import QtWidgets

from TMSiSDK import tmsi_device
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import DeviceInterfaceType, DeviceState, ChannelType
from TMSiFileFormats.file_writer import FileWriter, FileFormat
from TMSiPlotters.gui import PlottingGUI
from TMSiPlotters.plotters import PlotterFormat

try:
    # Initialize the TMSi-SDK first before starting using it
    tmsi_device.initialize()
    
    discoveryList = tmsi_device.discover(tmsi_device.DeviceType.saga, DeviceInterfaceType.docked, 
                                         DeviceInterfaceType.usb)
    if (len(discoveryList) > 0):
        # Create the device object to interface with the SAGA-system.
        dev = discoveryList[0]
    
        # Find and open a connection to the SAGA-system
        dev.open()
        
        # Choose the desired DR-DS interface type 
        dev.config.set_interface_type(DeviceInterfaceType.wifi)
        
        # Close the connection to the device (with the original interface type)
        dev.close()
        
        # Wait for a bit while the connection is closed
        time.sleep(1)
    
    # Discover the device object with the new interface type
    discoveryList = tmsi_device.discover(tmsi_device.DeviceType.saga, 
                                         DeviceInterfaceType.wifi, 
                                         DeviceInterfaceType.usb)
    
    if (len(discoveryList) > 0):
        # Create the device object to interface with the SAGA-system.
        dev = discoveryList[-1]
        
        # Find and open the connection to the SAGA-system
        dev.open()
        
        # Check the current bandwidth that's in use
        current_bandwidth = dev.get_current_bandwidth()
        print('The current bandwidth is {:.3} Mbit/s'.format(current_bandwidth))
        
        # Get the channel list
        ch_list = dev.config.channels
        
        # Enable all unipolar channels
        for idx, ch in enumerate(ch_list):
            if ch.type == ChannelType.UNI:
                ch.enabled = True
            else:
                ch.enabled = False
        dev.config.channels = ch_list
        
        # Maximal allowable sample rate with all enabled channels is 1000 Hz
        dev.config.set_sample_rate(ChannelType.UNI, 4)
    
        # Before the measurement starts first a file-writer-object must be created and opened.
        # Upon creation specify :
        #   - the data-format 'poly5' to be used
        #   - the filepath/name, where the file must be stored
        # then 'link' the file-writer-instance to the device.
        # The file-writer-object is now ready to capture the measurement-data and
        # write it to the specified file.
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_wifi_measurement.poly5"))
        file_writer.open(dev)
        
        # Enable backup logging of hte device
        dev.set_device_backup_logging("example_wifi")
    
        # Check if there is already a plotter application in existence
        plotter_app = QtWidgets.QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not plotter_app:
            plotter_app = QtWidgets.QApplication(sys.argv)
    
        # Define the GUI object and show it 
        # The channel selection argument states which channels need to be displayed initially by the GUI
        plot_window = PlottingGUI(plotter_format = PlotterFormat.signal_viewer,
                                            figurename = 'A RealTimePlot', 
                                            device = dev, 
                                            channel_selection = [0,1,2])
        plot_window.show()
        
        # Enter the event loop
        plotter_app.exec_()
    
        # Close the file-writer-instance.
        # The sample-data of the measurement has been archived into the specified file.
        file_writer.close()
        
        # Choose the desired DR-DS interface type 
        dev.config.set_interface_type(DeviceInterfaceType.docked)
        
        # Close the connection over the current interface
        dev.close()
        
    # Discover the device via the docked interface again
    discoveryList = tmsi_device.discover(tmsi_device.DeviceType.saga, 
                                         DeviceInterfaceType.docked, 
                                         DeviceInterfaceType.usb)
    
    if (len(discoveryList) > 0):
        # Create the device object to interface with the SAGA-system.
        dev = discoveryList[0]
         
        # Reopen the connection to the device
        dev.open()
        
        # Retrieve the recordings list with the full file on there
        recordings_list = dev.get_device_storage_list()
        for rec_id in recordings_list:
            print("{} - {}".format(rec_id, recordings_list[rec_id]))
        
        # Configure a file writer to save the backed up data
        file_writer_backup = FileWriter(FileFormat.poly5, join(measurements_dir,"example_wifi_measurement_backup_logging.poly5"))
        file_writer_backup.open(dev)
        
        # Get the handle to the file and start downloading the data
        file_handle = list(recordings_list.keys())[0]
        dev.download_recording_file(file_handle)
    
        # Close the file writer after download completion
        file_writer_backup.close()
    
        # Close the connection to the SAGA-system
        dev.close()

except TMSiError as e:
    print("!!! TMSiError !!! : ", e.code)
    if (e.code == TMSiErrorCode.device_error) :
        print("  => device error : ", hex(dev.status.error))
        DeviceErrorLookupTable(hex(dev.status.error))
        
finally:
    # Close the connection to the device when the device is opened
    if dev.status.state == DeviceState.connected:
        dev.close()