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
 * @file ${example_changing_channel_list.py} 
 * @brief This example shows the manipulation of the active channel list and 
 * demonstrates how the ChannelName property can be changed.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiSDK import tmsi_device
from TMSiSDK.device import DeviceInterfaceType, ChannelType, DeviceState
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable

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

        print('The active channels are : \n')
        for idx, ch in enumerate(dev.channels):
             print('[{0}] : [{1}] in [{2}], bw = [{3}]'.format(idx, ch.name, ch.unit_name, ch.bandwidth))
    
        # Enable all AUX-channels, print the updated active channel list
        #
        # Note : To change channel-properties next steps must be executed:
        #
        #           1. Make first a copy of the current total channel list, which can be
        #              retrieved with statement [ch_list = dev.config.channels]
        #           2. Make the changes of the channel-properties in the channel-list-copy
        #           3. Write the channel-list-copy back to the device-object with the statement
        #              [dev.config.channels = ch_list]
        #
        # Note : The channels of type ChannelType.status and ChannelType.counter can
        #        not be disabled. The device will ignore such changes.
        ch_list = dev.config.channels
        for idx, ch in enumerate(ch_list):
            if (ch.type == ChannelType.AUX):
                ch.enabled = True
            else :
                ch.enabled = False
        dev.config.channels = ch_list
    
        print('\nActivated only AUX-channels, de-activated the other channels, the active channels are now :')
        for idx, ch in enumerate(dev.channels):
             print('[{0}] : [{1}] in [{2}]'.format(idx, ch.name, ch.unit_name))
    
        # Rename some AUX-channels, print the updated active channel list
        #
        # Note : The name of the channels of type ChannelType.status and ChannelType.counter
        #        can not be changed. The device will ignore such changes.
        ch_list = dev.config.channels
        for idx, ch in enumerate(ch_list):
                if (ch.name == 'AUX 1-1'):
                    ch.name = 'Light'
                if (ch.name == 'AUX 2-2'):
                    ch.name = 'Y'
        dev.config.channels = ch_list
    
        print('\nRenamed channels [AUX 1-1] and [AUX 2-2], the names of the active channels are now :')
        for idx, ch in enumerate(dev.channels):
             print('[{0}] : [{1}] in [{2}]'.format(idx, ch.name, ch.unit_name))
             
             
        # Enable a subset of UNI-channels, print the updated channel list
        #
        # Note : To enable a subset of channels, next steps must be executed:
        #
        #           1. Make first a copy of the current total channel list, which can be
        #              retrieved with statement [ch_list = dev.config.channels]
        #           2. Keep track of the number of processed channels, to see if the next
        #              channel is in the list of channels that is to be enabled
        #           3. Make the changes of the channel-properties in the channel-list-copy
        #           4. Write the channel-list-copy back to the device-object with the statement
        #              [dev.config.channels = ch_list]
        #
        # Note : The channels of type ChannelType.status and ChannelType.counter can
        #        not be disabled. The device will ignore such changes.
        
        # Enable the first 24 UNI channels, skipping CREF
        UNI_list = list(range(1,25))
        # The counter is used to keep track of the number of UNI channels that have
        # been encountered while looping over the channel list
        UNI_count = 0
    
        ch_list = dev.config.channels
        for idx, ch in enumerate(ch_list):
            if (ch.type == ChannelType.UNI):
                if UNI_count in UNI_list:
                    ch.enabled = True
                else:
                    ch.enabled = False
                # Update the UNI counter
                UNI_count += 1
        dev.config.channels = ch_list
    
        print('\nActivated the first 24 UNI-channels, de-activated other UNI-channels, the active channels are now :')
        for idx, ch in enumerate(dev.channels):
             print('[{0}] : [{1}] in [{2}]'.format(idx, ch.name, ch.unit_name))
    
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