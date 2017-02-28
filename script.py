###############################################################################
# $Id$
#
# Project:	GDAL2Tiles, Google Summer of Code 2007 & 2008
#           Global Map Tiles Classes
# Purpose:	Convert a raster into TMS tiles, create KML SuperOverlay EPSG:4326,
#			generate a simple HTML viewers based on Google Maps and OpenLayers
# Author:	Klokan Petr Pridal, klokan at klokan dot cz
# Web:		http://www.klokan.cz/projects/gdal2tiles/
#
###############################################################################
# Copyright (c) 2008 Klokan Petr Pridal. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

##the following function was taken from the above open source code

def QuadTree(tx, ty, level):
	"Converts TMS tile coordinates to Microsoft QuadTree"
	quadKey = ""
	#print bin(tx), bin(ty)
	for i in range(level, 0, -1):
		digit = 0
		mask = 1 << (i-1)
		#print tx, ty, mask
		if (tx & mask) != 0:
			digit += 1
		if (ty & mask) != 0:
			digit += 2
		#print quadKey
		quadKey += str(digit)
	return quadKey


    
################## the following functions are no longer from the copyrighted project

import math
import sys
import urllib, cStringIO

#ensure latitude is in range of globe
def latBoundsCheck(latvalue):
	latRange = [-85.05112878, 85.05112878]
	return min(max(latvalue, latRange[0]), latRange[1])

#ensure longitude is in range of globe
def lonBoundsCheck(lonvalue):
	lonRange = [-180, 180]
	return min(max(lonvalue, lonRange[0]), lonRange[1])

def boundsCheck(value, min_check, max_check):
	return min(max(value, min_check), max_check)

#Convert Lat and Lon to pixels
def LatLonToPixels(lat, lon, level):
	"Converts lat/lon to pixel coordinates in given zoom of the EPSG:4326 pyramid"
	lat = latBoundsCheck(lat)
	lon = lonBoundsCheck(lon)
	sinlatitude = math.sin(lat * math.pi / 180)
	px = ((180 + lon) / 360) 
	py = 0.5 - math.log((1+sinlatitude)/(1-sinlatitude)) / (4*math.pi)
	map_scale = 256 * 2**level
	px_final = boundsCheck(px * map_scale + 0.5, 0, map_scale - 1)
	py_final = boundsCheck(py * map_scale + 0.5, 0, map_scale - 1)
	return px_final, py_final

#Convert Pixels to Tile Coordinates
def PixelsToTile(px, py):
	"Returns coordinates of the tile covering region in pixel coordinates"
	tx = int(math.floor(px / 256.0))
	ty = int(math.floor(py / 256.0))
	return tx, ty

#Calculate the center of inputted points
def centers(lat, lon, lat1, lon1):
	"Compute the centers"
	lat = float(lat)
	lon = float(lon)
	lat1 = float(lat1)
	lon1 = float(lon1)
	final_lat = (lat + lat1)/2.0
	final_lon = (lon + lon1)/2.0

	return final_lat, final_lon

#grabs both coordinates from command line input
lat = float(sys.argv[1])
lon = float(sys.argv[2])
lat1 = float(sys.argv[3])
lon1 = float(sys.argv[4])

def BingImageRetriever(center_lat, center_lon, level):
	#converts to pixels
	pix_x, pix_y = LatLonToPixels(center_lat, center_lon, level)
	#converts to tile coords
	tile_x, tile_y = PixelsToTile(pix_x, pix_y)
	#query quadkey corresponding tile coords
	quadkey = QuadTree(tile_x, tile_y, level)
	#url for specific quadkey
	URL = "http://h0.ortho.tiles.virtualearth.net/tiles/h" + quadkey + ".jpeg?g=131"
	urllib.urlretrieve(URL, "tile.jpg")
	return URL, quadkey

#calculates center of bounding box
center_lat, center_lon = centers(lat, lon, lat1, lon1)

#stops at the first level that returns non-error image
for level in xrange(23, 0, -1):
	URL, final_quadkey = BingImageRetriever(center_lat, center_lon, level)
	if open("error.jpg","rb").read() == open("tile.jpg","rb").read():
		pass
	else:
		print "Quadkey: " + str(final_quadkey)
		break
	
