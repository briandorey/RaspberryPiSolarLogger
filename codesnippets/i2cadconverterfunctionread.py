#!/usr/bin/env python3

#read MCP3428 16-Bit, Multi-Channel Analog-to-Digital Converter with I2C Interface and On-Board Reference using Raspberry Pi
#	ADC Address Pins Config:
#
#	L & L = 0x68
#	F & F = 0x68
#	L & F = 0x69
#	L & H = 0x6A
#	F & L = 0x6B
#	H & L = 0x6C
#	H & F = 0x6D
#	H & H = 0x6E
#	F & H = 0x6F


import quick2wire.i2c as i2c

import time

adc_address1 = 0x68
adc_address2 = 0x69

adc_channel1 = 0x98
adc_channel2 = 0xB8
adc_channel3 = 0xD8
adc_channel4 = 0xF8

with i2c.I2CBus() as bus:
	

	def getadcreading(address, channel):
		bus.transaction(i2c.write_bytes(address, channel))
		time.sleep(0.05)
		h, l, r = bus.transaction(i2c.read(address,3))[0]
		time.sleep(0.05)
		h, l, r = bus.transaction(i2c.read(address,3))[0]
		
		t = (h << 8 | l)
		if (t >= 32768):
			t = 655361 -t
		v = t * 2.048/32768.0	
		
		return v
	
	while True:
		

		print ("Channel 3: %02f" % getadcreading(adc_address1, adc_channel3))
		print ("Channel 4: %02f" % getadcreading(adc_address1, adc_channel4))
		
		time.sleep(1)	
