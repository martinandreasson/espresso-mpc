#!/usr/bin/python

def he_control_loop(dummy, state):

  from time import sleep
  from datetime import datetime, timedelta
  import RPi.GPIO as GPIO

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(conf.he_pin, GPIO.OUT)
  GPIO.output(conf.he_pin,0)

  try:
    while True:
      control_signal = state['control_signal']
      # PWM to control heating element
      if control_signal >= 100:
        GPIO.output(conf.he_pin,1)
        sleep(conf.sample_time)
      elif control_signal > 0 and control_signal < 100:
        GPIO.output(conf.he_pin,1)
        sleep(conf.sample_time*control_signal/100.)
        GPIO.output(conf.he_pin,0)
        sleep(conf.sample_time*(1-(control_signal/100.)))
      else:
        GPIO.output(conf.he_pin,0)
        sleep(conf.sample_time)

  finally:
    GPIO.output(conf.he_pin,0)
    GPIO.cleanup()

def control_loop(dummy,state):

  import sys
  import pickle
  from time import sleep, time, ctime
  import math
  import RPi.GPIO as GPIO
  import config as conf
  import numpy
  from cvxopt import matrix
  from cvxopt import solvers
  import mpc_matrices
  import timer
  import Adafruit_GPIO.SPI as SPI
  import Adafruit_MAX31855.MAX31855 as MAX31855
  sensor = MAX31855.MAX31855(spi=SPI.SpiDev(conf.spi_port, conf.spi_dev))

  lasttime = time()
  lastsettemp = state['settemp']
  setsteamtemp = state['setsteamtemp']
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(conf.brew_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(conf.steam_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  brew_state_prev = GPIO.input(conf.brew_pin)
  steam_state_prev = GPIO.input(conf.steam_pin)
  mpc_mat_brew = mpc_matrices.mpc_matrices(lastsettemp, conf.T_s)
  mpc_mat_steam = mpc_matrices.mpc_matrices(setsteamtemp, conf.T_s)
  mpc_mat = mpc_mat_brew
  A = mpc_mat['A']
  B = mpc_mat['B']
  B2 = mpc_mat['B2']
  u = 0 # Control signal
  u_I = 0 # Integral control
  n = conf.n
  dt = conf.sample_time
  tempc = sensor.readTempC()
  tempc_prev = tempc
  y = tempc - lastsettemp
  x = numpy.mat([[y + 3.3], [y]]) # current state
  x_prev = numpy.mat([[y + 3.3], [y]]) # previous state

  try:
    while True:
      settemp = state['settemp']
      tempc = sensor.readTempC()
      if math.isnan(tempc):
          tempc = tempc_prev
      if abs(tempc - tempc_prev) > 100:
           tempc = tempc_prev
      tempc_prev = tempc

      # If steam button pressed, change setpoint temperature and observer gain
      steam_state = GPIO.input(conf.steam_pin)
      if steam_state:
     	 state['settemp'] = state['settemp_orig']
         K = conf.K_brew
         mpc_mat = mpc_mat_brew
      else:
         state['settemp'] = state['setsteamtemp']
         K = conf.K_steam
         mpc_mat = mpc_mat_steam

      if steam_state != steam_state_prev:
          A = mpc_mat['A']
          B = mpc_mat['B']
          B2 = mpc_mat['B2']
          steam_state_prev = steam_state

      if state['settemp'] != lastsettemp :
          # Change state instantaneously (by-pass filter)
          settemp = state['settemp']
          x = x - numpy.mat([[settemp], [settemp]]) + numpy.mat([[lastsettemp], [lastsettemp]])
          x_prev = x
          lastsettemp = state['settemp']

      if settemp > 125:
          T_s = conf.T_s_high
      else:
          T_s = conf.T_s
      y = tempc - settemp

      # Observer
      y_tilde = x_prev.item(1,0)

      # If brewing, add feed forward control and change observer
      brew_state = GPIO.input(conf.brew_pin)

      if brew_state: # Not brewing
          x = A*x_prev + B*u + B2 + K*conf.sample_time*(y - y_tilde)*numpy.mat('1; 1')
          d_1vec = numpy.zeros((n,1))
      else: # Brewing
          x = A*x_prev + B*(u - conf.brew_boost) + B2 + K*conf.sample_time*(y - y_tilde)*numpy.mat('1; 1')
          d_1vec = -numpy.ones((n,1))*conf.brew_boost

      x_prev = x
      # Check if timer is on
      awake = timer.timer(state)
      if awake:
          # Equality constraint
          if brew_state:
              b_constr = mpc_mat['A_app']*x + mpc_mat['b_constr']
          else:
              b_constr = mpc_mat['A_app']*x + mpc_mat['b_constr_brew']
          b_opt = matrix(b_constr, tc='d')

          # Invoke solver
          solvers.options['show_progress'] = False
          sol = solvers.lp(mpc_mat['q_opt'], mpc_mat['G_opt'], mpc_mat['h_opt'], mpc_mat['A_opt'], b_opt, solver='cvxopt')
          x_opt = numpy.array(sol['x'])
          u_mpc = x_opt[2*n,0] # Only use first control signal

          # Integral control, only if not steaming
          if steam_state:
              u_I = u_I - dt*conf.K_I*x.item(1,0)
              if u_I > conf.u_I_max:
                  u_I = conf.u_I_max
              elif u_I < -conf.u_I_max:
                  u_I = -conf.u_I_max

          if steam_state:
              u = u_mpc + u_I
          else:
              u = u_mpc

          if u < 0:
              u = 0
          elif u > 100:
              u = 100

      else:
          u = 0

      state['awake'] = awake
      state['tempc'] = round(x.item(1,0) + settemp,2)
      state['control_signal'] = round(u,2)

      time1 = time()
      time2 = math.ceil(time1)%60

      if time2 == 0:
          with open('/root/espresso-mpc/objs.pickle', 'wb') as fw:
              pickle.dump([state['settemp'], state['settemp_orig'], state['setsteamtemp'], state['TimerOnMo'], state['TimerOffMo'], state['TimerOnTu'], state['TimerOffTu'], state['TimerOnWe'], state['TimerOffWe'], state['TimerOnTh'], state['TimerOffTh'], state['TimerOnFr'], state['TimerOffFr'], state['TimerOnSa'], state['TimerOffSa'], state['TimerOnSu'], state['TimerOffSu']],fw)

      exec_time = time1 - lasttime

      print 'Exec. time:', str(exec_time), 'Temperature:', state['tempc'], 'Control signal:', state['control_signal'], 'Integral control:', round(u_I, 2), 'Awake:', str(awake), 'Temp. setpoint:', str(settemp), 'y:', str(round(x.item(1,0),2))

      sleeptime = lasttime + conf.sample_time - time()
      if sleeptime < 0 :
        sleeptime = 0
      sleep(sleeptime)
      lasttime = time()

  finally:
    GPIO.cleanup()

if __name__ == '__main__':

  from multiprocessing import Process, Manager
  from time import sleep
  from urllib2 import urlopen
  import config as conf
  import pickle
  import rest_server as rest_server

  manager = Manager()
  state = manager.dict()
  state['control_signal'] = 0
  state['awake'] = False

  # Read states
  try:
      with open('/root/espresso-mpc/objs.pickle') as fr:
          [state['settemp'], state['settemp_orig'], state['setsteamtemp'], state['TimerOnMo'], state['TimerOffMo'], state['TimerOnTu'], state['TimerOffTu'], state['TimerOnWe'], state['TimerOffWe'], state['TimerOnTh'], state['TimerOffTh'], state['TimerOnFr'], state['TimerOffFr'], state['TimerOnSa'], state['TimerOffSa'], state['TimerOnSu'], state['TimerOffSu']] = pickle.load(fr)
  except:
      state['settemp'] = conf.settemp
      state['settemp_orig'] = conf.settemp
      state['setsteamtemp'] = conf.setsteamtemp
      state['TimerOnMo'] = conf.TimerOnMo
      state['TimerOffMo'] = conf.TimerOffMo
      state['TimerOnTu'] = conf.TimerOnTu
      state['TimerOffTu'] = conf.TimerOffTu
      state['TimerOnWe'] = conf.TimerOnWe
      state['TimerOffWe'] = conf.TimerOffWe
      state['TimerOnTh'] = conf.TimerOnTh
      state['TimerOffTh'] = conf.TimerOffTh
      state['TimerOnFr'] = conf.TimerOnFr
      state['TimerOffFr'] = conf.TimerOffFr
      state['TimerOnSa'] = conf.TimerOnSa
      state['TimerOffSa'] = conf.TimerOffSa
      state['TimerOnSu'] = conf.TimerOnSu
      state['TimerOffSu'] = conf.TimerOffSu

  p = Process(target=control_loop,args=(1,state))
  p.daemon = True
  p.start()

  h = Process(target=he_control_loop,args=(1,state))
  h.daemon = True
  h.start()

  r = Process(target=rest_server.rest_server,args=(1,state))
  r.daemon = True
  r.start()

  while p.is_alive() and h.is_alive() and r.is_alive():
    sleep(0.1)
