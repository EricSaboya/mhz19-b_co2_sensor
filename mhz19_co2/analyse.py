# !/usr/bin/python 
# ****************************************************************************
# Author: Eric Saboya, Dept. of Geographical Science, University of Bristol
# Contact: eric.saboya@bristol.ac.uk
# Created: 2-Oct-2022
# ****************************************************************************
# About
# Analyse datalogger script
# ****************************************************************************
import os
import numpy as np
import pandas as pd 


def read_co2_logfile(logfile):
	ds = pd.read_csv(logfile)
	time = pd.to_datetime(ds['time'])
	co2 = ds['co2']
	co2_err = ds['uncertainty']
	return time, co2, co2_err


def data_five_minute_ave(t_data, c_data):
	""" Average 10s CO2 sensor data to five minute averaged data

	args:
		t_data: (datetime) time stamp values. 
		c_data: (float) correspsonding concentration data

	returned time stamp values are for the midde of the interval

	"""
	co2_5min_mean = []
	co2_5min_stdev = []
	time_5min = []

	n_len=len(t_data)
	for i in range(0, n_len-30, 30):
		time_mid = ((t_data[i+30]-t_data[i])/2) + t_data[i]
		time_5min.append(time_mid)

		co2_mean = np.nanmean(c_data[i:i+30])
		co2_5min_mean.append(co2_mean)
		co2_stdev = np.std(c_data[i:i+30])
		co2_5min_stdev.append(co2_stdev)

	return np.array(time_5min), np.array(co2_5min_mean), np.array(co2_5min_stdev)



