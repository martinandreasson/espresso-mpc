#!/usr/bin/python

# Pin for relay connected to heating element
spi_port = 0
spi_dev = 0
he_pin = 26
brew_pin = 17
steam_pin = 14
thermometer_pin = 0

# MPC parameters
sample_time = 0.5
n = 25 # number of steps in MPC
c_1 = 0.015 # Temperature dynamics between reservoirs
c_2 = 1.0*1.04*10**(-11) # Temperature-depandent energy loss
c_u = 1.05*0.014 # Control static signal gain
a_1 = 1.3 # Adjust inverse heat capacity
T_s = 55 # Surrounding temperature
T_s_high = 55 # Surrounding temperature
K_I = 0.01
u_I_max = 4

# Defauld brew boost in % of max heating power
brew_boost = 40

# Observer gains
K_brew = 0.02
K_steam = 0.2

# Default parameters
settemp = 102
setsteamtemp = 145
TimerOnMo = '06:00'
TimerOffMo = '16:00'
TimerOnTu = '06:00'
TimerOffTu = '16:00'
TimerOnWe = '06:00'
TimerOffWe = '16:00'
TimerOnTh = '06:00'
TimerOffTh = '16:00'
TimerOnFr = '06:00'
TimerOffFr = '16:00'
TimerOnSa = '06:00'
TimerOffSa = '16:00'
TimerOnSu = '06:00'
TimerOffSu = '16:00'

# Web/REST Server Options
port = 80
