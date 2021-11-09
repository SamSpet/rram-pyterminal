from Lib import CommandMap as CM

VoltDict = {'3V3'      : b'\x41'.decode('utf-8'), 
            'AVDD_WR'  : b'\x42'.decode('utf-8'),
            'AVDD_WL'  : b'\x43'.decode('utf-8'),
            'AVDD_RRAM': b'\x44'.decode('utf-8'),
            'VDD'      : b'\x45'.decode('utf-8'),
            'AVDD_SRAM': b'\x46'.decode('utf-8')}
            

def list_sources(pyterminal):
    print('-------------------------------------')
    print('| Output Name | Status | Value (mV) |')
    print('-------------------------------------')
    for key, value in VoltDict.items():
        response = pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_GET + ' ' + value, False)
        output_status = 'On' if response.split()[0] == '1' else 'Off'
        output_value = 'Analog' if response.split()[1] == '-1' else response.split()[1]
        print(f'| {key:>11} | {output_status:>6} | {output_value:>10} |')
    print('-------------------------------------')


def clear(pyterminal, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_CLEAR, verbal)


def status(pyterminal, verbal):
    return pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_STATUS, verbal)


def save(pyterminal, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_SAVE, verbal)
    

def load(pyterminal, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_LOAD, verbal)
    

def allon(pyterminal, verbal):
    for k, v in VoltDict.items():
        pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_ENABLE + ' ' + v, verbal)
        

def alloff(pyterminal, verbal):
    for k, v in VoltDict.items():
        pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_DISABLE + ' ' + v, verbal)
    

def reset(pyterminal, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_RESET, verbal)
    

def enable(pyterminal, target, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_ENABLE + ' ' + VoltDict[target], verbal)
    

def disable(pyterminal, target, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_DISABLE + ' ' + VoltDict[target], verbal)
    

def increment(pyterminal, target, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_INCR + ' ' + VoltDict[target], verbal)
    

def decrement(pyterminal, target, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_DECR + ' ' + VoltDict[target], verbal)
    

def plus(pyterminal, value, target, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_PLUS + ' ' + value + ' ' + VoltDict[target], verbal)
    

def minus(pyterminal, value, target, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_MINUS + ' ' + value + ' ' + VoltDict[target], verbal)
    

def set_source(pyterminal, value, target, verbal):
    pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_SET + ' ' + value + ' ' + VoltDict[target], verbal)
    

def get_source(pyterminal, target, verbal):
    return pyterminal.send_command(CM.CM_PM + ' ' + CM.CM_PM_GET + ' ' + VoltDict[target], verbal).split()


def unknown(parameters):
    print('Unknown Command: ' + ' '.join(parameters) + '(From PyTerminal)')
        

def decode(pyterminal, parameters):
    if   parameters[1] == 'list'   : list_sources(pyterminal)
    elif parameters[1] == 'clear'  : clear       (pyterminal,                               True)
    elif parameters[1] == 'status' : status      (pyterminal,                               True)
    elif parameters[1] == 'save'   : save        (pyterminal,                               True)
    elif parameters[1] == 'load'   : load        (pyterminal,                               True)
    elif parameters[1] == 'allon'  : allon       (pyterminal,                               True)
    elif parameters[1] == 'alloff' : alloff      (pyterminal,                               True)
    elif parameters[1] == 'reset'  : reset       (pyterminal,                               True)
    elif parameters[1] == 'enable' : enable      (pyterminal, parameters[2],                True)
    elif parameters[1] == 'disable': disable     (pyterminal, parameters[2],                True)
    elif parameters[1] == '++'     : increment   (pyterminal, parameters[2],                True)
    elif parameters[1] == '--'     : decrement   (pyterminal, parameters[2],                True)
    elif parameters[1] == '+'      : plus        (pyterminal, parameters[2], parameters[3], True)
    elif parameters[1] == '-'      : minus       (pyterminal, parameters[2], parameters[3], True)
    elif parameters[1] == 'set'    : set_source  (pyterminal, parameters[2], parameters[3], True)
    elif parameters[1] == 'get'    : get_source  (pyterminal, parameters[2],                True)
    else: unknown(parameters)
    