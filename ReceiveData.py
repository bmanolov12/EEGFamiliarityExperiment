# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:07:25 2020

@author: bmano
"""

from pylsl import StreamInlet, resolve_stream

try:
    streams = None
    while streams == None:
        streams = resolve_stream('name', 'audio_out')
    
    print("Stream created!")
    inlet = StreamInlet(streams[0])
    
    while True:
        sample, timestamp = inlet.pull_sample()
        print(sample)
#allow for escaping
except KeyboardInterrupt as e:
    print("Ending program")
    raise e