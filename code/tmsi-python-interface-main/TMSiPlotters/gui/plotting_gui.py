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
 * @file ${plotting_gui.py} 
 * @brief GUI that handles all user interaction when displaying (different) 
 * signals.
 *
 */


'''

from PySide2 import QtWidgets, QtGui
import numpy as np
import sys
import json

from os.path import join, dirname, realpath, normpath, exists

Plotter_dir = dirname(realpath(__file__)) # directory of this file
measurements_dir = join(Plotter_dir, '../../measurements') # directory with all measurements
modules_dir = normpath(join(Plotter_dir, '../..')) # directory with all modules

from TMSiSDK import tmsi_device
from TMSiSDK import sample_data_server
from TMSiSDK.device import DeviceInterfaceType, DeviceState, MeasurementType

from TMSiPlotters.plotters import PlotterFormat
from TMSiPlotters.gui._plotter_gui import Ui_MainWindow 
from TMSiPlotters.plotters.signal_plotter import SignalViewer
from TMSiPlotters.plotters.hd_emg_plotter import HeatMapViewer
from TMSiPlotters.plotters.impedance_plotter import ImpedanceViewer


class PlottingGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    """ A GUI that displays the signals on the screen. The GUI handles the 
        incoming data and is able to apply scaling. Furthermore, the GUI handles
        closing the device when it is closed. 
    """
    
    def __init__(self, plotter_format, figurename, device, channel_selection = None, filter_app = None,
                 tail_orientation = None, signal_lim = None, grid_type = 'none', file_storage = None, 
                 layout = None):
        """ Setting up the GUI's elements. 
        """
        super(PlottingGUI, self).__init__()

        # Load the UI Page
        self.setupUi(self)
        
        # Pass the device handle so that it is accesible to the GUI
        self.device = device
        self.setWindowTitle(figurename)
        self.filter_app = filter_app
        self.grid_type = grid_type
        
        # Create a list of displayed channels. The counter channel is never displayed
        if not channel_selection:
            self._channel_selection = np.arange(0, np.size(self.device.channels,0)-1)

        else:
            for i in channel_selection:
                # When indices are selected that correspond to the STATUS channel,
                # or the COUNTER channel, remove them from the channel_selection parameter
                if (i == np.size(self.device.channels,0)-2):
                    _idx = channel_selection.index(i)
                    channel_selection = channel_selection[:_idx]
            self._channel_selection = np.hstack((channel_selection, np.size(self.device.channels,0)-2))

        # Set up UI and thread
        if plotter_format == PlotterFormat.signal_viewer:
            self.real_time_plot = SignalViewer(self, device, filter_app = filter_app, grid_type = self.grid_type)
            self.initUI()
            self.startEvent()
            
        elif plotter_format == PlotterFormat.heatmap: 
            self.real_time_plot = HeatMapViewer(gui_handle = self, device = device, 
                                                tail_orientation = tail_orientation, 
                                                signal_lim = signal_lim,
                                                grid_type = grid_type)
            
            # Hide unused GUI controllers from the plotter window
            self.channel_list_groupbox.setVisible(False)
            self.hide_AUX_button.setVisible(False)
            self.show_AUX_button.setVisible(False)
            self.hide_BIP_button.setVisible(False)
            self.show_BIP_button.setVisible(False)
            self.hide_UNI_button.setVisible(False)
            self.show_UNI_button.setVisible(False)
            self.hide_DIGI_button.setVisible(False)
            self.show_DIGI_button.setVisible(False)
            self.decrease_time_button.setVisible(False)
            self.increase_time_button.setVisible(False)
            self.enable_filter_button.setVisible(False)
            self.disable_filter_button.setVisible(False)
            
            # Connect scaling buttons to the respective functions in the plotter
            self.set_range_box.activated.connect(lambda x: self.real_time_plot._update_scale('range'))
            self.autoscale_button.clicked.connect(lambda x: self.real_time_plot._update_scale('scale'))
            
            self.startEvent()
            
        elif plotter_format == PlotterFormat.impedance_viewer:
            self.real_time_plot = ImpedanceViewer(gui_handle = self, device = device,
                                                file_storage = file_storage, layout = layout,
                                                grid_type = grid_type)
            
            # Hide unused GUI controllers from the plotter window
            self.channel_list_groupbox.setVisible(False)
            self.hide_AUX_button.setVisible(False)
            self.show_AUX_button.setVisible(False)
            self.hide_BIP_button.setVisible(False)
            self.show_BIP_button.setVisible(False)
            self.hide_UNI_button.setVisible(False)
            self.show_UNI_button.setVisible(False)
            self.hide_DIGI_button.setVisible(False)
            self.show_DIGI_button.setVisible(False)
            self.decrease_time_button.setVisible(False)
            self.increase_time_button.setVisible(False)
            self.set_range_box.setVisible(False)
            self.set_range_label.setVisible(False)
            self.autoscale_button.setVisible(False)            
            self.enable_filter_button.setVisible(False)
            self.disable_filter_button.setVisible(False)
            
            self.startEvent(impedance = True)
        
    def initUI(self):
        """ Method responsible for constructing the basic elements in the plot
        """
        
        # Configuration settings
        self.active_channels = np.size(self.device.channels,0)
        
        # Set channel list checkboxes
        self._gridbox = QtWidgets.QGridLayout()
        self.channel_list_groupbox.setLayout(self._gridbox)
        
        if self.device.config.reference_method[0] == 'common':
            self._chan_offset = 1
        else:
            self._chan_offset = 0
        
        # Get the HD-EMG conversion file
        config_file = join(modules_dir, 'TMSiSDK','_resources','HD_EMG_grid_channel_configuration.json')
        # Open the file if it exists, notify the user if it does not
        if exists(config_file):
            # Get the HD-EMG conversion table
            with open(config_file) as json_file:
                self.conversion_data = json.load(json_file)
        else:
            print("Couldn't load HD-EMG conversion file, using default channel ordering")
            self.grid_type = 'none'
        
        # Create a list of value that maps the channel number to position on the grid
        if self.grid_type.casefold() == '32ch textile grid large'.casefold(): 
            # Convert to position of the grid
            self.channel_conversion_list = np.array(self.conversion_data['32ch textile grid large']['channel_conversion']) - (1-self._chan_offset)
            if self._chan_offset:
                self.channel_conversion_list = np.insert(self.channel_conversion_list, 0, 0)
            self.channel_conversion_list = np.hstack((self.channel_conversion_list,
                                                      np.arange(len(self.channel_conversion_list),
                                                                len(self.device.channels), 
                                                                dtype = int)))
            
        elif self.grid_type.casefold() == '32ch textile grid small'.casefold():
            # Convert to position of the grid
            self.channel_conversion_list = np.array(self.conversion_data['32ch textile grid small']['channel_conversion']) - (1-self._chan_offset)
            if self._chan_offset:
                self.channel_conversion_list = np.insert(self.channel_conversion_list, 0, 0)
            self.channel_conversion_list = np.hstack((self.channel_conversion_list,
                                                      np.arange(len(self.channel_conversion_list),
                                                                len(self.device.channels), 
                                                                dtype = int)))
        else:
            self.channel_conversion_list = np.arange(0,len(self.device.channels), dtype = int)
        
        # Create checkboxes for the active channels so that they can be selected
        self._checkboxes = []
        for i in range(self.active_channels - 2):
            _checkBox = QtWidgets.QCheckBox(self.device.channels[self.channel_conversion_list[i]].name)
            if i in self._channel_selection:
                _checkBox.setChecked(True)
            self._gridbox.addWidget(_checkBox, i%25, np.floor(i/25))
            _checkBox.clicked.connect(self.real_time_plot._update_channel_display)
            
            # Keep track of the checkboxes and the channel type belonging to the checkbox
            self._checkboxes.append((_checkBox, self.device.channels[i].type))

        # Connect button clicks to code execution
        self.autoscale_button.clicked.connect(lambda x: self.real_time_plot._update_scale('scale'))
        self.increase_time_button.clicked.connect(self.real_time_plot._increase_time_range)
        self.decrease_time_button.clicked.connect(self.real_time_plot._decrease_time_range)
        self.set_range_box.activated.connect(lambda x: self.real_time_plot._update_scale('range'))
        
        # Set the window update button text
        self.increase_time_button.setText('Increase time range: ' + str(self.real_time_plot.window_size + 1) + 's')
        self.decrease_time_button.setText('Decrease time range: ' + str(self.real_time_plot.window_size - 1) + 's')

        # Connect display buttons to code execution
        self.show_UNI_button.clicked.connect(self.real_time_plot._show_all_UNI)
        self.hide_UNI_button.clicked.connect(self.real_time_plot._hide_all_UNI)
        self.show_BIP_button.clicked.connect(self.real_time_plot._show_all_BIP)
        self.hide_BIP_button.clicked.connect(self.real_time_plot._hide_all_BIP)
        self.show_AUX_button.clicked.connect(self.real_time_plot._show_all_AUX)
        self.hide_AUX_button.clicked.connect(self.real_time_plot._hide_all_AUX)
        self.show_DIGI_button.clicked.connect(self.real_time_plot._show_all_DIGI)
        self.hide_DIGI_button.clicked.connect(self.real_time_plot._hide_all_DIGI)
        
        if self.filter_app:
            self.disable_filter_button.clicked.connect(self.filter_app.disableFilter)
            self.enable_filter_button.clicked.connect(self.filter_app.enableFilter)
        else:
            self.disable_filter_button.setVisible(False)
            self.enable_filter_button.setVisible(False)


    def startEvent(self, impedance = False):
        """Method that starts the thread of the plotter"""
        
        if self.filter_app:
            self.filter_app.start()

        self.real_time_plot.thread.start()
            
        # Start measurement using the device thread
        if not self.device.status.state == DeviceState.sampling:
            if not impedance:
                self.device.start_measurement()
            else: 
                self.device.start_measurement(MeasurementType.impedance)
            

    def closeEvent(self, event):
        """ Method that redefines the default close event of the GUI. This is
            needed to close the sampling thread when the figure is closed.
        """
        
        # Stop the worker and the thread
        self.real_time_plot.worker.stop()
        
        if self.filter_app:
            self.filter_app.stop()
        
        self.real_time_plot.thread.terminate()
        self.real_time_plot.thread.wait()
        
        self.device.stop_measurement()

        
        # Unregister the Consumer from the sample data server. The RealTimeFilter object
        # takes care of this action itself. 
        if not self.filter_app:
            sample_data_server.unregisterConsumer(self.device.id, self.real_time_plot.worker.q_sample_sets)
        else:
            sample_data_server.unregisterConsumer(self.device.id, self.filter_app.filter_thread.q_sample_sets)
        





if __name__ == "__main__":
    # Initialise the TMSi-SDK first before starting using it
    tmsi_device.initialize()
    
    # Create the device object to interface with the SAGA-system.
    dev = tmsi_device.create(tmsi_device.DeviceType.saga, DeviceInterfaceType.docked, DeviceInterfaceType.network)

    # Find and open a connection to the SAGA-system and print its serial number
    dev.open()
    print("handle 1 " + str(dev.info.ds_serial_number))    
    
    # Initialise the application
    app = QtGui.QApplication(sys.argv)
    # Define the GUI object and show it
    window = RealTimePlot(figurename = 'A RealTimePlot', device = dev)
    window.show()
    
    # Enter the event loop
    app.exec_()
    
    dev.close()

