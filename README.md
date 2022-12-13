# PyPerceive

### Goal:
Importing and using Perceive'd Percept data in Python

[Original Perceive Toolbox](https://github.com/neuromodulation/perceive) (matlab-based)


### Environment
```
conda create --name pyPerceive_dev python jupyter pandas scipy numpy matplotlib statsmodels seaborn
pip install mne 
pip install mne_bids

pip install openpyxl
pip install xlrd

pip install pymatreader

# For BIDS conformation (Jonathan Van Hoecke script)
# For ipyfilechooser and ipywidgets
conda install -c conda-forge ipywidgets
conda install -c conda-forge ipyfilechooser
conda install -c conda-forge mne-qt-browser
conda install ipympl
```

### Requirements

```
import os
import sys
import importlib
import json
from dataclasses import dataclass, field, fields
from itertools import compress
import csv
import pandas as pd
import numpy as np

import scipy
import matplotlib.pyplot as plt
from scipy import signal

import openpyxl
from openpyxl import Workbook, load_workbook
import xlrd

import mne_bids
import mne
```

``` 
pip install -r requirements.txt
pip install -r requirements.lock

bash install.sh
```


| package | version |
| ------- | ------- |
|Python   | sys 3.10.6, packaged by conda-forge (main, Oct 24 2022, 16:02:16) [MSC v.1916 64 bit (AMD64)] |
| pandas  | 1.4.4 |
| numpy   | 1.23.3 |
| mne_bids| 0.11.1 |
| mne     |  1.2.1 |
| sci-py  | 1.9.3 |


**requirements_dev.txt** 
 