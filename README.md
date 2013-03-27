RaspberryPiSolarLogger
======================

Raspberry Pi and I2C based solar energy logging system

Interfacing various I2C devices via a custom addon PCB to Raspberry Pi

ADC conversion using a pair of MCP3428 16-Bit, Multi-Channel Analog-to-Digital Converter with I2C Interface and On-Board Reference by Microchip which have 4 input channels. Board also has a buffer to allow 5V I2C sensors to work with the 3.3V levels on the Raspberry Pi board.

Blog post on http://www.briandorey.com/post/Raspberry-Pi-I2C-Analog-to-Digital-Converter.aspx has photos of the prototype board.

Update 24th July 2012
Added final python script to save data from I2C sensors and 1-Wire sensors and send to web server every minute.