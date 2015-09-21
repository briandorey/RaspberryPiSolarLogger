#!/usr/bin/env python

#
# read sensors from https://www.wirelessthings.net/wireless-temperature-sensor
# using USB wireless dongle SRF Stick - USB Radio (868-915Mhz)
# https://www.wirelessthings.net/srf-stick-868-915-mhz-easy-to-use-usb-radio
# and display to screen, each sensor has an ID starting with:
# TA or TB
#
import serial 
baud = 9600 
port = '/dev/ttyACM0' 
ser = serial.Serial(port, baud) 
ser.timeout = 2 



def formatResult(resultvalue):
	if resultvalue is not None:
		if resultvalue.startswith("TBTEMP"):
			valnum = resultvalue.replace("TBTEMP", "")
			print("TB: %.1f" % round(float(valnum),2))
			
		if resultvalue.startswith("TATEMP"):
			valnum = resultvalue.replace("TATEMP", "")
			print("TA: %.1f" % round(float(valnum),2))
	


while(1): 
	if ser.inWaiting() >= 12: 
		if ser.read() == 'a':
			tmpval = ser.read(11)
			#print tmpval
			formatResult(tmpval) 

ser.close
