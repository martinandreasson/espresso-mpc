#!/usr/bin/python

def rest_server(dummy,state):
  from bottle import route, run, get, post, request, static_file, abort
  from subprocess import call
  from datetime import datetime
  import set_time
  import config as conf
  import os

  basedir = os.path.dirname(__file__)
  wwwdir = basedir+'/www/'

  @route('/')
  def docroot():
    return static_file('index.html',wwwdir)

  @route('/<filepath:path>')
  def servfile(filepath):
    return static_file(filepath,wwwdir)

  @route('/curtemp')
  def curtemp():
    return str(state['temp'])

  @get('/settemp')
  def settemp():
    return str(state['settemp'])

  @get('/setsteamtemp')
  def setsteamtemp():
    return str(state['setsteamtemp'])

  @post('/settemp')
  def post_settemp():
    try:
      settemp = float(request.forms.get('settemp'))
      if settemp >= 10 and settemp <= 110 :
        state['settemp'] = settemp
        state['settemp_orig'] = settemp
        return str(settemp)
      else:
        abort(400,'Set temp out of range 10-110.')
    except:
      abort(400,'Invalid number for set temp.')

  @post('/setsteamtemp')
  def post_setsteamtemp():
    try:
      setsteamtemp = float(request.forms.get('setsteamtemp'))
      if setsteamtemp >= 110 and setsteamtemp <= 150 :
        state['setsteamtemp'] = setsteamtemp
        return str(setsteamtemp)
      else:
        abort(400,'Set temp out of range 110-150.')
    except:
      abort(400,'Invalid number for set temp.')

  @post('/getclienttime')
  def post_clienttime():
    try:
        clienttime = float(request.forms.get('getclienttime'))/1000
        ctv = datetime.fromtimestamp(clienttime)
        set_time.set_time((ctv.year, ctv.month, ctv.day, ctv.hour, ctv.minute, ctv.second, 0))
    except:
        abort(400,'Could not synchronize time')

  @post('/TimerOnMo')
  def post_TimerOnMo():
    TimerOnMo = request.forms.get('TimerOnMo')
    try:
      datetime.strptime(TimerOnMo,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOnMo'] = TimerOnMo
    return str(TimerOnMo)

  @post('/TimerOnTu')
  def post_TimerOnTu():
    TimerOnTu = request.forms.get('TimerOnTu')
    try:
      datetime.strptime(TimerOnTu,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOnTu'] = TimerOnTu
    return str(TimerOnTu)

  @post('/TimerOnWe')
  def post_TimerOnWe():
    TimerOnWe = request.forms.get('TimerOnWe')
    try:
      datetime.strptime(TimerOnWe,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOnWe'] = TimerOnWe
    return str(TimerOnWe)

  @post('/TimerOnTh')
  def post_TimerOnTh():
    TimerOnTh = request.forms.get('TimerOnTh')
    try:
      datetime.strptime(TimerOnTh,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOnTh'] = TimerOnTh
    return str(TimerOnTh)

  @post('/TimerOnFr')
  def post_TimerOnFr():
    TimerOnFr = request.forms.get('TimerOnFr')
    try:
      datetime.strptime(TimerOnFr,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOnFr'] = TimerOnFr
    return str(TimerOnFr)

  @post('/TimerOnSa')
  def post_TimerOnSa():
    TimerOnSa = request.forms.get('TimerOnSa')
    try:
      datetime.strptime(TimerOnSa,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOnSa'] = TimerOnSa
    return str(TimerOnSa)

  @post('/TimerOnSu')
  def post_TimerOnSu():
    TimerOnSu = request.forms.get('TimerOnSu')
    try:
      datetime.strptime(TimerOnSu,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOnSu'] = TimerOnSu
    return str(TimerOnSu)

  @post('/TimerOffMo')
  def post_TimerOffMo():
    TimerOffMo = request.forms.get('TimerOffMo')
    try:
      datetime.strptime(TimerOffMo,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOffMo'] = TimerOffMo
    return str(TimerOffMo)

  @post('/TimerOffTu')
  def post_TimerOffTu():
    TimerOffTu = request.forms.get('TimerOffTu')
    try:
      datetime.strptime(TimerOffTu,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOffTu'] = TimerOffTu
    return str(TimerOffTu)

  @post('/TimerOffWe')
  def post_TimerOffWe():
    TimerOffWe = request.forms.get('TimerOffWe')
    try:
      datetime.strptime(TimerOffWe,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOffWe'] = TimerOffWe
    return str(TimerOffWe)

  @post('/TimerOffTh')
  def post_TimerOffTh():
    TimerOffTh = request.forms.get('TimerOffTh')
    try:
      datetime.strptime(TimerOffTh,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOffTh'] = TimerOffTh
    return str(TimerOffTh)

  @post('/TimerOffFr')
  def post_TimerOffFr():
    TimerOffFr = request.forms.get('TimerOffFr')
    try:
      datetime.strptime(TimerOffFr,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOffFr'] = TimerOffFr
    return str(TimerOffFr)

  @post('/TimerOffSa')
  def post_TimerOffSa():
    TimerOffSa = request.forms.get('TimerOffSa')
    try:
      datetime.strptime(TimerOffSa,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOffSa'] = TimerOffSa
    return str(TimerOffSa)

  @post('/TimerOffSu')
  def post_TimerOffSu():
    TimerOffSu = request.forms.get('TimerOffSu')
    try:
      datetime.strptime(TimerOffSu,'%H:%M')
    except:
      abort(400,'Invalid time format.')
    state['TimerOffSu'] = TimerOffSu
    return str(TimerOffSu)

  @get('/allstats')
  def allstats():
    return dict(state)

  @route('/restart')
  def restart():
    call(["reboot"])
    return '';

  @route('/shutdown')
  def shutdown():
    call(["shutdown","-h","now"])
    return '';

  @get('/healthcheck')
  def healthcheck():
    return 'OK'

  run(host='0.0.0.0',port=conf.port,server='auto')
