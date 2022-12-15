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
 * @file ${example_changing_sample_rate.py} 
 * @brief This example shows how to change the Base Sample Rate property of 
 * SAGA, as well as how the active sample rate of individual channels can be 
 * changed.
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

        print('The current base-sample-rate is {0} Hz.'.format(dev.config.base_sample_rate))
        print('\nThe current sample-rates per channel-type-group are :')
    
        for type in ChannelType:
            if (type != ChannelType.unknown) and (type != ChannelType.all_types):
                print('{0} = {1} Hz'.format(str(type), dev.config.get_sample_rate(type)))
    
        # The sample-rate of the channel-type-groups are derivated from the base-sample-rate.
        # Changing the base-sample-rate will therefor also automatically change the
        # sample-rate of the channel-type-groups.
        #
        # Note: The SAGA-systems 'knows' 2 base-sample-rates : 4000 Hz (default) and 4096 Hz.
        dev.config.base_sample_rate = 4096
    
        print('\n\nThe updated base-sample-rate is {0} Hz.'.format(dev.config.base_sample_rate))
        print('\nThe updated sample-rates per channel-type-group are :')
    
        for type in ChannelType:
            if (type != ChannelType.unknown) and (type != ChannelType.all_types):
                print('{0} = {1} Hz'.format(str(type), dev.config.get_sample_rate(type)))
    
        # It is also possible to change the sample-rate per channel-type-group individually.
        # The sample-rate is a derivate from the actual base-sample-rate. The sample-rate
        # must be set as a portion of the base-sample-rate. This can be done as next:
        #
        #       1 ( = 100% of the base-sample-rate),
        #       2 ( =  50% of the base-sample-rate),
        #       4 ( =  25% of the base-sample-rate) or
        #       8 ( =  12.5% of the base-sample-rate)
        #
        # Other values then 1,2,4 or 8 are not possible.
        #
        # To set a sample-rate of 512 Hz for all channel-type-groups, the base-sample-rate
        # must be 4096 Hz an the divider-value must be 8
        #
        # The sample-rate can be set per channel-type-group or for all channel-type-groups
        # at once as demostrated in the next example.
        dev.config.set_sample_rate(ChannelType.all_types, 2)
        dev.config.set_sample_rate(ChannelType.BIP, 4)
        dev.config.set_sample_rate(ChannelType.UNI, 8)
    
        print('\n\nThe base-sample-rate is still {0} Hz.'.format(dev.config.base_sample_rate))
        print('\nThe updated sample-rates per channel-type-group are now :')
    
        for type in ChannelType:
            if (type != ChannelType.unknown) and (type != ChannelType.all_types):
                print('{0} = {1} Hz'.format(str(type), dev.config.get_sample_rate(type)))
    
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