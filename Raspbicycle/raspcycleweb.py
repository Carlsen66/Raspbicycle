#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  raspberry fitness bike.py
#  
#  Copyright 2013 Carlsen66 (Johnny Carlsen)
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
import termios, sys, os, getopt
import RPi.GPIO as GPIO
import time
import datetime



def SaveData(dista, distb, ele, cad, speed, rise, motor):
	
	with open('/var/www/data.php', 'w') as f:
		f.write('<div class=divdata> <div id="databox"><p class="data">Distance (km)</p> <div id="webdata">')
		fstr = '%3.1f'%dista
		f.write(fstr)
		f.write('</div> </div><div id="databox"> <p class="data">Elevation</p> <div id="webdata">')
		fstr = '%3d'%ele
		f.write(fstr)
		f.write('</div> </div><div id="databox"> <p class="data">Rise (%)</p> <div id="webdata">')
		fstr = '%2.1d'%rise
		f.write(fstr)  
		f.write('</div></div></div></br><div class=divdata><div id="databox"><p class="data">Cadance</p><div id="webdata">')
		fstr = '%3d'%cad
		f.write(fstr)
		f.write('</div> </div> <div id="databox"><p class="data">Motor</p><div id="webdata">')
		fstr = '%3d'%motor
		f.write(fstr)
		f.write('</div> </div> <div id="databox"><p class="data">Speed</p><div id="webdata">')
		fstr = '%2.1d'%speed
		f.write(fstr)
		f.write('</div></div> </div>')
		f.close()
	
	
	return 0 
        
	
def distance( lat1, lon1, lat2, lon2 ):
	R = 6371
	dLat = radians(lat2-lat1)
	dLon = radians(lon2-lon1)
	
	a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2))  * sin(dLon/2) * sin(dLon/2)
	
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	
	d = R * c
	
	return d
	
	

def PhaseXMLFile(inputfile, latlist, lonlist, elelist):
	c=0
	
	doc = xml.dom.minidom.parse(inputfile)
 
	for node in doc.getElementsByTagName("trkpt"):
		lon = node.getAttribute("lon")
		lat = node.getAttribute("lat")
		elexml = node.getElementsByTagName("ele")[0].toxml()
		ele=elexml.replace('<ele>','').replace('</ele>','')
	
		lonlist.append(float(lon))
		latlist.append(float(lat))
		elelist.append(float(ele))
		c+=1
		#print "LAT %s LON %s ele %s" % (lat, lon, ele)
	return c	



def GetDistance(latlist, lonlist ):
	dist=0
	totdist=0
	totele=0
	eleup=0
	eledown=0
	lastele=0
	i=0
	j=0
	
	for lat in latlist:
		j+=1
		
	while i < j-1:	 
		lat1 = float(latlist[i])
		lat2 = float(latlist[i+1])
		lon1 = float(lonlist[i])
		lon2 = float(lonlist[i+1])
		
		i+=1
		dist = distance(lat1, lon1, lat2, lon2)
		
		totdist +=dist
		
		
	return totdist
	
	
	
def GetEle(elelist, eleupdown ):
	eleup=0
	eledown=0
	lastele=0
	ra=0
	
	for e in elelist: 
		ele = float(e)
		
		if lastele == 0: lastele = ele
		
		if lastele > ele:
			ra = lastele-ele
			eledown += ra
		elif lastele < ele:
			ra = ele-lastele
			eleup += ra
		
		lastele = ele
	
	eleupdown.append(eleup)
	eleupdown.append(eledown)
		
	return 0
	


	
