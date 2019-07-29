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
import xml.etree.cElementTree as et


#open the xml file for reading:
file = open('xmlfile.xml','r')
#convert to string:
data = file.read()
tree=et.fromstring(data)
file.close()

#close file because we dont need it anymore:

print ("tag %s" % tree.tag)
print ("attrib %s"  % tree.attrib)

print "sec loop"
	
for dt in tree.findall('file'):
	lat = dt.get('lat')
	lon = dt.get('lon')
	ele = dt.find('Name').text
	print lat, lon, ele


