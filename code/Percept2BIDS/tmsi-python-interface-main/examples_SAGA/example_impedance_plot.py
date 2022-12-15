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
 * @file ${example_impedance_plot.py} 
 * @brief This example shows the functionality of the impedance plotter.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from PySide2 import QtWidgets
import numpy as np

from TMSiSDK import tmsi_device
from TMSiPlotters.gui import PlottingGUI
from TMSiPlotters.plotters import PlotterFormat
from TMSiSDK.device import DeviceInterfaceType, ChannelType, DeviceState
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
    
        # Enable UNI 01 to UNI 32
        ch_list = dev.config.channels
        UNI_count = 0
        UNI_list = np.arange(1,33, dtype = int)
        for idx, ch in enumerate(ch_list):
            if (ch.type == ChannelType.UNI):
                if UNI_count in UNI_list:
                    ch.enabled = True
                else:
                    ch.enabled = False
                UNI_count += 1
            else :
                ch.enabled = False
        dev.config.channels = ch_list
        
        # Check if there is already a plotter application in existence
        plotter_app = QtWidgets.QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not plotter_app:
            plotter_app = QtWidgets.QApplication(sys.argv)
    
        # Define the GUI object and show it (either a grid layout or head layout may be chosen)
        window = PlottingGUI(plotter_format = PlotterFormat.impedance_viewer,
                             figurename = 'An Impedance Plot', 
                             device = dev, 
                             layout = 'grid')
        window.show()
        
        # Enter the event loop
        plotter_app.exec_()
        
        # Delete the Impedace plotter application
        del plotter_app
        
        # Close the connection to the SAGA device
        dev.close()
    
except TMSiError as e:
    print("!!! TMSiError !!! : ", e.code)
    if (e.code == TMSiErrorCode.device_error) :
        print("  => device error : 0x", hex(dev.status.error))
        DeviceErrorLookupTable(hex(dev.status.error))
        
finally:
    # Close the connection to the device when the device is opened
    if dev.status.state == DeviceState.connected:
        dev.close()
