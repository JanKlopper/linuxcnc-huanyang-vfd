machinekit-huanyang-vfd
=====================

A user space component for controlling a huanyang spindle inverter with machienkit.

The component was developed by S. Alford and published at http://www.cnczone.com/forums/phase-converters/91847-huanyang-vfd-rs485-modbus-3.html#post704008http://www.cnczone.com/forums/phase-converters/91847-huanyang-vfd-rs485-modbus-3.html#post704008
Some changes were contributed to fix problems with the rebranding of emc2 to linuxcnc.
These were contributed by alan_3301, also on the forum.

Others included some minor bugfixes in the code.

This is the python rewrite of the same code in C, negating the need for compiling the component on the target platform (a beaglebone black in our case), which removes the need for various machinekit sources files.

The software is released under GPL V2
