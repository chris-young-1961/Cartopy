#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:39:04 2022

@author: chrisyoung
"""

# Simple map of a single event and IU network stations, with great circle paths

import obspy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from obspy.clients.fdsn import Client

# Function to strip STA out of IU.STA.LOC.CHAN
def get_sta(stachan):
    sta = []
    index = 3
    while stachan[index] != '.':
        sta.append(stachan[index])
        index += 1
    sta = stachan[3:(index)]
    return sta

# Create IRIS client to fetch data
c = Client('IRIS')

# Get event information
UTC_str = '2011-03-11T05:46:23.2'     #Tohoku event
event_time = obspy.UTCDateTime(UTC_str)
cat = c.get_events(starttime = event_time - 10, endtime = event_time + 10, 
                    minmagnitude = 9)
origin = cat[0].preferred_origin()

# Get IU network station info
inv = c.get_stations(network = 'IU', station = '*', location = '00',
                      channel='BHZ',level='channel')

# Make lists of station names and coordinates (for plotting)
stachan_list = inv.get_contents()['channels']
coords_list = []
for stachan in stachan_list:
    coords = inv.get_coordinates(stachan)
    coords_list.append(coords)

# Create world map with colored land/ocean and coastlines
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
# ax.coastlines()

# Plot event
event_color = (220/255, 20/255, 60/255)   #crimson
plt.plot(origin.longitude, origin.latitude,
          marker='*', markerfacecolor=event_color, 
          markeredgecolor = event_color,transform=ccrs.Geodetic(),
          zorder=10)

# Plot stations
sta_color = (255/255, 140/255, 0/255)   #dark orange
stachan_prev = ()
for stachan, coords in zip(stachan_list, coords_list):
    if stachan != stachan_prev:
        # Plot station
        plt.plot(coords['longitude'], coords['latitude'],
                  marker='^', markersize=2, markerfacecolor=sta_color, 
                  markeredgecolor = sta_color,transform=ccrs.Geodetic(), 
                  zorder=5)
        # Path from event to station
        plt.plot([origin.longitude, coords['longitude']],[origin.latitude, coords['latitude']], 
                 color='black', linewidth=0.5,linestyle='--',
                 transform=ccrs.Geodetic(),zorder = 6)
        # Label station
        sta = get_sta(stachan)   #strip out STA code
        plt.text(coords['longitude'], coords['latitude'], 
                 sta,va="bottom", ha="left", fontsize=6,
                 transform=ccrs.Geodetic(),zorder = 7)
    stachan_prev = stachan    

# Save the plot by calling plt.savefig() BEFORE plt.show()
plt.savefig('GlobalIUMapWithEvent.png', dpi = 300)

plt.show()