#!/usr/bin/python
"""This is a Python Hal driver for the huanyang VFD over rs485/modbus"""
import hal
import time

import huanyang485


h = hal.component("huanyangvfd")
h.newpin("spindle_on", hal.HAL_BIT, hal.HAL_IN)
h.newpin("freq_cmd", hal.HAL_U32, hal.HAL_IN)
h.newpin("speed", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("spindle_rev", hal.HAL_BIT, hal.HAL_IN)
h.newpin("spindle_fwd", hal.HAL_BIT, hal.HAL_IN)

h.newpin("OutA", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("OutF", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("DCV", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("ACV", hal.HAL_FLOAT, hal.HAL_IN)

h.newpin("Rott", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("modbus-ok", hal.HAL_BIT, hal.HAL_IN)
h.newpin("base-freq", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("max-freq", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("freq-lower-limit", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("rated-motor-voltage", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("rated-motor-current", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("rated-motor-rev", hal.HAL_FLOAT, hal.HAL_IN)


#h.newpin("spindle_rev", hal.HAL_BIT, hal.HAL_IN)

h.ready()

d = huanyang485.Huanyang_rs485(device='/dev/ttyUSB0')
d.ReadSetup()

h['base-freq'] = d.base_frequency
h['max-freq'] = d.max_frequency
h['freq-lower-limit'] = d.min_frequency     
h['rated-motor-voltage'] = d.rated_motor_voltage
h['rated-motor-current'] = d.rated_motor_current
#h['motor_poles'] = d.motor_poles
h['rated-motor-rev'] = d.rated_motor_rpm
spindle_on = False
frequency = 0
logfile = open('/home/machinekit/log.txt', 'a')

try:
    while 1:
        time.sleep(1)
        if h['spindle_on'] != spindle_on:
          spindle_on = h['spindle_on']
          if spindle_on:
            logfile.write('Start Spindle\n')
            d.StartSpindel()
          else:
            logfile.write('Stop Spindle\n')
            d.StopSpindel()
        if float(h['speed'])/7.2  != frequency:
          logfile.write('new speed: %r\n' % h['speed'])
          frequency = int(h['speed']/7.2)
          
          h['freq_cmd'] = frequency
          logfile.write('new frequency: %r\n' % frequency)
          d.SetFrequency(frequency)

        if h['freq_cmd'] != frequency:
          frequency = h['freq_cmd']
          logfile.write('new frequency: %r\n' % frequency)
          d.SetFrequency(frequency)
        
        h['OutA']  = d.GetStatus(huanyang485.STATUS_OutA)
        h['OutF']  = d.GetStatus(huanyang485.STATUS_OutF)        
        h['Rott']  = d.GetStatus(huanyang485.STATUS_RoTT)
        h['DCV']  = d.GetStatus(huanyang485.STATUS_DCV)
        h['ACV']  = d.GetStatus(huanyang485.STATUS_ACV)                
        h['modbus-ok'] = d.modbus_ok

except KeyboardInterrupt:
    raise SystemExit
