#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013 Carlsen <carlsen@carlsen-desktop>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
 
import xml.dom.minidom
from xml.dom.minidom import Node
from math import pi, sin, sqrt, cos, atan2, radians

	
def distance( lat1, lon1, lat2, lon2 ):
	R = 6371
	dLat = radians(lat2-lat1)
	dLon = radians(lon2-lon1)
	
	a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2))  * sin(dLon/2) * sin(dLon/2)
	
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	
	d = R * c
	
	return d


def main():
	lonlist = []
	latlist = []
	elelist = []
	c=0
	totdist=0
	totele=0
	eleup=0
	eledown=0
	lastele=0
	
	doc = xml.dom.minidom.parse("xmlfile.gpx")
 
	for node in doc.getElementsByTagName("trkpt"):
		lon = node.getAttribute("lon")
		lat = node.getAttribute("lat")
		elexml = node.getElementsByTagName("ele")[0].toxml()
		ele=elexml.replace('<ele>','').replace('</ele>','')
	
		lonlist.append(lon)
		latlist.append(lat)
		elelist.append(ele)
		c+=1
		#print "LON %s LAT %s ELE %s" % (lon, lat, ele)
	
	print "C = %d" % c	
	
	for i in range(0, c-1, 1): 
		lat1 = float(latlist[i])
		lat2 = float(latlist[i+1])
		lon1 = float(lonlist[i])
		lon2 = float(lonlist[i+1])
		ele = float(elelist[i])
		
		dist = distance(lat1, lon1, lat2, lon2)
		
		totdist +=dist
		
		if lastele == 0: lastele = ele
		
		if lastele > ele:
			ra = lastele-ele
			eledown +=lastele-ele
		else:
			ra = ele-lastele
			eleup +=ele-lastele
			
		lastele = ele
		
		print "LAT %s LON %s ELE %f DIST %f  ELE %f" % (lat1, lon1, ele, dist, ra)
		
	print "Total dist %f " % totdist
	
	print "Ele Up ele %f " % eleup
	print "Ele Down ele %f " % eledown
	
	return 0

if __name__ == '__main__':
	main()

