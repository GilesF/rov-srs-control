#!/usr/bin/python
# Copyright 2015, Jonathan Lee
# Distributed under the terms of the BSD 3-Clause License
#
#
# ROV_SRS_Main
#
#
# Overview:	The main runtime script to handle SRS Control.
#
# Authors:	Jonathan Lee
#

from collections import deque

import Adafruit_BBIO.GPIO as GPIO
import ROV_SRS_Library as SRS

#
# Constant Definitions.
#

# General Program Constants.
PWM_AVG_NUM  = 5		# Pulses to average before state transitions.
PWM_WID_FREQ = 70		# Expected signal frequency [Hz].
PWM_WID_MAX  = 14		# Input signal maximum duty cycle [%].
PWM_WID_MIN  = 7		# Input signal minimum duty cycle [%].
PWM_WID_TOL  = 20		# Tolerance on Pulse Width Deviations [%].

POS_HIST_NUM = 5		# Previous Position Commands to compare against
						#	before actuator motions.

# Linear Actuator Constants.
PIN_LA_IN   = "P8_10"		# Pin for Input PWM from RC Controller.
PIN_LA_ENA  = "P8_13"		# Pin for Output High Enable Signal.
PIN_LA_OUT1 = "P8_11"		# Pin for Output High/Low to Driver CH1.
PIN_LA_OUT2 = "P8_9"		# Pin for Output High/Low to Driver CH2.

LA_STROKE_MAX    = 2		# Maximum stroke length [inch].
LA_STROKE_TARGET = 1.5		# Target stroke length [inch].

# Carousel Stepper Constants.
PIN_CS_IN = "P8_20"			# Pin for Input PWM from RC Controller.
# TODO: Define Pins

# Shoulder Stepper Constants.
PIN_SS_IN = "P8_30"			# Pin for Input PWM from RC Controller.
# TODO: Define Pins

# Pressure Transducer Constants.
PIN_PT_IN = "P8_40"			# Pin for Input Data from Transducer.
# TODO: Define Pins

def main():
	"""Translates RC Controller Input to appropriate actuator signals.
	
	This function utilizes a set of initial variable values to setup
	desired functionality parameters (e.g. actuator stroke length), then 
	enters a polling loop to continually check the state of the input 
	signals. Upon proper conditions being met, changes in these inputs 
	cause the program to enter and iterate through one of three state 
	machines (one for each of the actuators on the SRS).
	
	Args:
		N/A
	
	Returns:
		N/A
	"""
	#
	# Initialize Pins.
	#
	GPIO.setup(PIN_LA_IN, GPIO.IN)
	GPIO.setup(PIN_LA_ENA, GPIO.OUT)
	GPIO.setup(PIN_LA_OUT1, GPIO.OUT)
	GPIO.setup(PIN_LA_OUT2, GPIO.OUT)
	
	GPIO.setup(PIN_CS_IN, GPIO.IN)
	
	GPIO.setup(PIN_SS_IN, GPIO.IN)
	# TODO: Continue with remaining Pins.
	
	#
	# Set Hardware to default States.
	#
	
	# Linear Actuator: Default to maximum extent.
	GPIO.output(PIN_LA_ENA, GPIO.HIGH)
	GPIO.output(PIN_LA_OUT1, GPIO.HIGH)
	GPIO.output(PIN_LA_OUT2, GPIO.LOW)
	
	# Carousel Stepper: Hold current position.
	# TODO
	
	# Shoulder Stepper: Hold current position.
	# TODO
	
	#
	# Initialize Variables.
	#
	
	# Pulse Width Averages.
	la_pwm_avg = 0.0
	cs_pwm_avg = 0.0
	ss_pwm_avg = 0.0
	
	# Position Command Histories.
	la_pos = 0
	la_pos_hist = deque(POS_HIST_NUM)
	
	cs_pos = 0
	cs_pos_hist = deque(POS_HIST_NUM)
	
	ss_pos = 0
	ss_pos_hist = deque(POS_HIST_NUM)
	
	#
	# Main program polling loop.
	#
	while True:
		#
		# Linear Actuator polling.
		#
		
		# Determine Average Pulse Width.
		la_pwm_avg = SRS.calc_pulse_width(
			PIN_LA_IN, PWM_AVG_NUM, PWM_WID_FREQ)
		
		# Add new Position Command to History.
		la_pos = SRS.set_position(
			la_pwm_avg,
			PWM_WID_FREQ, PWM_WID_MAX, PWM_WID_MIN, PWM_WID_TOL)
		la_pos_hist.append(la_pos)
		
		# Check for Position Change.
		SRS.move_linear(
			la_pos_hist, POS_HIST_NUM, PIN_LA_OUT1, PIN_LA_OUT2,
			(LA_STROKE_TARGET/LA_STROKE_MAX))
		
		#
		# Carousel Stepper polling.
		#
		
		# TODO
		
		#
		# Shoulder Stepper polling.
		#
		
		# TODO
		
		#
		# Pressure Transducer polling.
		#
		
		# TODO