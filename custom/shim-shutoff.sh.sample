#!/bin/sh
#
# OnOff SHIM exposed by cyperghost for retropie.org.uk
# This is mandatory for proper SHIM shutdown!
# GPIO 4 (Pin 7) is uesd as default to cut off power
# GPIO 17 (Pin 11) is used as default to send off command to PI AND to let the LED blink 3 times during shutdown/ halt (only if 3.3V is connected)
# We use a modified version of gpio-buttons.py to shutdown pi with GPIO

# GPIO to cut off power!    
poweroff_pin="4"    

# GPIO to see shuting down on SHIM LED.
led_pin="17"    
    
if [ "$1" = "poweroff" ]; then    
    
    /bin/echo $led_pin > /sys/class/gpio/export    
    /bin/echo out > /sys/class/gpio/gpio$led_pin/direction    
		
		# Blink LED 3 times
        for iteration in 1 2 3; do    
            /bin/echo 0 > /sys/class/gpio/gpio$led_pin/value    
            /bin/sleep 0.2    
            /bin/echo 1 > /sys/class/gpio/gpio$led_pin/value    
            /bin/sleep 0.2    
       done    
    
    /bin/echo $poweroff_pin > /sys/class/gpio/export    
    /bin/echo out > /sys/class/gpio/gpio$poweroff_pin/direction    
    /bin/echo 0 > /sys/class/gpio/gpio$poweroff_pin/value
fi
if [ "$1" = "halt" ]; then    
    
    /bin/echo $led_pin > /sys/class/gpio/export    
    /bin/echo out > /sys/class/gpio/gpio$led_pin/direction    
    
        for iteration in 1 2 3; do    
            /bin/echo 0 > /sys/class/gpio/gpio$led_pin/value    
            /bin/sleep 0.2    
            /bin/echo 1 > /sys/class/gpio/gpio$led_pin/value    
            /bin/sleep 0.2    
       done    
    
    /bin/echo $poweroff_pin > /sys/class/gpio/export    
    /bin/echo out > /sys/class/gpio/gpio$poweroff_pin/direction    
    /bin/echo 0 > /sys/class/gpio/gpio$poweroff_pin/value
fi