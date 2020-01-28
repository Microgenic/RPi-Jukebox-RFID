#!/bin/bash
#
# see https://github.com/MiczFlor/RPi-Jukebox-RFID for details
# Especially the docs folder for documentation

# The absolute path to the folder which contains this script
PATHDATA="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

clear
echo "Backup files"


# Python scripts
# /home/pi/RPi-Jukebox-RFID/scripts/

sudo cp /home/pi/RPi-Jukebox-RFID/scripts/gpio-buttons.py $PATHDATA/gpio-buttons.py
sudo cp /home/pi/RPi-Jukebox-RFID/scripts/i2c_lcd_driver.py $PATHDATA/i2c_lcd_driver.py
sudo cp /home/pi/RPi-Jukebox-RFID/scripts/rfid_trigger_play.sh $PATHDATA/rfid_trigger_play.sh

# Services
# /etc/systemd/system/phoniebox-idle-watchdog.service
sudo cp /etc/systemd/system/phoniebox-i2c-lcd-display.service $PATHDATA/phoniebox-i2c-lcd-display.service

#Start- / Stop-Scripts
#
# /lib/systemd/system-shutdown/
sudo cp /lib/systemd/system-shutdown/shim-shutoff.sh $PATHDATA/shim-shutoff.sh