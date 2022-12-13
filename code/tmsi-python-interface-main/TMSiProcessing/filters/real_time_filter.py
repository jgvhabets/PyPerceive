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
 * @file ${real_time_filter.py} 
 * @brief Real-time filter that can be applied to incoming data.
 *
 */


'''

import sys

from TMSiSDK import sample_data_server
from TMSiSDK.device import ChannelType, DeviceInterfaceType

import numpy as np
import queue
from copy import deepcopy
import threading
import time

from scipy import signal, fft 
import matplotlib.pyplot as plt

class RealTimeFilter:
    """ A semi-real time filter that can be used to retrieve and filter the data 
    and send them to queue. Different filters can be used for the different 
    analogue channel types (UNI, BIP. AUX). When no filter is generated/enabled 
    data remains unfiltered.
    Start/Stop also starts/stops sampling of the device
    """
    def __init__(self, device):
        """Initialise filter instance
        """
        self.device=device
        self.num_channels = np.size(self.device.channels,0)
        self.sample_rate = self.device.config.get_sample_rate(ChannelType.counter)
        
        self._preprocess_wifi = False
        if self.device.info.dr_interface == DeviceInterfaceType.wifi:
            self._preprocess_wifi = True
        
        _UNI=[]
        _BIP=[]
        _AUX=[]
        
        for idx, ch in enumerate(device.channels):
            if (ch.type == ChannelType.UNI):
                _UNI.append(idx)
            elif (ch.type == ChannelType.BIP):
                _BIP.append(idx)
            elif (ch.type == ChannelType.AUX):
                _AUX.append(idx)
    
        self.channels={'UNI': _UNI,
                      'BIP': _BIP, 
                      'AUX': _AUX}
        self.filter_specs={'UNI': {'Order': None, 'Fc_hp': None, 'Fc_lp': None, 'Enabled': False},
                      'BIP': {'Order': None, 'Fc_hp': None, 'Fc_lp': None,'Enabled': False}, 
                      'AUX': {'Order': None, 'Fc_hp': None, 'Fc_lp': None, 'Enabled': False}}
        self._filter_details={'UNI': {'sos': None, 'z_sos': None},
                              'BIP': {'sos': None, 'z_sos': None}, 
                              'AUX': {'sos': None, 'z_sos': None}}
        
        # Prepare Queues
        _QUEUE_SIZE = 1000
        self.q_sample_sets = queue.Queue(_QUEUE_SIZE)
        
        _MAX_SIZE_FILTER_QUEUE=50
        self.q_filtered_sample_sets=queue.Queue(_MAX_SIZE_FILTER_QUEUE)
        
        self.filter_thread = FilterThread(self)
    
    def generateFilter(self, order=2, Fc_hp=None, Fc_lp=None, ch_types=None, show=False):
        """ Generate filter with given order and cut-off frequency/frequencies. 
        Generates a high-pass filter when only Fc_hp is specified,a low-pass 
        filter when only Fc_lp is specified or a band-pass when both Fc_hp and 
        Fc_lp are given.
        Filter is applied to the specified channel types or to all analogue 
        channels when no channels types are given.
        Use show to inspect the frequency response of the filter """
        if not ch_types:
            ch_types=list(self.channels.keys())
            
        for ch_type in ch_types:
            self.filter_specs[ch_type]['Order']=order
            self.filter_specs[ch_type]['Fc_hp']=Fc_hp
            self.filter_specs[ch_type]['Fc_lp']=Fc_lp
            
            chan=self.channels[ch_type]
            
            if not (Fc_hp or Fc_lp) or not chan:
                sos=None
                z_sos=None
                self.filter_specs[ch_type]['Enabled']=False
            else:
                if Fc_hp and Fc_lp:
                    sos=signal.butter(order, [Fc_hp, Fc_lp], 'bandpass', fs=self.sample_rate, output='sos')
                elif Fc_hp:
                    sos=signal.butter(order, Fc_hp, 'highpass', fs=self.sample_rate, output='sos')
                elif Fc_lp:
                    sos=signal.butter(order, Fc_lp, 'lowpass', fs=self.sample_rate, output='sos')
                 
                z_sos0 = signal.sosfilt_zi(sos)
                z_sos=np.repeat(z_sos0[:, np.newaxis, :], len(chan), axis=1)
                self.filter_specs[ch_type]['Enabled']=True
            
            self._filter_details[ch_type]['sos']=sos
            self._filter_details[ch_type]['z_sos']=z_sos
        
        if show:
            # Show the frequency response of the filter
            w, h = signal.sosfreqz(sos, worN=fft.next_fast_len(self.sample_rate*10))
            plt.figure()
            plt.subplot(2, 1, 1)
            db = 20*np.log10(np.maximum(np.abs(h), 1e-5))
            plt.plot((self.sample_rate/2)*(w/np.pi), db, label = ch_type)
            plt.ylim(-50, 5)
            plt.grid(True)
            plt.yticks([0, -20, -40])
            plt.ylabel('Gain [dB]')
            plt.title('Frequency Response')
            plt.subplot(2, 1, 2)
            plt.plot((self.sample_rate/2)*(w/np.pi), np.angle(h), label = ch_type)
            plt.grid(True)
            plt.yticks([-np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi],
                       [r'$-\pi$', r'$-\pi/2$', '0', r'$\pi/2$', r'$\pi$'])
            plt.ylabel('Phase [rad]')
            plt.xlabel('Frequency [Hz]')
            plt.show()
        
    def disableFilter(self, *ch_types):
        """ Disable the filters for the given channel types. All filters are disabled 
        when no channel types are given"""
        if not ch_types:
            ch_types=list(self.channels.keys())
            
        for ch_type in ch_types:
            self.filter_specs[ch_type]['Enabled']=False
            
    def enableFilter(self, *ch_types):
        """ Enable the filters for the given channel types. All filters are enabled 
        when no channel types are given"""
        if not ch_types:
            ch_types=list(self.channels.keys())
        
        for ch_type in ch_types:
            chan=self.channels[ch_type]
            if chan:
                self.filter_specs[ch_type]['Enabled']=True
                self.reset(ch_type)

    def reset(self, *ch_types):
        """ Reset the filters for the given channel types. All filters are reset 
        when no channel types are given"""
        
        if not ch_types:
            ch_types=list(self.channels.keys())
        
        for ch_type in ch_types:
            chan=self.channels[ch_type]
            if self.filter_specs[ch_type]['Enabled']:
                z_sos0 = signal.sosfilt_zi(self._filter_details[ch_type]['sos'])
                z_sos=np.repeat(z_sos0[:, np.newaxis, :], len(chan), axis=1)
                self._filter_details[ch_type]['z_sos']=z_sos
            
    def start(self):
        """ Start the filter thread and device""" 
        self.filter_thread.start()
        
    def stop(self):
        """ Stop the filter thread and device"""
        self.filter_thread.stop()


class FilterThread(threading.Thread):
    """A semi-real time filter"""
    
    def __init__(self, main_class):
        """ Setting up the class' properties
        """
        super(FilterThread,self).__init__()
        
        self.q_filtered_sample_sets=main_class.q_filtered_sample_sets
        self.q_sample_sets = main_class.q_sample_sets
        
        self.channels=main_class.channels
        self._filter_details=main_class._filter_details
        self.filter_specs=main_class.filter_specs
        self.device=main_class.device
        self._preprocess_wifi = main_class._preprocess_wifi
        
        # Register the consumer to the sample data server
        sample_data_server.registerConsumer(main_class.device.id, self.q_sample_sets)
                

    def run(self): 
        """ Method that retrieves samples from the queue, reshapes them into 
            the desired format and filters the samples.
        """
        # Start measurement
        self.sampling = True
        
        while self.sampling:
            while not self.q_sample_sets.empty():
                #Read samples from queue 
                sd = self.q_sample_sets.get()
                self.q_sample_sets.task_done()
                
                # Reshape the samples retrieved from the queue
                samples = np.reshape(sd.samples, (sd.num_samples_per_sample_set, sd.num_sample_sets), order = 'F')
                
                # Missing samples are registered as NaN. This crashes the filter. 
                # Therefore, copies are inserted for the filtered data
                if self._preprocess_wifi:
                    find_nan = np.isnan(samples)
                    if find_nan.any():
                        idx_nan = np.where(np.isnan(samples))
                        samples[idx_nan] = samples[idx_nan[0], idx_nan[1][0]-1]
                
                # Filter data
                if any([self.filter_specs[key]['Enabled'] for key in self.filter_specs]):
                    for ch_type, ch_filter in self._filter_details.items():
                        if self.filter_specs[ch_type]['Enabled']:
                            # filter the data
                            samples[self.channels[ch_type]], self._filter_details[ch_type]['z_sos']=signal.sosfilt(self._filter_details[ch_type]['sos'], samples[self.channels[ch_type]], zi=self._filter_details[ch_type]['z_sos'])

                # Output sample data to queue
                self.q_filtered_sample_sets.put(deepcopy(samples))
                
                # Pause the thread for a bit to update the plot (should be the same sleep time as the plotter)
                time.sleep(0.03)
        
    def stop(self):
        """ Method that is executed when the thread is terminated. 
            This stop event stops the measurement.
        """
        self.sampling=False
