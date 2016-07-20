#!/usr/bin/python
"""This is a Python Hal driver for the huanyang VFD over rs485/modbus"""
import hal
import time

import huanyang485


h = hal.component("huanyangvfd")
h.newpin("spindle_on", hal.HAL_BIT, hal.HAL_IN)
h.newpin("freq_cmd", hal.HAL_U32, hal.HAL_IN)
h.newpin("spindle_rev", hal.HAL_BIT, hal.HAL_IN)
h.newpin("spindle_forward", hal.HAL_BIT, hal.HAL_IN)
h.ready()

d = huanyang485.Huanyang_rs485(device='/dev/ttyUSB0')

spindle_on = False
frequency = 0
direction = False

try:
    while 1:
        time.sleep(1)
        if h['spindle_on'] != spindle_on:
          spindle_on = h['spindle_on']
          if spindle_on:
            d.StartSpindel()
          else:
            d.StopSpindel()
        if h['freq_cmd'] != frequency:
          frequency = h['freq_cmd']
          d.SetFrequency(frequency)
        if h['spindle_rev'] == 1 and direction != -1:
          direction = -1
          d.Reverse()
        if h['spindle_forward'] == 1 and direction != 1:
          direction = 1
          d.Forward()

except KeyboardInterrupt:
    raise SystemExit
