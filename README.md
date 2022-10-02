# mhz19-b_co2_sensor
**About:** 
Python code to interface the MHZ19-b CO2 low-cost sensor with a laptop. 
Code shows the CO2 readings in real-time and saves values to a csv file.
______________________________________________________________________________
**Description**

The MHZ19-b CO2 sensor is a low-cost NDIR (non-dispersive infrared) sensor
that is manufactured by Winsen Lt., China. This sensor has been often 
used in Raspberry Pi projects for monitoring ambient CO2 concentrations (though
with much larger uncertainties than high-cost instruments such as a Picarro or 
Aerodyne spectrometer).


Here, I present Python code for interfacing this MHZ-19b sensor with a 
laptop using a usb connector. (See below for connection description)

The Python script: mhz19_co2.py, when run, will look for the CO2 sensor 
connection and if found will print the time stamp and CO2 concentration every 
ten seconds. These values, plus the uncertainty (quoted as ±50 ppm + 5% 
concentration value in the MHZ-19b user manual). Data will be saved to a log file.
The script will continue to run until ctrl-c keyboard interrupt is used.

Note. In the mhz19_co2.py file within the function "connect_serial" one will have
to change the serial_dev path to correspond to the port used on one's laptop.

______________________________________________________________________________
**Sensor setup**
There are 9 pins in the MHZ-19b sensor. Only four connections are needed:

1. +5v (usb) --> Vin (MHZ-19b)
2. GND (usb) --> GND (MHZ-19b)
3. TXD0 (usb) --> RXD (MHZ-19b)
4. RXD0 (usb) --> TXD (MHZ-19b)

See photo in the labelled file.
