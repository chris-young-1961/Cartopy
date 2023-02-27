#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:39:04 2022

@author: chrisyoung
"""
# Plot simple map of stations in IU  network; station info fetched from IRIS
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
        # Label station
        sta = get_sta(stachan)   #strip out STA code
        plt.text(coords['longitude'], coords['latitude'], 
                 sta,va="bottom", ha="left", fontsize=6,
                 transform=ccrs.Geodetic(),zorder = 7)
    stachan_prev = stachan    

# Save the plot by calling plt.savefig() BEFORE plt.show()
plt.savefig('GlobalIUMap.png', dpi = 300)

plt.show()