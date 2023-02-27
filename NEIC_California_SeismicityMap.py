#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:39:04 2022

@author: chrisyoung
"""
# Reads in NEIC catalog from IRIS for specifed time interval, plots events on 
# CONUS map with symbols scaled by magnitude and colored by depth.

import obspy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from obspy.clients.fdsn import Client

# Create IRIS client to fetch data
c = Client('IRIS')

# Get event information
min_mag = 2.5
max_mag = 6.5
min_latitude = 28.
max_latitude = 43.
min_longitude = -128.
max_longitude = -111.
start_str = '2018-01-01T00:00:00.0'
end_str =   '2022-12-01T00:00:00.0'
start_time = obspy.UTCDateTime(start_str)
end_time = obspy.UTCDateTime(end_str)
cat = c.get_events(starttime = start_time, endtime = end_time, 
                    minlatitude = min_latitude, maxlatitude = max_latitude,
                    minlongitude=min_longitude, maxlongitude = max_longitude,
                    minmagnitude = min_mag, maxmagnitude = max_mag, catalog = 'NEIC PDE')

# Create world map with colored land/ocean and coastlines
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([min_longitude, max_longitude, min_latitude, max_latitude], crs=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE,linestyle='-',linewidth=0.3)
ax.add_feature(cfeature.STATES, linestyle='-',linewidth=0.2)
ax.add_feature(cfeature.LAKES, alpha=0.5,linewidth=0.1)
# ax.add_feature(cfeature.RIVERS)

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
            
        # print('mag: ', magnitude.mag, ' size: ', marker_size)
        plt.plot(origin.longitude, origin.latitude,
                 marker='o', markerfacecolor=event_color, 
                 markeredgecolor = 'black', markersize = marker_size,
                 markeredgewidth = 0.2,
                 transform=ccrs.Geodetic(),
                 zorder=1)

# Add some labels at the bottom of the map
# Create a Rectangle patch for legend
patch_color = (240/255, 255/255, 244/255)  #honeydew
rect = patches.Rectangle((min_longitude, min_latitude), max_longitude-min_longitude,
                          1.7, linewidth=1, edgecolor='k', facecolor=patch_color)
ax.add_patch(rect)
# Add legend text and symbols
y_top = min_latitude + 1.3     #legend labels at this latitude and below
y_inc = 0.3      #subsequent lines are this far below
textcolor = (0/255, 0/255, 0/255)  #black
# Catalog info
x_left = 0.5 * (max_longitude + min_longitude) + 1.5
ax.text(x_left, y_top, 'NEIC PDE Catalog', rotation=0.0,
        color=textcolor, va="center", ha="center", fontsize=4, 
        fontweight = 'bold',zorder=10)
ax.text(x_left, y_top - 1.*y_inc, start_str + ' to ' + end_str, rotation=0.0,
        color=textcolor, va="center", ha="center", fontsize=4, zorder=10)
ax.text(x_left, y_top - 2.*y_inc, 'magnitude ' + str(min_mag) + ' to ' + str(max_mag), 
        rotation=0.0,
        color=textcolor, va="center", ha="center", fontsize=4, zorder=10)
ax.text(x_left, y_top - 3.*y_inc, str(event_count) + ' events', rotation=0.0,
        color=textcolor, va="center", ha="center", fontsize=4, zorder=10)
# Mag range legend
x_space = 0.2
x_left = max_longitude - 2.00
ax.text(x_left, y_top, 'magnitude', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, 
        fontweight = 'bold', zorder=10)
ax.text(x_left, y_top - y_inc, str(max_mag), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space,y_top - y_inc, marker='o', markerfacecolor=depth_color_list[0],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
ax.text(x_left, y_top - 2.*y_inc, str((min_mag+max_mag)/2.), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space,y_top - 2.*y_inc, marker='o', markerfacecolor=depth_color_list[0],
          markeredgecolor = 'black', markersize = (min_marker_size+max_marker_size)/2.,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
ax.text(x_left, y_top - 3.*y_inc, str(min_mag), rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space,y_top - 3.*y_inc, marker='o', markerfacecolor=depth_color_list[0],
          markeredgecolor = 'black', markersize = min_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
# Depth range legend
x_left = min_longitude + 0.5
marker_size = 0.5*(max_marker_size - min_marker_size)
ax.text(x_left, y_top, 'depth [km]', rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, 
        fontweight = 'bold', zorder=10)
depth_str = '0 to ' + str(depth_list[0])
ax.text(x_left, y_top - y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space, y_top - y_inc, marker='o', markerfacecolor=depth_color_list[0],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
depth_str = str(depth_list[0]) + ' to ' + str(depth_list[1])
ax.text(x_left, y_top - 2.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space,y_top - 2.*y_inc, marker='o', markerfacecolor=depth_color_list[1],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
depth_str = str(depth_list[1]) + ' to ' + str(depth_list[2])
ax.text(x_left, y_top - 3.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space,y_top - 3.*y_inc, marker='o', markerfacecolor=depth_color_list[2],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
x_left = x_left + 2.55
depth_str = str(depth_list[2]) + ' to ' + str(depth_list[3])
ax.text(x_left, y_top - y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space,y_top - y_inc, marker='o', markerfacecolor=depth_color_list[3],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
depth_str = str(depth_list[3]) + ' to ' + str(depth_list[4])
ax.text(x_left, y_top - 2.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space,y_top - 2.*y_inc, marker='o', markerfacecolor=depth_color_list[4],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)
depth_str = '> ' + str(depth_list[4]) 
ax.text(x_left, y_top - 3.*y_inc, depth_str, rotation=0.0,
        color=textcolor, va="center", ha="left", fontsize=4, zorder=10)
plt.plot(x_left - x_space,y_top - 3.*y_inc, marker='o', markerfacecolor=depth_color_list[5],
          markeredgecolor = 'black', markersize = max_marker_size,
          markeredgewidth = 0.2,transform=ccrs.Geodetic(),zorder=10)

# Save the plot by calling plt.savefig() BEFORE plt.show()
plt.savefig('NEIC California_seismicity_map.png', dpi = 300)
plt.show()