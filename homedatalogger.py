#!/usr/bin/env python3
#solar voltage, current and temperature data logging system
# project log on www.briandorey.com
# -----------------------
import quick2wire.i2c as i2c
import os
import time
import re
import datetime
import urllib.request

varCurrentMinute = 0
varPrevMinute = 0
varNow = datetime.datetime.now()

# 1 wire temperature sensors
path1="/mnt/1wire/28.5B7DC4030000/temperature"
path2="/mnt/1wire/28.8C37C4030000/temperature"
path3="/mnt/1wire/28.611555030000/temperature"
path4="/mnt/1wire/28.8945C4030000/temperature"

# I2C temperature sensor
temphomeaddress = 0x4B



# I2C ADC chip addresses
adc_address1 = 0x68
adc_address2 = 0x69

adc_channel1 = 0x98
adc_channel2 = 0xB8
adc_channel3 = 0xD8
adc_channel4 = 0xF8

# setup variables with default values
varPumpRunning = 0
varDCVolts = 0.0
varDCAmps = 0.0
varACAmps = 0.0
varInverterAmps = 0.0
varPVAmps = 0.0

varTempHome = 0.0

varTempBase = 0.0
varTempBaseNew = 0.00
varTempTop = 0.0
varTempTopNew = 0.00
varTempCollector = 0.0
varTempCollectorNew = 0.00

print("Logging Started")

# functions to read and process data
def get1wiretempreading(path):
	try:
		time.sleep(2)
		f = open(path,"r")
		text = f.readlines()
		#f.close()
		return float(text[0]) + 3
	except:
		print ("getwiretemp failed")		
		return 88
	
with i2c.I2CBus() as bus:
	

	def getadcreading(address, channel):
		try:
			bus.transaction(i2c.write_bytes(address, channel))
			time.sleep(0.05)
			h, l, r = bus.transaction(i2c.read(address,3))[0]
			time.sleep(0.05)
			h, l, r = bus.transaction(i2c.read(address,3))[0]
			
			t = (h << 8 | l)
			if (t >= 32768):
				t = 655361 -t
			#v = (t * 2.048/32768.0	)
			v = (t * 0.000154	)
			return v
		except:
			print ("getadcreading failed")	
			return 0.00	
		
	def getI2CTemp():
		try:
			sensora, sensorb = bus.transaction(i2c.write_bytes(temphomeaddress, 0x00),
			i2c.read(temphomeaddress,2))[0]
			
			temp = (sensora << 8 | sensorb) /256
			return temp
		except:
			print ("get i2ctemp failed")	
			return 0.00	
		
	def calcDCCurrent(inval):
		return ((inval) - 2.466) / 0.066;
		
	def calcInverterCurrent(inval):
		return ((inval) - 2.4988) / 0.066;
		
	def calcSolarCurrent(inval):
		return ((inval) - 2.477) / 0.066;	
		
	def calcDCVolts(inval):
		
		return inval * 4.6256;
		
	def calcACCurrent(inval):
		return (inval * 20);		
	
	def calcPumpRunning(inval):
		if (inval > 0.5):
			return 1
		else:
			return 0 
			
	def DoUpload():
		# do server update
		try:
			f = urllib.request.urlopen('http://10.0.0.125/save.aspx?'
			+ 'watertop=' + str(varTempTop)
			+ '&waterbase=' + str(varTempBase)
			+ '&solar=' + str(varTempCollector)
			+ '&home=' + str(varTempHome)
			+ '&Irms=' + str(varACAmps)
			+ '&iSolar=' + str(varPVAmps)
			+ '&vbattery=' + str(varDCVolts)
			+ '&iInverter=' + str(varInverterAmps)
			+ '&iDCLine=' + str(varDCAmps)
			+ '&pump=' + str(varPumpRunning)
			+ '')
		
			print (f.read(100))
		except:
			print ("http connection failed")	
		
		
		
		
		
		
				
	# init temp sensor
	bus.transaction(i2c.write_bytes(temphomeaddress, 0x01, 0x60))
	bus.transaction(i2c.write_bytes(temphomeaddress, 0x01))
	
	while True:
		
		# read sensors into temp variables
		varPumpRunning = calcPumpRunning(getadcreading(adc_address1, adc_channel1))
		varDCVolts = calcDCVolts(getadcreading(adc_address1, adc_channel2))
		varDCAmps = calcDCCurrent(getadcreading(adc_address2, adc_channel1))
		varACAmps = calcACCurrent(getadcreading(adc_address2, adc_channel2))
		varInverterAmps = calcInverterCurrent(getadcreading(adc_address2, adc_channel3))
		varPVAmps = calcSolarCurrent(getadcreading(adc_address2, adc_channel4))

		varTempHome = getI2CTemp()
		
		# read 1-Wire sensors and update values if not error value (85 + 3 caculation factor)
		varTempBaseNew = get1wiretempreading(path2)
		if (varTempBaseNew != 88):
			varTempBase = varTempBaseNew
			
		varTempTopNew = get1wiretempreading(path4)
		if (varTempTopNew != 88):
			varTempTop = varTempTopNew
		
		varTempCollectorNew = get1wiretempreading(path1)
		if (varTempCollectorNew != 88):
			varTempCollector = varTempCollectorNew
		
		print ("Pump: %02f" % varPumpRunning)
		print ("DC Volts: %02f" % varDCVolts)
		
		print ("DC A: %02f" % varDCAmps)
		print ("Mains A: %02f" % varACAmps)
		print ("Inverter A: %02f" % varInverterAmps)
		print ("PV A: %02f" % varPVAmps)
		
		print ("Home Temp: %02f" %  varTempHome)
		
		
		print("Tank Base: %03f" % varTempBase)
		print("Tank Top: %03f" % varTempTop)
		print("Collector: %03f" % varTempCollector)
		
		# spare sensor inputs
		#print("PI Box: %03f" % get1wiretempreading(path3))
		#print ("Channel 3: %02f" % getadcreading(adc_address1, adc_channel3))
		#print ("Channel 4: %02f" % getadcreading(adc_address1, adc_channel4))
		
		
		# get current datetime and see if minute is different to previous minute
		varNow = datetime.datetime.now()
		print (str(varNow))
		varCurrentMinute = varNow.minute
		if (varCurrentMinute != varPrevMinute):
			varPrevMinute = varCurrentMinute
			DoUpload()
		# sleep for 1 second and repeat	
		time.sleep(1)	
