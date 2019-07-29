#!/usr/bin/env python

import pprint
 
import xml.dom.minidom
from xml.dom.minidom import Node
 
doc = xml.dom.minidom.parse("xmlfile.gpx")
 
mapping = {}
 
for node in doc.getElementsByTagName("trkpt"):
	lon = node.getAttribute("lon")
	lat = node.getAttribute("lat")
	elexml = node.getElementsByTagName("ele")[0].toxml()
	ele=elexml.replace('<ele>','').replace('</ele>','')
	
	
	print "LON %s LAT %s ELE %s" % (lon, lat, ele)
			
