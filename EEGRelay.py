# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:32:40 2020

@author: bmano
"""

from pylsl import StreamOutput, StreamInfo
from psychopy import prefs
import psychtoolbox as ptb


#READ IN USB/EEG
#change UID for each user
uid = "uid0001"
info = StreamInfo("EEGStream", "EEG", 16, 100, "float32", uid)
#label the channels


outlet = StreamOutlet(info)
#TRANSLATE TO OUTPUT
#STREAM OUTPUT TO LSL