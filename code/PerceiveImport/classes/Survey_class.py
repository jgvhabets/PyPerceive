""" Create Survey class """

import os
import sys
import importlib
import json
from dataclasses import dataclass, field, fields
from itertools import compress
import csv
import pandas as pd
import numpy as np

import sklearn as sk
import scipy
import matplotlib.pyplot as plt
from scipy import signal

#mne
import mne_bids
import mne

@dataclass (init=True, repr=True)
class Survey:
    """
    BrainSense Survey Class 
    
    parameters:
        - 
    
    Returns:
        - 
    
    """
    
    # initialized fields
    ch_names
    
    
    def __post_init__(self,):
        print(self.ch_names)
    
    def __str__(self,):
        return f'channel names are {self.ch_names}'