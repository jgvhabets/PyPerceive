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
 * @file ${example_SD_card_download.py} 
 * @brief This example shows how to download card recordings that are stored on 
 * SAGA’s onboard memory.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
import time

Example_dir = dirname(realpath(__file__))  # directory of this file
modules_dir = join(Example_dir, '..')  # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiSDK.device import DeviceInterfaceType
from TMSiSDK import tmsi_device
from TMSiFileFormats.file_writer import FileWriter, FileFormat
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import DeviceInterfaceType, DeviceState

try:
    # Initialize the SDK
    tmsi_device.initialize()
    
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    discoveryList = tmsi_device.discover(tmsi_device.DeviceType.saga, DeviceInterfaceType.docked, 
                                         DeviceInterfaceType.usb)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
    
        # Create a file writer object to download the onboard recording (if there is any)
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_file_backup.poly5"))
        file_writer.open(dev)
        
        # Get a list of all available recordings
        recordings_list = dev.get_device_storage_list()
        if len(recordings_list) <= 0:
            raise(IndexError)
        
        # Retrieve the first recording of the device
        res = list(recordings_list.keys())[0]
        # Start downloading the file from the onboard memory
        dev.download_recording_file(res)
        
        # Close the file writer after completion of the download
        file_writer.close()
        
        # Close the connection to the device
        dev.close()

except IndexError:
    print("device memory is empty, impossible to download any file")
    
    # Close the connection to the device
    dev.close()

except TMSiError as e:
    file_writer.close()
    print("!!! TMSiError !!! : ", e.code)
    if (e.code == TMSiErrorCode.device_error) :
        print("  => device error : ", hex(dev.status.error))
        DeviceErrorLookupTable(hex(dev.status.error))
        
finally:
    # Close the connection to the device when the device is opened
    if dev.status.state == DeviceState.connected:
        dev.close()