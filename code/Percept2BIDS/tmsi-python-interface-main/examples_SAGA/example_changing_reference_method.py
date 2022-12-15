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
 * @file ${example_changing_reference_method.py} 
 * @brief This example shows how to change the applied reference method. The
 * configurable options are ReferenceMethod.common and ReferenceMethod.average.
 * In case of common reference, the reference switch method can be set to 
 * ReferenceSwitch.fixed or ReferenceSwitch.auto.In case of 
 * ReferenceSwitch.auto, reference method automatically swithces to average 
 * reference when the common reference signal is out of range
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

from TMSiSDK import tmsi_device
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import DeviceInterfaceType, ChannelType, ReferenceMethod, ReferenceSwitch, DeviceState
from TMSiFileFormats.file_writer import FileWriter, FileFormat

try:
    # Initialize the TMSi-SDK first before starting using it
    tmsi_device.initialize()

    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    discoveryList = tmsi_device.discover(tmsi_device.DeviceType.saga, DeviceInterfaceType.docked, 
                                         DeviceInterfaceType.usb)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
    
        # Set the sample rate of all channels to 1000 Hz
        dev.config.base_sample_rate = 4000
        dev.config.set_sample_rate(ChannelType.all_types, 4)
        
        # Specify the reference method and reference switch method that are used during sampling 
        # ReferenceMethod: average or common
        # ReferenceSwitch: fixed or auto
        dev.config.reference_method = ReferenceMethod.common,ReferenceSwitch.fixed
        
        # Retrieve the channel list from the device
        ch_list = dev.config.channels
        
        # Enable all UNI-channels
        for idx, ch in enumerate(ch_list):
            if (ch.type == ChannelType.UNI):
                # When the device samples in average reference method, the CREF channel can be disabled
                if (idx == 0) and (dev.config.reference_method == ReferenceMethod.average.value):
                    ch.enabled = False
                else:
                    ch.enabled = True
            else:
                ch.enabled = False
        dev.config.channels = ch_list
    
        # Before the measurement starts first a file-writer-object must be created and opened.
        # Upon creation specify :
        #   - the data-format 'poly5' to be used
        #   - the filepath/name, where the file must be stored
        # then 'link' the file-writer-instance to the device.
        # The file-writer-object is now ready to capture the measurement-data and
        # write it to the specified file.
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir, "changed_reference_method_measurement.poly5"))
        file_writer.open(dev)
    
        # Start the measurement and wait 10 seconds. In the mean time the file-writer-instance
        # will capture the sampling data and store it into the specified file in the 'poly5'-data format.
        dev.start_measurement()
    
        # Wait for 10 seconds
        time.sleep(10)
    
        # Stop the measurement
        dev.stop_measurement()
    
        # Close the file-writer-instance.
        # The sample-data of the measurement has been archived into the specified file.
        file_writer.close()
    
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