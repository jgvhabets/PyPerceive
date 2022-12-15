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
 * @file ${example_EMG_workflow.py} 
 * @brief This example shows the functionality of the impedance plotter and an
 * HD-EMG heatmap. The user has to configure the tail orientation of the grid,
 * so that the grid is adapted to 'look into the grid'. The heatmap displays 
 * the RMS value per channel, combined with linear interpolation to fill the 
 * space between channels.
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
from TMSiPlotters.gui import PlottingGUI
from TMSiPlotters.plotters import PlotterFormat
from TMSiSDK.device import DeviceInterfaceType, DeviceState
from TMSiFileFormats.file_writer import FileWriter, FileFormat
from TMSiSDK.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK import get_config


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
    
        # Load the HD-EMG channel set and configuration
        print("load HD-EMG config")
        if dev.config.num_channels<64:
            cfg = get_config("saga32_config_textile_grid_large")
            # options: '32ch textile grid large', 'flex pcb grids', 'SAGA64 32ch textile grid large'
            grid_type = '32ch textile grid large'
        else:
            cfg = get_config("saga64_config_textile_grid_large")
            # options: '32ch textile grid large', 'flex pcb grids', 'SAGA64 32ch textile grid large'
            grid_type = 'SAGA64 32ch textile grid large'
        dev.load_config(cfg)
        
        
        # Check if there is already a plotter application in existence
        plotter_app = QtWidgets.QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not plotter_app:
            plotter_app = QtWidgets.QApplication(sys.argv)
            
        # Define the GUI object and show it
        window = PlottingGUI(plotter_format = PlotterFormat.impedance_viewer,
                             figurename = 'An Impedance Plot', 
                             device = dev, 
                             layout = 'grid', 
                             file_storage = join(measurements_dir,"example_EMG_workflow"),
                             grid_type = grid_type)
        window.show()
        
        # Enter the event loop
        plotter_app.exec_()
        
        # Pause for a while to properly close the GUI after completion
        print('\n Wait for a bit while we close the plot... \n')
        time.sleep(1)
        
        # Ask for desired file format
        file_format=input("Which file format do you want to use? (Options: poly5 or xdf)\n")
        
        # Initialise the desired file-writer class and state its file path
        if file_format.lower()=='poly5':
            file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_EMG_workflow.poly5"))
        elif file_format.lower()=='xdf':
            file_writer = FileWriter(FileFormat.xdf, join(measurements_dir,"example_EMG_workflow.xdf"), add_ch_locs=True)
        else:
            print('File format not supported. File is saved to Poly5-format.')
            file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_EMG_workflow.poly5"))
        
        # Define the handle to the device
        file_writer.open(dev)
    
        # Define the GUI object and show it 
        # The tail orientation is needed so that the user looks 'into' the grid. 
        # The signal_lim parameter (in microVolts) is needed to configure the colorbar range
        plot_window = PlottingGUI(plotter_format = PlotterFormat.signal_viewer,
                                    figurename = 'An HD-EMG Heatmap', 
                                    device = dev,
                                    tail_orientation = 'down', 
                                    signal_lim = 150,
                                    grid_type = grid_type)
        plot_window.show()
        
        # Enter the event loop
        plotter_app.exec_()
        
        # Quit and delete the Plotter application
        QtWidgets.QApplication.quit()
        del plotter_app
        
        # Close the file writer after GUI termination
        file_writer.close()
        
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