def main(argv):
	lonlist = []
	latlist = []
	elelist = []
	eleupdown = []
	c=0
	i=0
	#http://www.bikecalc.com/gear_meters_of_development
	caddist= 0.0055 #padel turn in km
	leftdist = 0
	lastele=0
	motor_pos = 0
	motor_turns = 10
	datasaved =0
	cadspeed = 0
	
	MOTORINPUT = 11
	MOTORZERO = 9
	CADANCE = 8
	MOTORUP = 10
	MOTORDOWN = 22
	
	GPIO.setmode(GPIO.BCM)
	# Set up the GPIO channels - one input and one output
		
	GPIO.setup(MOTORINPUT, GPIO.IN)
	GPIO.setup(MOTORZERO, GPIO.IN)
	GPIO.setup(CADANCE, GPIO.IN)
	
	GPIO.setup(MOTORDOWN,GPIO.OUT) #DOWN
	GPIO.setup(MOTORUP,GPIO.OUT) #UP

	GPIO.output(MOTORDOWN, False)
	GPIO.output(MOTORUP, False)
	time.sleep(1)
	
	SaveData(0, 0, 0, 0, 0, 0, 0)
	
	while 1:
		with open('/var/www/data.dat', 'r') as d:
			data = d.read()
			
			if data == "START":
				#Move 'magnetic bar' in start position
				
						
				print "Move 'magnetic bar' in ZERO position\n"
				GPIO.output(MOTORDOWN, True)
				while GPIO.input(MOTORZERO) == 0 : time.sleep(0.1)
					
				GPIO.output(MOTORDOWN,False)
				time.sleep(0.5)
				
				#get filename form command promt
				inputfile = ''
				try:
					opts, args = getopt.getopt(argv,"hi:",["ifile="])
				except getopt.GetoptError:
					print '<program> -i <inputfile>'
					sys.exit(2)
				
				for opt, arg in opts:
					if opt == '-h':
						print '<program> -i <inputfile> '
						sys.exit()
					elif opt in ("-i", "--ifile"):
						inputfile = arg
					
				if inputfile == '':	inputfile = 'default.gpx'
				
				if not os.path.exists(inputfile): 
					print "gpx file don't exist %s" % inputfile
					sys.exit()
					
				print 'Input file is "', inputfile
				
				
				# PhaseXMLFile
				c = PhaseXMLFile(inputfile, latlist, lonlist, elelist)
				print "C = %d" % c
				
				#get total distance
				totdist = GetDistance(latlist, lonlist)
					
				print "Total dist {0:f} ".format(totdist)
				
				#Get total elevation up and down
				GetEle(elelist, eleupdown)
				
				print "Elevation Up ele {0:f} ".format(eleupdown[0])
				print "Elevation Down ele {0:f} ".format( eleupdown[1])
				print "\nBicycle computer v1.0\n"
				
				
				
				motor_steps = [170,170,170, 170, 170, 170, 170, 170, 180, 240, 260, 275, 284, 312, 324, 334, 342, 348, 353, 357, 360 ] 
				motor_startpos = motor_steps[10]			
				print "Move 'magnetic bar' in start position\n"
				
				motor_input_high=0
				GPIO.output(MOTORUP, True)
				while motor_pos < motor_startpos:
					motor_input = GPIO.input(MOTORINPUT)
					
					if motor_input == 1 and motor_input_high == 0:
						motor_input_high = 1
						motor_pos +=1
						#print "motor_pos = %d motor_startpos = %d" % (motor_pos, motor_startpos)
					if motor_input == 0 and motor_input_high == 1:
						motor_input_high = 0 
				
				GPIO.output(MOTORUP,False)
				GPIO.output(MOTORDOWN,False)
				print "motor_pos = {0:4d} motor_startpos = {1:4d}".format(motor_pos, motor_startpos)	
			
				time.sleep(2)
						
				i=0
				cadturn=0
				lastcadturn=0
				sumdist=0
				motor_ele=0
				stopbike=0		
						
				# **********************************************
				# Main loop program
				# **********************************************
				#
						
				for lat in latlist:	
					if lastele == 0 : lastele = elelist[i]
					try:
						ele = elelist[i+1] - lastele
					except:
						break;
					
					print "ele = %f elelist[i+1] = %f - lastele = %f"%(ele, elelist[i+1], lastele)
					
					dist = distance(latlist[i], lonlist[i], latlist[i+1], lonlist[i+1])
					
					if dist < caddist: dist = caddist
					eleprocent = (ele/(dist*1000)*100)
					intprocent = int(float(eleprocent)) 
					print "\nPosition {0:3d} lat {1:2.4f} lon {2:2.4f} ele {3:2.4} dist {4:3.3f} raise {5:3.2f} %".format(i, latlist[i], lonlist[i],elelist[i], (dist * 100), eleprocent )
					
					lastele = elelist[i+1]
					
					# elevation
					print "intprocent %d"% intprocent
					
					if intprocent > 10: intprocent = 10
					if intprocent < -10: intprocent = -10
					
					print "motor_steps %d "% motor_steps[10 + intprocent]
					
					motor_ele = (motor_steps[10 + intprocent]) - motor_pos 
					
					print "motor_ele( %s ) "%(motor_ele)
					eledir = 0
					
					if motor_ele >0:
						eledir = 2
						GPIO.output(MOTORUP, True)
						print "MOTORUP True"
						
					elif motor_ele < 0:
						eledir = 1
						GPIO.output(MOTORDOWN, True)
						print "MOTODOWN True"
					
					motor_input_high = 0
					cadan_input_high = 0	
					motor_input_reg  = 0
					saved = 0
					
					print "motor_ele = {0:3.3f} turns".format(motor_ele)
					while True:
						motor_input = GPIO.input(MOTORINPUT)
						
						if motor_input == 1 and motor_input_high == 0:
							motor_input_high = 1
						if motor_input == 0 and motor_input_high == 1:
							motor_input_high = 0
							motor_input_reg = 0
						if motor_input_high == 1 and motor_input_reg == 0:
							motor_input_reg = 1
							# watch motor position
							if eledir == 1:
								motor_pos -= 1
								motor_ele += 1
							elif eledir == 2:
								motor_pos += 1
								motor_ele -= 1  
							
							if motor_ele == 0:
								print "MOTOR STOP motor_pos {0:4d}".format(motor_pos)
								GPIO.output(MOTORUP, False)
								GPIO.output(MOTORDOWN, False)
								eledir = 0
						
								
						cadan_input = GPIO.input(CADANCE)
						
						if cadan_input == 1 and cadan_input_high == 0:
							cadan_input_high = 1
						if cadan_input == 0 and cadan_input_high == 1:
							cadan_input_high = 0
							cadturn += 1
							if dist >= caddist: 
								dist -= caddist
								sumdist += caddist
								print "dist {0:3.3f} caddist {1:3.3f}".format(dist, caddist)
								
							
						if dist < caddist and motor_ele == 0: break
						
						distb = totdist - sumdist
						dista = sumdist
						speed = (cadspeed*caddist)*60
						
						
						now = datetime.datetime.now()
						
						if (now.second % 10) == 0:
							if saved == 0:
								if cadturn > 1: 
									cadspeed = cadturn * (60/10)
									if lastcadturn == 0: lastcadturn = cadspeed
									cadspeed = (cadspeed + lastcadturn ) / 2
									lastcadturn = cadspeed
								
								#print "Dist {0:3.3f} motor_ele {1:3d}".format(dist, motor_ele)	
								print "motorpos = {0:3d} cadance = {1:3.1f} : {2:2.1f}Km distleft = {3:3.3f}".format(motor_pos, cadspeed, speed, distb)
								
								cadturn =0
								saved = 1
							
							with open('/var/www/data.dat', 'r') as d:
								data = d.read()
								
								if data == "PAUSE":
									time.sleep(1)
								if data == "STOP":
									stopbike = 1
									break
						else:
							saved = 0
						
						
						if(now.second % 2) == 0:
							if datasaved == 0:
								datasaved = 1	
								SaveData(dista, distb, elelist[i], cadspeed, speed, eleprocent, motor_pos)
						else:
							datasaved = 0
								
							
						if stopbike == 1:
							break
									
						
					i+=1
					if stopbike == 1:
						break
				
				
				print "Trip is over!"
				GPIO.output(MOTORDOWN, False)
				GPIO.output(MOTORUP, False)
				time.sleep(2)
				print "Resetting......"
				GPIO.output(MOTORDOWN, True)
				
				motorzero=0
				while motorzero == 0:
					motorzero = GPIO.input(MOTORZERO)
				
				GPIO.output(MOTORDOWN, False)
				
				print "DONE"
				
				
				
				
				
				
				
				
		time.sleep(1)
	
	return 0
	

if __name__ == '__main__':
	main(sys.argv[1:])

