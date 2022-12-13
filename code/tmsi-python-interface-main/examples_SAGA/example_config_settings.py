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
 * @file ${example_config_settings.py} 
 * @brief This example shows the different configuration options, more detailed
 * explanations can be found in the examples of individual properties.
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)
from PySide2 import QtWidgets

from TMSiSDK import tmsi_device
from TMSiSDK.device import DeviceInterfaceType, DeviceState, ChannelType, ReferenceMethod, ReferenceSwitch
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable



try:
    # Initialise the TMSi-SDK first before starting using it
    tmsi_device.initialize()

    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    discoveryList = tmsi_device.discover(tmsi_device.DeviceType.saga, DeviceInterfaceType.docked,
                                         DeviceInterfaceType.usb)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]

        # Open a connection to the SAGA-system
        dev.open()

        # Print current device configuation
        print('Current device configuration:')
        print('Base-sample-rate: \t\t\t{0} Hz'.format(dev.config.base_sample_rate))
        print('Sample-rate: \t\t\t\t{0} Hz'.format(dev.config.sample_rate))
        print('Interface-bandwidth: \t\t{0} MHz'.format(dev.config.interface_bandwidth))
        print('Reference Method: \t\t\t', dev.config.reference_method)
        print('Sync out configuration: \t', dev.config.get_sync_out_config())
        print('Triggers:\t\t\t\t\t', dev.config.triggers )

        # Update the different configuration options:

        # Set base sample rate: either 4000 Hz (default)or 4096 Hz.
        dev.config.base_sample_rate = 4000

        # Set sample rate to 2000 Hz (base_sample_rate/2)
        dev.config.set_sample_rate(ChannelType.all_types, 2)

        # Specify the reference method and reference switch method that are used during sampling
        dev.config.reference_method = ReferenceMethod.common,ReferenceSwitch.fixed

        # Set the trigger settings
        dev.config.triggers=True

        # Set the sync out configuration
        dev.config.set_sync_out_config(marker=False, freq=1, duty_cycle=50)

        # Print new device configuation
        print('\n\nNew device configuration:')
        print('Base-sample-rate: \t\t\t{0} Hz'.format(dev.config.base_sample_rate))
        print('Sample-rate: \t\t\t\t{0} Hz'.format(dev.config.sample_rate))
        print('Reference Method: \t\t\t', dev.config.reference_method)
        print('Sync out configuration: \t', dev.config.get_sync_out_config())
        print('Triggers:\t\t\t\t\t', dev.config.triggers )

        # Close the connection to the SAGA device
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