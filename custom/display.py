#!/usr/bin/python
# -*- coding: utf-8 -*-

import ptvsd
ptvsd.enable_attach()

#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_i2c.py
#  LCD test script using I2C backpack.
#  Supports 16x2 and 20x4 screens.
#
# Author : Matt Hawkins
# Date   : 20/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------
import smbus
import time
from datetime import date
import atexit

# Define some device parameters
I2C_ADDR  = 0x3f # I2C device address
LCD_WIDTH = 20   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

lastMSG = []
lastMSG.append("nix")
lastMSG.append("nix")
lastMSG.append("nix")
lastMSG.append("nix")
lastMSG.append("nix")

lstMSGi = []
lstMSGi.append(1)
lstMSGi.append(1)
lstMSGi.append(1)
lstMSGi.append(1)
lstMSGi.append(1)


# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  # If a message is longer than LCD_WIDTH (20) it will be cutted and then moves
  message = message.replace("\n"," ")
  
  if line == 0x80:
    li = 1
  if line == 0xC0:
    li = 2
  if line == 0x94:
    li = 3
  if line == 0xD4:
    li = 4
  global lastMSG
  global lstMSGi
  lcd_byte(line, LCD_CMD)
  if lastMSG[li] == message:
    if len(message) > LCD_WIDTH:
      for i in range(LCD_WIDTH):
        i2 = i + lstMSGi[li]
        lcd_byte(ord(message[i2]),LCD_CHR)
      test = lstMSGi[li] + LCD_WIDTH
      if test < len(message):
        lstMSGi[li] += 1
      else:
        lstMSGi[li] = 0
    else:
      message = message.ljust(LCD_WIDTH," ")
      for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)
  else:
    lastMSG[li] = message
    lstMSGi[li] = 0

		
		
def GetMPC(command):
    from subprocess import check_output
    process = check_output(command.split())
    return str(process, 'utf-8') # required for python3

def exit_handler():
    global LCD_BACKLIGHT
    LCD_BACKLIGHT = 0x00  # Off
    lcd_byte(0x01, LCD_CMD)

def main():
  try:
    # Main program block

    # Initialise display
    lcd_init()
    while True:
      try:
        mpcstatus = GetMPC("mpc status")
        playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
        file = GetMPC("mpc -f %file% current") # Get the current title
        if playing == "[playing]": # If it is currently playing
          if file.startswith("http"): # if it is a http stream!
            name = GetMPC("mpc -f %name% current")
            titel = GetMPC("mpc -f %title% current")
            if len(name) > LCD_WIDTH:
              lcd_string(name[0:LCD_WIDTH],LCD_LINE_1)
              lcd_string(name[LCD_WIDTH:],LCD_LINE_2)
            else:
              lcd_string(name,LCD_LINE_1)
              lcd_string(" ",LCD_LINE_2)
            lcd_string(titel,LCD_LINE_3)
            lcd_string("Playing",LCD_LINE_4)
          else: # if it is not a stream
            album = GetMPC("mpc -f %album% current"  )
            titel = GetMPC("mpc -f %title% current")
            track = GetMPC("mpc -f %track% current")
            time = GetMPC("mpc -f %time% current")
            artist = GetMPC("mpc -f %artist% current")
            lcd_string(""+titel,LCD_LINE_1)
            lcd_string(""+artist,LCD_LINE_2)
            lcd_string(""+album,LCD_LINE_3)
            lcd_string("Playing Track "+track,LCD_LINE_4)
        elif playing == "[paused]": # If is is paused
          if file.startswith("http"): # stream
            name = GetMPC("mpc -f %name% current")
            titel = GetMPC("mpc -f %title% current")
            if len(name) > LCD_WIDTH:
              lcd_string(name[0:LCD_WIDTH],LCD_LINE_1)
              lcd_string(name[LCD_WIDTH:],LCD_LINE_2)
            else:
              lcd_string(name,LCD_LINE_1)
            lcd_string(titel,LCD_LINE_3)
            lcd_string("Paused",LCD_LINE_4)
          else: #Not stream
            album = GetMPC("mpc -f %album% current")
            titel = GetMPC("mpc -f %title% current")
            track = GetMPC("mpc -f %track% current")
            time = GetMPC("mpc -f %time% current")
            artist = GetMPC("mpc -f %artist% current")
            lcd_string(""+titel,LCD_LINE_1)
            lcd_string(""+artist,LCD_LINE_2)
            lcd_string(""+album,LCD_LINE_3)
            lcd_string("Paused Track "+track,LCD_LINE_4)
        else:
          lcd_string("Hallo Kinder,",LCD_LINE_1)
          lcd_string("PhonieBox bereit! ",LCD_LINE_2)
          lcd_string(" ",LCD_LINE_3)
          lcd_string(date.today().strftime("%A %d. %B"),LCD_LINE_4)
      except:
        lcd_string("Hallo Kinder,",LCD_LINE_1)
        lcd_string("Phoniebox Zickt. ",LCD_LINE_2)
        lcd_string("Papa macht das schon",LCD_LINE_3)
        lcd_string("",LCD_LINE_4)
        pass
    time.sleep(10)
  except:
    LCD_BACKLIGHT = 0x00  # Off
    lcd_byte(0x01, LCD_CMD)
  finally:
    LCD_BACKLIGHT = 0x00  # Off
    lcd_byte(0x01, LCD_CMD)


atexit.register(exit_handler)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    LCD_BACKLIGHT = 0x00  # Off
    lcd_byte(0x01, LCD_CMD)
    pass
  finally:
    LCD_BACKLIGHT = 0x00  # Off
    lcd_byte(0x01, LCD_CMD)

	
