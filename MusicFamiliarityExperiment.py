# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 21:38:09 2020

@author: bmano
"""

from time import sleep
import os
from pathlib import Path
import collections
import math
import csv
from pylsl import StreamInfo, StreamOutlet, StreamInlet
import wave
from psychopy import core, event, sound, prefs
import psychtoolbox as ptb
import random
from datetime import datetime as dt
import tkinter as tk
from tkinter import ttk
#import librosa

base_path = Path(__file__).parent
popDir = os.path.join(base_path,"AudioFiles\\popular")
unpopDir = os.path.join(base_path,"AudioFiles\\unpopular")
#p = pyaudio.PyAudio()

#change the pref library to PTB and set the latency mode to high precision
prefs.hardware['audioLib'] = 'PTB'
prefs.hardware['audioLatencyMode'] = 3

#set up labstreaminglayer stream outlet
info = StreamInfo(name='audio_out', type='Markers', channel_count=1,
                  channel_format='int32', source_id='sound_example_stream')
outlet = StreamOutlet(info) #broadcast the stream

#read pop songs from directory
popSongs = os.listdir(popDir)
songPaths = collections.defaultdict(str)

#read unpopular songs from directory
unpopSongs = os.listdir(unpopDir)

#lists for building experiment playlist
unfamLimit = 2
famLimit = 2
playsPerSong = 3
unfamList = []
famList = []

pl = []
count = 0
songKeys = collections.defaultdict(int)
#assign marker keys to each of the songs and build the list of songs
for song in popSongs:
    pl.append(song)
    count += 1
    songKeys[song] = count
    songPaths[song] = os.path.join(popDir,song)
for song in unpopSongs:
    pl.append(song)
    count += 1
    songKeys[song] = count
    songPaths[song] = os.path.join(unpopDir,song)


#Popup window creation section
buttonVals = []
#handle button click for feedback/liking popup
def onClick(event):
    btn = event.widget
    buttonVal = int(btn.cget("text"))
    buttonVals.append(buttonVal)

#create a popup window with no input
def popupMsg(msg, title):
    popup = tk.Tk()
    #make window appear in middle of screen
    width = 400
    height = 200
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x_coord = (screen_width/2) - (width/2)
    y_coord = (screen_height/2) - (height/2)
    popup.geometry("%dx%d+%d+%d" % (width,height,x_coord,y_coord))
    popup.wm_title(title)
    label = ttk.Label(popup, text=msg, font = ("Verdana", 12))
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()

#create a popup window with input
def popupInput(msg, title):
    popup = tk.Tk()
    popup.wm_title(title)
    #make window appear in middle of screen
    width = 400
    height = 300
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x_coord = (screen_width/2) - (width/2)
    y_coord = (screen_height/2) - (height/2)
    popup.geometry("%dx%d+%d+%d" % (width,height,x_coord,y_coord))
    label = ttk.Label(popup, text=msg, font = ("Verdana", 12))
    label.grid(row = 0, column = 0)
    label2 = ttk.Label(popup, text="Low:", font = ("Verdana", 10))
    label2.grid(row = 1, column = 0)
    label3 = ttk.Label(popup, text="High:", font = ("Verdana", 10))
    label3.grid(row = 7, column = 0)
    #label.pack(side="bottom", fill="x", pady=10)
    for i in range(1,8):
        b = ttk.Button(popup, text="%s" %i, command= popup.destroy)
        b.grid(row = i, column = 1)
        #b.pack()
        b.bind('<Button-1>', onClick)
    popup.mainloop()

def play(song):
    #get play duration for song
    #playtime = librosa.get_duration(filename=song)
    
    #Calculate the timestamp 500ms from now to allow enough time for sound card to prepare stimulus
    sample_stamp = ptb.GetSecs()+0.5

    #beep = sound.Sound('beep_sound.wav')
    stimulus = sound.Sound(songPaths[song])
    stimulus.play(when=sample_stamp)
    markers = {'sound': [songKeys[song]]}
    outlet.push_sample(markers['sound'], sample_stamp)
    
    # while stimulus.status != FINISHED:
    #     continue
    
    #Python playback, not necessary when using LSL
    # f = wave.open(song,"rb")
    # #open stream
    # stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
    #             channels = f.getnchannels(),  
    #             rate = f.getframerate(),  
    #             output = True)
    # #read data  
    # data = f.readframes(chunk)
    # #play stream  
    # while data:  
    #     stream.write(data)  
    #     data = f.readframes(chunk)  
    
    # #stop stream  
    # stream.stop_stream()  
    # stream.close()  
    # p.terminate()
    
    #add sleep timer equal to song length
    #sleep(playtime)
    
    sleep(30.5)
    
    #get familiarity rating
    popupInput("Rate your familiarity", "Familiarity Rating")
    famRating = buttonVals.pop(0)
    #get preference rating
    popupInput("Rate your liking", "Preference Rating")
    prefRating = buttonVals.pop(0)
    return famRating, prefRating

if __name__ == '__main__':
    random.shuffle(pl)
    isReady = False
    #play the initial list of songs until requisite number met or playlist complete
    for song in pl:
        famRating,prefRating = play(song)
        if (famRating == 1 or famRating == 2) and len(unfamList) < unfamLimit:
            unfamList.append(song)
            print("Added to unfamiliar list")
        elif (famRating == 6 or famRating == 7) and len(famList) < famLimit:
            famList.append(song)
            print("Added to familiar list")
        else:
            print("Not added to either list")
        if len(unfamList) == unfamLimit and len(famList) == famLimit:
            pl = []
            for x in famList:
                pl.append(x)
            for y in unfamList:
                pl.append(y)
            isReady = True
            sleep(1)
            break
        sleep(1)
    
    #requisite number of songs not met
    if isReady == False:
        print("Thank you for your participation. The study is now complete.")
        exit()
    
    print("Both lists finalized")
    #initialize song ratings dictionary
    songFamRatings = collections.defaultdict(list)
    songPrefRatings = collections.defaultdict(list)
    
    
    count = 1
    #play songs until all songs in playlist then take 2 minute break
    while count < playsPerSong:
        count += 1
        print("Play number " + str(count))
        random.shuffle(pl)
        #play each song and get familiarity rating
        for song in pl:
            famRating,prefRating = play(song)
            songFamRatings[song].append(famRating)
            songPrefRatings[song].append(prefRating)
            sleep(1)
        #2 minute break after block
        if count < playsPerSong:
            popupMsg("Break time!\nPress OK to continue", "Break time")
            sleep(2)
        
            
    print("Thank you for your participation. The study is now complete.")
    sleep(10)
    
    #write songRatings to file
    uid = dt.now().strftime("%d%m%Y_%H%M")
    filename = 'FamLikingRatings\\' + uid + '.csv'
    path = os.path.join(base_path, filename)
    with open(filename, "w+") as f:
        for key in songFamRatings.keys():
            f.write("%s,%s,%s\n"%(key,songFamRatings[key],songPrefRatings[key]))
        
        
        
        
        
        
        
        
        
        
        