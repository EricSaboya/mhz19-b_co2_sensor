# !/usr/bin/python 
# ****************************************************************************
# Author: Eric Saboya, Dept. of Geographical Science, University of Bristol
# Contact: eric.saboya@bristol.ac.uk
# Created: 1-Oct-2022
# ****************************************************************************
# About
# MH-Z19 Python datalogger script for CO2 measurements (direct from laptop)
# ****************************************************************************

import os 
import sys
import csv 
import time 
import serial 
import datetime as dt 
import traceback 

def logfilename():
	"""Create datalogging file with appropriate time stamp  
	"""
	now=dt.datetime.now()
	return 'CO2LOG-%0.4d-%0.2d-%0.2d-%0.2d%0.2d%0.2d.csv' % (now.year, now.month, now.day, now.hour, now.minute ,now.second)

def connect_serial(serial_dev):
	""" Interface with CO2 mh-z19b sensor (connect via USB)
	"""
	return serial.Serial(serial_dev, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1.0)

def read_concentration():
	""" Reads CO2 concentration from sensor
	"""
	# Change serial_dev to correpsond to computer's port
	serial_dev="/dev/tty.usbserial-0001"
	# Number of attempts to acquire data
	retry_count=3 
	try:
		ser=connect_serial(serial_dev)
		for retry in range(retry_count):
			result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
			s=ser.read(9)
			if len(s)>=4 and s[0]==0xff and s[1]==0x86:
				# Calculate concentration according to datasheet
				return s[2]*256+s[3]
	except:
		traceback.print_exc()
	return ""

def mh_z19():
	""" If CO2 values exist, insert into dict.
	"""
	co2=read_concentration()
	if not co2:
		return {}
	else:
		return {'co2':co2}

def concentration_uncert(c):
	""" Calculate concentration uncertainty based on manual
	"""
	uncert = c*0.05 + 50
	return uncert

def main():
	outfname=logfilename()
	try:
		with open(outfname, 'a') as f:
		f.write("time, CO2, uncertainty\n")
			while True:
				co2=mh_z19()
				now=time.ctime()
				parsed=time.strptime(now)
				lgtime=time.strftime("%Y-%m-%d %H:%M:%S")
				row=[lgtime, co2['co2']]
				print('Time Stamp: ',lgtime, ', CO2 concentration: ', co2['co2'],'ppm')
				# Calculate uncertainties
				uncert = concentration_uncert(co2['co2'])
				# Write data to file.
				f.write(str(lgtime)+','+str(co2['co2'])+','+str(uncert)+'\n')
				measuretime=10
				time.sleep(measuretime)
	except KeyboardInterrupt as e:
		f.close()
		sys.stderr.write('nCtrl+C pressed, exiting log of %s' % (outfname))


if __name__ == "__main__":
	main()
