# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 13:09:52 2020

@author: bmano
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import statistics
import collections
import csv
import scipy.stats as stats

#get directory for audio files
base_path = Path(__file__).parent
popDir = os.path.join(base_path,"AudioFiles\\compressed_popular")
unpopDir = os.path.join(base_path,"AudioFiles\\compressed_unpopular")


#read popular songs from directory
popSongs = os.listdir(popDir)
popSongSizes = collections.defaultdict(int)

#read unpopular songs from directory
unpopSongs = os.listdir(unpopDir)
unpopSongSizes = collections.defaultdict(int)

# #build list of paths for each song
for song in popSongs:
    popSongSizes[song] = int(os.path.getsize(os.path.join(popDir,song)))
for song in unpopSongs:
    unpopSongSizes[song] = int(os.path.getsize(os.path.join(unpopDir,song)))
    
# popSongSizes = [int(os.path.getsize(os.path.join(popDir,song))) for song in popSongs]
# unpopSongSizes = [int(os.path.getsize(os.path.join(unpopDir,song))) for song in unpopSongs]    
    
#bar graphs for song file sizes    
plt.bar(range(len(popSongSizes)), sorted([popSongSizes[x] for x in popSongSizes.keys()]))
plt.title("Popular song sizes")
plt.ylabel("Song size (bytes)")
plt.show()

plt.bar(range(len(unpopSongSizes)), sorted([unpopSongSizes[x] for x in unpopSongSizes.keys()]))
plt.title("Unpopular songs")
plt.ylabel("Song size (bytes)")
plt.show()

#boxplot for song file sizes
plt.boxplot([[popSongSizes[x] for x in popSongSizes.keys()], [unpopSongSizes[x] for x in unpopSongSizes.keys()]])
plt.xticks([1,2],["Popular","Unpopular"])
plt.ylabel("File size (bytes)")
plt.xlabel("Group")
plt.title("Boxplots of song sizes")
plt.show()
    

popSizes = [popSongSizes[x] for x in popSongSizes.keys()]
unpopSizes = [unpopSongSizes[x] for x in unpopSongSizes.keys()]

#t-test
t = stats.ttest_ind(popSizes, unpopSizes)
print(t)

#wilcoxon rank sum
w = stats.wilcoxon(popSizes, unpopSizes)
print(w)


#build csv of song sizes
filename = 'AudioFileSizes.csv'
path = os.path.join(base_path, filename)
with open(filename, "w+") as f:
    for key in popSongSizes.keys():
        f.write("%s,%s\n"%(key,popSongSizes[key]))
    for key in unpopSongSizes.keys():
        f.write("%s,%s\n"%(key,unpopSongSizes[key]))