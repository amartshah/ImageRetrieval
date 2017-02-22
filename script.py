import math


def centers(lat, lon, lat1, lon1):
	"Compute the centers"
	lat = float(lat)
	lat = float(lon)
	lat = float(lat1)
	lat = float(lon1)
	final_lat = (lat + lat1)/2.0
	final_lon = (lon + lon1)/2.0

	return final_lat, final_lon

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
def GoogleTile(tx, ty, zoom):
		"Converts TMS tile coordinates to Google Tile coordinates"
		
		# coordinate origin is moved from bottom-left to top-left corner of the extent
		return tx, (2**zoom - 1) - ty

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
