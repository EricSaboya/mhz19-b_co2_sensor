# !/usr/bin/python 
# ****************************************************************************
# Author: Eric Saboya, Dept. of Geographical Science, University of Bristol
# Contact: eric.saboya@bristol.ac.uk
# Created: 1-Oct-2022
# ****************************************************************************
# About
# Functions for analysing and plotting CO2 data
# ****************************************************************************
import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib import dates as dates


# Analysis functions
def read_co2_logfile(logfile):
	""" Read in csv logfile

	"""
	ds = pd.read_csv(logfile)
	time = pd.to_datetime(ds['time'])
	co2 = ds['CO2']
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

def propagate_uncert(cstdev, c_uncert_mean):
	""" propagate uncertainty values for five-min averaged data
	
	args:
		cstdev: standard deviation of concentration measurements in 
		        5-min period. 
		c_uncert_mean: average uncertainty value from 5-min period

	"""
	return np.sqrt((cstdev**2)+(c_uncert_mean**2))


# Plotting functions
def plot_timeseries(xdata, ydata, yerr, xlabel, ylabel, title, savefigure):
	""" Plot time series data
	 	args:
	 		xdata (float): x-axis data (usually datetime data)
	 		ydata (float): y-axis data 
	 		yerr (float): y-axis data error values
	 		xlabel (str): x-axis label
	 		ylabel (str): y-axis label
	 		title (str): figure title
	 		savefigure (str): path+fname for figure saving

	"""
	myFmt = dates.DateFormatter('%H:%M')

	fig, ax = plt.subplots(figsize=(10,6))
	ax.errorbar(xdata, 
		        ydata, 
		        yerr=yerr, 
		        fmt='o', 
		        ecolor='k', 
		        elinewidth=1.0, 
		        markersize=7.0, 
		        markerfacecolor='b', 
		        markeredgecolor='k', 
		        capsize=5, 
		        capthick=1.0)

	ax.set_xlabel(xlabel)
	ax.xaxis.set_major_formatter(myFmt)
	ax.set_ylabel(ylabel)
	ax.set_title(title)
	fig.tight_layout()
	plt.savefig(savefigure, dpi=300)
	plt.close()


