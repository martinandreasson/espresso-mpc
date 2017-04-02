#!/usr/bin/python

def timer(state):
    
    from datetime import datetime

    now = datetime.now()
    weekday = now.weekday()
    now = now.replace(year = 1900, month = 1, day = 1)
    t_onMo = datetime.strptime(state['TimerOnMo'],'%H:%M')
    t_offMo = datetime.strptime(state['TimerOffMo'],'%H:%M')
    t_onTu = datetime.strptime(state['TimerOnTu'],'%H:%M')
    t_offTu = datetime.strptime(state['TimerOffTu'],'%H:%M')
    t_onWe = datetime.strptime(state['TimerOnWe'],'%H:%M')
    t_offWe = datetime.strptime(state['TimerOffWe'],'%H:%M')
    t_onTh = datetime.strptime(state['TimerOnTh'],'%H:%M')
    t_offTh = datetime.strptime(state['TimerOffTh'],'%H:%M')
    t_onFr = datetime.strptime(state['TimerOnFr'],'%H:%M')
    t_offFr = datetime.strptime(state['TimerOffFr'],'%H:%M')
    t_onSa = datetime.strptime(state['TimerOnSa'],'%H:%M')
    t_offSa = datetime.strptime(state['TimerOffSa'],'%H:%M')
    t_onSu = datetime.strptime(state['TimerOnSu'],'%H:%M')
    t_offSu = datetime.strptime(state['TimerOffSu'],'%H:%M')

    if t_onMo <= now and t_offMo >= now and weekday == 0:
        awake = True
    elif t_onTu <= now and t_offTu >= now and weekday == 1:
        awake = True
    elif t_onWe <= now and t_offWe >= now and weekday == 2:
        awake = True
    elif t_onTh <= now and t_offTh >= now and weekday == 3:
        awake = True
    elif t_onFr <= now and t_offFr >= now and weekday == 4:
        awake = True
    elif t_onSa <= now and t_offSa >= now and weekday == 5:
        awake = True
    elif t_onSu <= now and t_offSu >= now and weekday == 6:
        awake = True
    else:
        awake = False

    return awake
