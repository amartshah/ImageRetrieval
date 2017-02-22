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

"""
globalmaptiles.py

Global Map Tiles as defined in Tile Map Service (TMS) Profiles
==============================================================

Functions necessary for generation of global tiles used on the web.
It contains classes implementing coordinate conversions for:

  - GlobalMercator (based on EPSG:900913 = EPSG:3785)
       for Google Maps, Yahoo Maps, Microsoft Maps compatible tiles
  - GlobalGeodetic (based on EPSG:4326)
       for OpenLayers Base Map and Google Earth compatible tiles

More info at:

http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification
http://wiki.osgeo.org/wiki/WMS_Tiling_Client_Recommendation
http://msdn.microsoft.com/en-us/library/bb259689.aspx
http://code.google.com/apis/maps/documentation/overlays.html#Google_Maps_Coordinates

Created by Klokan Petr Pridal on 2008-07-03.
Google Summer of Code 2008, project GDAL2Tiles for OSGEO.

In case you use this class in your product, translate it to another language
or find it usefull for your project please let me know.
My email: klokan at klokan dot cz.
I would like to know where it was used.

Class is available under the open-source GDAL license (www.gdal.org).
"""
#####the following helper functions were taken from the open source project cited above  
import math

def LatLonToPixels(lat, lon, zoom):
	"Converts lat/lon to pixel coordinates in given zoom of the EPSG:4326 pyramid"

	res = 180 / 256.0 / 2**zoom
	px = (180 + lat) / res
	py = (90 + lon) / res
	return px, py

def PixelsToTile(px, py):
	"Returns coordinates of the tile covering region in pixel coordinates"

	tx = int( math.ceil( px / float(self.tileSize) ) - 1 )
	ty = int( math.ceil( py / float(self.tileSize) ) - 1 )
	return tx, ty

def Resolution(zoom ):
	"Resolution (arc/pixel) for given zoom level (measured at Equator)"
	
	return 180 / 256.0 / 2**zoom
	#return 180 / float( 1 << (8+zoom) )

def TileBounds(tx, ty, zoom):
	"Returns bounds of the given tile"
	res = 180 / 256.0 / 2**zoom
	return (
		tx*256*res - 180,
		ty*256*res - 90,
		(tx+1)*256*res - 180,
		(ty+1)*256*res - 90
	)


def QuadTree(tx, ty, zoom ):
	"Converts TMS tile coordinates to Microsoft QuadTree"
	
	quadKey = ""
	ty = (2**zoom - 1) - ty
	for i in range(zoom, 0, -1):
		digit = 0
		mask = 1 << (i-1)
		if (tx & mask) != 0:
			digit += 1
		if (ty & mask) != 0:
			digit += 2
		quadKey += str(digit)
	return quadKey


##### own code

def centers(lat, lon, lat1, lon1):
	"Compute the centers"
	lat = float(lat)
	lat = float(lon)
	lat = float(lat1)
	lat = float(lon1)
	final_lat = (lat + lat1)/2.0
	final_lon = (lon + lon1)/2.0

	return final_lat, final_lon