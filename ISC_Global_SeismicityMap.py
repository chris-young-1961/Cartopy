#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:39:04 2022

@author: chrisyoung
"""
# Reads in ISC catalog for specifed time interval, plots events on global map with
# symbols scaled by magnitude and colored by depth.

import obspy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from obspy.clients.fdsn import Client

# Create IRIS client to fetch data
c = Client('IRIS')

# Get event information
min_mag = 4.0
max_mag = 7.0
start_str = '2010-01-01T00:00:00.0'
end_str =   '2012-01-01T00:00:00.0'
start_time = obspy.UTCDateTime(start_str)
end_time = obspy.UTCDateTime(end_str)
cat = c.get_events(starttime = start_time, endtime = end_time, 
                    minmagnitude = min_mag, maxmagnitude = max_mag, catalog = 'ISC')

# Create world map with colored land/ocean and coastlines
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()

# Plot catalog events
depth_list = [35.,70.,150.,300.,500.]
depth_color_list = [(220/255, 20/255, 60/255),  #crinmson
                    (255/255, 140/255, 0/255),  #dark orange
                    (255/255, 215/255, 0/255),  #gold
                    (0/255,128/255, 0/255),     #green
                    (0/255, 0/255, 255/255),    #blue
                    (138/255, 43/255, 226/255)] #blue violet
min_marker_size = 1
max_marker_size = 3
marker_scale_fac = (max_marker_size - min_marker_size)/(max_mag - min_mag)
                
event_count = 0                    
for event in cat:
    origin = event.preferred_origin()
    magnitude = event.preferred_magnitude()

    # Only plot events with depth and magnitude
    if (type(origin.depth) is float) & (type(magnitude.mag) is float):
        event_count += 1
        # Event size scaled by magnitude
        marker_size = min_marker_size + (magnitude.mag - min_mag)*marker_scale_fac
        # Event color by depth
        depth = origin.depth/1000.
        if depth <= depth_list[0]:
            event_color = depth_color_list[0]
        elif depth <= depth_list[1]:
            event_color = depth_color_list[1]
        elif depth <= depth_list[2]:
            event_color = depth_color_list[2]
        elif depth <= depth_list[3]:
            event_color = depth_color_list[3]
        elif depth <= depth_list[4]:
            event_color = depth_color_list[4]
        else:
            event_color = depth_color_list[5]
            
        plt.plot(origin.longitude, origin.latitude,
                 marker='o', markerfacecolor=event_color, 
                 markeredgecolor = 'black', markersize = marker_size,
                 markeredgewidth = 0.2,
                 transform=ccrs.Geodetic(),
                 zorder=10)

# Add some labels at the bottom of the map
y_top = -74.     #legend labels at this latitude and below
y_inc = 4.      #subsequent lines are this far below
textcolor = (0/255, 0/255, 0/255)  #black
# Catalog info
ax.text(0.0, y_top - y_inc, 'ISC Catalog', rotation=0.0,
        color=textcolor, va="center", ha="center", fontsize=4, 
        fontweight = 'bold',zorder=10)
ax.text(0.0, y_top - 2.*y_inc, start_str + ' to ' + end_str, rotation=0.0,
        color=textcolor, va="center", ha="center", fontsize=4, zorder=10)
ax.text(0.0, y_top - 3.*y_inc, str(event_count) + ' events', rotation=0.0,
        color=textcolor, va="center", ha="center", fontsize=4, zorder=10)
# Mag range legend
x_left = 150.
ax.text(x_left, y_top, 'magnitude', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, 
        fontweight = 'bold', zorder=10)
ax.text(x_left, y_top - y_inc, str(max_mag), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4,y_top - y_inc, marker='o', markerfacecolor=depth_color_list[0],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
ax.text(x_left, y_top - 2.*y_inc, str((min_mag+max_mag)/2.), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4,y_top - 2.*y_inc, marker='o', markerfacecolor=depth_color_list[0],
          markeredgecolor = 'black', markersize = (min_marker_size+max_marker_size)/2.,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
ax.text(x_left, y_top - 3.*y_inc, str(min_mag), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4,y_top - 3.*y_inc, marker='o', markerfacecolor=depth_color_list[0],
          markeredgecolor = 'black', markersize = min_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
# Depth range legend
x_left = -170.
marker_size = 0.5*(max_marker_size - min_marker_size)
ax.text(x_left, y_top, 'depth [km]', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, 
        fontweight = 'bold', zorder=10)
depth_str = '0 to ' + str(depth_list[0])
ax.text(x_left, y_top - y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4, y_top - y_inc, marker='o', markerfacecolor=depth_color_list[0],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
depth_str = str(depth_list[0]) + ' to ' + str(depth_list[1])
ax.text(x_left, y_top - 2.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4,y_top - 2.*y_inc, marker='o', markerfacecolor=depth_color_list[1],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
depth_str = str(depth_list[1]) + ' to ' + str(depth_list[2])
ax.text(x_left, y_top - 3.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4,y_top - 3.*y_inc, marker='o', markerfacecolor=depth_color_list[2],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
x_left = x_left + 40.
depth_str = str(depth_list[2]) + ' to ' + str(depth_list[3])
ax.text(x_left, y_top - y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4,y_top - y_inc, marker='o', markerfacecolor=depth_color_list[3],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
depth_str = str(depth_list[3]) + ' to ' + str(depth_list[4])
ax.text(x_left, y_top - 2.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4,y_top - 2.*y_inc, marker='o', markerfacecolor=depth_color_list[4],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
depth_str = '> ' + str(depth_list[4]) 
ax.text(x_left, y_top - 3.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - 4,y_top - 3.*y_inc, marker='o', markerfacecolor=depth_color_list[5],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)

# Save the plot by calling plt.savefig() BEFORE plt.show()
plt.savefig('ISC_Global_SeismicityMap.png', dpi = 300)
plt.show()