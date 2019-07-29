#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bicycle Computer.py
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


def distance(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = radians(lat2-lat1)
    dLon = radians(lon2-lon1)

    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * \
        cos(radians(lat2)) * sin(dLon/2) * sin(dLon/2)

    c = 2 * atan2(sqrt(a), sqrt(1-a))

    d = R * c

    return d


def PhaseXMLFile(latlist, lonlist, elelist):
    c = 0

    doc = xml.dom.minidom.parse("xmlfile.gpx")

    for node in doc.getElementsByTagName("trkpt"):
        lon = node.getAttribute("lon")
        lat = node.getAttribute("lat")
        elexml = node.getElementsByTagName("ele")[0].toxml()
        ele = elexml.replace('<ele>', '').replace('</ele>', '')

        lonlist.append(float(lon))
        latlist.append(float(lat))
        elelist.append(float(ele))
        c += 1

    return c


def GetDistance(latlist, lonlist):
    dist = 0
    totdist = 0
    totele = 0
    eleup = 0
    eledown = 0
    lastele = 0
    i = 0
    j = 0

    for lat in latlist:
        j += 1

    while i < j-1:
        lat1 = float(latlist[i])
        lat2 = float(latlist[i+1])
        lon1 = float(lonlist[i])
        lon2 = float(lonlist[i+1])

        i += 1
        dist = distance(lat1, lon1, lat2, lon2)

        totdist += dist

        print("LAT %s LON %s DIST %5.2f " % lat1, lon1, dist)

    return totdist


def GetEle(elelist, eleupdown):
    eleup = 0
    eledown = 0
    lastele = 0
    i = 0

    for e in elelist:
        ele = float(elelist[i])
        i += 1

        if lastele == 0:
            lastele = ele

        if lastele > ele:
            ra = lastele-ele
            eledown += lastele-ele
        else:
            ra = ele-lastele
            eleup += ele-lastele

        lastele = ele

        # print "ELE %f" % (ra)

    # print "Ele Up ele %f " % eleup
    # print "Ele Down ele %f " % eledown

    eleupdown.append(eleup)
    eleupdown.append(eledown)

    return 0


def main():
    lonlist = []
    latlist = []
    elelist = []
    eleupdown = []
    c = 0
    i = 0
    candist = 0.1
    leftdist = 0
    lastele = 0

    c = PhaseXMLFile(latlist, lonlist, elelist)
    print("C = %d" % c)

    totdist = GetDistance(latlist, lonlist)

    print("Total dist %f " % totdist)

    GetEle(elelist, eleupdown)

    print("Ele Up ele %f " % eleupdown[0])
    print("Ele Down ele %f " % eleupdown[1])
    print("\nBicycle computer v1.0\n")
    for lat in latlist:
        if lastele == 0:
            lastele = elelist[i]
        ele = lastele - elelist[i]

        print("Pos lat %s lon %s ele %s" % latlist[i], lonlist[i], ele)
        dist = distance(latlist[i], lonlist[i], latlist[i+1], lonlist[i+1])
        print("Next position %f" % dist)

        lastele = elelist[i]

        # Change ele
        if ele > 0:
            print("set output for motor UP")
        else:
            print("set output for motor DOWN")

        # convert - to +
        if ele < 0:
            ele = ele - ele - ele

        # count input from motor
        while True:

            print("ele = %f " % ele)

            if ele == 0:
                break
            # get input form motor
            # if input:
            motor = raw_input("motor ")
            if motor == "m":
                ele -= 1  # we guess that one motor turn is equal to one ele/meter

        # get candance
        while True:
            # get input from candance
            candance = raw_input("candance ")
            if candance == "c":
                dist -= candist

            print("left dist %f" % dist)

            if dist <= 0:
                break

        i += 1

    return 0
