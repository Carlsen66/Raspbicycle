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
import xml.etree.ElementTree as xml
#open the xml file for reading:
file = open('xmlfile.gpx','r')
#convert to string:
data = file.read()
tree = xml.fromstring(data)

#Get the root node
rootElement = tree

#Get a list of children elements with tag == "Books"
bookList = rootElement.findall("name")

#Check if any "Books" were found
if bookList != None:
	for book in bookList:
		#Do something with your book!
		
		print book 
