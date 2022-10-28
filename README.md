# PyPerceive

### Goal:
Importing and using Perceive'd Percept data in Python

[Original Perceive Toolbox](https://github.com/neuromodulation/perceive) (matlab-based)


### Environment

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

import sklearn as sk
import scipy
import matplotlib.pyplot as plt
from scipy import signal

import mne_bids
import mne
```

``` 
pip install -r requirements.txt
pip install -r requirements.lock

bash install.sh
```

**requirements.txt**

| package | version |
| ------- | ------- |
|Python   | sys 3.10.6, packaged by conda-forge (main, Aug 22 2022, 20:43:44) [Clang 13.0.1 ] |
| pandas  | 1.5.0 |
| numpy   | 1.21.6 |
| mne_bids| 0.11 |
| mne     |  1.2.0 |
| sci-py  | 1.9.1 |
| sci-kit learn | 1.1.2 |



**requirements_dev.txt** 
 