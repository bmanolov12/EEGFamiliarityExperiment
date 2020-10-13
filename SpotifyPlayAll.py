# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 21:38:09 2020

@author: bmano
"""

import spotipy
from time import sleep
from spotipy.oauth2 import SpotifyOAuth
import os
import collections
import math
import csv
#from spotipy.oauth2 import SpotifyClientCredentials



os.environ['SPOTIPY_CLIENT_ID'] = '899c7be4628e42ebba1718d33d2fda4f'
os.environ['SPOTIPY_CLIENT_SECRET'] = '07d5f0b433cb465095df45c729a950ea'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

SCOPE = "user-read-playback-state,user-modify-playback-state"
CACHE = ".cache-" + "test"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE,
                                                client_id='899c7be4628e42ebba1718d33d2fda4f', 
                                                client_secret='07d5f0b433cb465095df45c729a950ea',
                                                cache_path=CACHE))

# auth_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(auth_manager=auth_manager)

popPlaylistID = "spotify:playlist:0VwyOVdurASf0uV00BHmF8"
unpopPlaylistID = "spotify:playlist:0VwyOVdurASf0uV00BHmF8"
offset=0

def play(uris):
    sp.start_playback(uris=uris)
    sleep(28)
    #only play 5 seconds
    sp.pause_playback()
    #get familiarity rating
    famRating = input("Rate your familiarity from 1 (not familiar at all) to 7 (very familiar)")
    return famRating

if __name__ == '__main__':
    response = sp.playlist_items(popPlaylistID,
                                  offset=offset,
                                  fields='items.track.id,total',
                                  additional_types=['track'])
    
    response2 = sp.playlist_items(unpopPlaylistID,
                                  offset=offset,
                                  fields='items.track.id,total',
                                  additional_types=['track'])
    
    previewPlaylist = [response['items'][x]['track']['id'] for x in range(len(response['items']))]
    #previewPlaylist = [['spotify:track:'+x] for x in previewPlaylist]
    previewPlaylist = [[x] for x in previewPlaylist if x != None]
    
    previewPlaylist2 = [response2['items'][x]['track']['id'] for x in range(len(response2['items']))]
    #previewPlaylist = [['spotify:track:'+x] for x in previewPlaylist]
    previewPlaylist2 = [[x] for x in previewPlaylist2 if x != None]
    
    #lists for building experiment playlist
    unfamLimit = 8
    famLimit = 8
    unfamList = []
    famList = []
    
    pl = previewPlaylist
    isReady = False
    #play the initial list of songs until requisite number met or playlist complete
    for song in pl:
        famRating = play(song)
        if (famRating == '1' or famRating == '2') and len(unfamList) < unfamLimit:
            unfamList.append(song)
        elif (famRating == '6' or famRating == '7') and len(famList) < famLimit:
            famList.append(song)
        if len(unfamList) == unfamLimit and len(famList) == famLimit:
            pl = unfamList.append(famList)
            isReady = True
            break
        sleep(2)
    
    #requisite number of songs not met
    if isReady == False:
        print("Thank you for your participation. The study is now complete.")
        exit()
    
    #initialize song ratings dictionary
    songRatings = collections.defaultdict(list)
    
    playsPerSong = 5
    count = 0
    #play songs until all songs in playlist then take 2 minute break
    while count < playsPerSong:
        random.shuffle(pl)
        #play each song and get familiarity rating
        for song in pl:
            famRating = play(song)
            songRatings[song].append(famRating)
            sleep(2)
        count += 1
        #2 minute break after block
        if count < playsPerSong:
            sleep(120)
            cont = input("Press any key to continue")
            sleep(5)
        
            
    print("Thank you for your participation. The study is now complete.")
    sleep(10)
    
    #write songRatings to file
    #what about order of plays?
    
        
        
        
        
        
        
        
        
        
        
        