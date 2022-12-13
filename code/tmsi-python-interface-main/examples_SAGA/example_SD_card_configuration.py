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
 * @file ${example_SD_card_configuration.py} 
 * @brief This example shows the functionality to get and set the 
 * configuration of the onboard memory of SAGA. The prefix file name is 
 * changed in the example.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
import datetime

Example_dir = dirname(realpath(__file__))  # directory of this file
modules_dir = join(Example_dir, '..')  # directory with all modules
sys.path.append(modules_dir)

from TMSiSDK.device import DeviceInterfaceType
from TMSiSDK import tmsi_device
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import DeviceInterfaceType, DeviceState, ChannelType


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
        
        # Disable backup logging of recordings to the SD card
        dev.set_device_backup_disabled()
        
        # Get the device's card configuration and print the file Pre-fix
        device_amb_conf = dev.get_device_memory_configuration()
        print("T1: " + "".join(map(lambda x: chr(x) if x >=
              0 else " ", device_amb_conf.PrefixFileName[:])))
        
        # Check the current bandwidth that's in use (this may not exceed 2Mbit/s for button start recordings)
        current_bandwidth = dev.get_current_bandwidth()
        print('The current bandwidth is {:.3} Mbit/s'.format(current_bandwidth))
        
        # Enable button start of card recordings
        dev.set_device_recording_button("Button")
        
        # Get the device's card configuration and print the file Pre-fix
        device_amb_conf2 = dev.get_device_memory_configuration()
        print("T2: " + "".join(map(lambda x: chr(x) if x >=
              0 else " ", device_amb_conf2.PrefixFileName[:])))
        
        # Close the connection to the device
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