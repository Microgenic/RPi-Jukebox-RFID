#!/usr/bin/python
# -*- coding: latin-1 -*-

import i2c_lcd_driver
from time import sleep
from subprocess import check_output

LCD_WIDTH = 20   # Maximum characters per line
ADDRESS = 0x3f  # LCD Address
I2CBUS = 1  # i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)

fontdata1 = [
        # char(0) - Play
        [ 0b00000, 
          0b10000, 
          0b11000, 
          0b11100, 
          0b11110, 
          0b11100, 
          0b11000, 
          0b10000 ],

        # char(1) - Pause
        [ 0b00000, 
          0b11011, 
          0b11011, 
          0b11011, 
          0b11011, 
          0b11011, 
          0b11011, 
          0b11011 ]]

def GetMPC(command):
    process = check_output(command.split())
    return process
    
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])

def main():
    mylcd = i2c-lcd-driver.lcd(ADDRESS, I2CBUS)
    while True:
        mpcstatus = GetMPC("mpc status")
        playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
        file = GetMPC("mpc -f %file% current") # Get the current title
        if file.startswith("http"): # if it is a http stream!
            name = GetMPC("mpc -f %name% current")
            titel = GetMPC("mpc -f %title% current")           
            if len(name) > LCD_WIDTH:
                mylcd.lcd_display_string(name[0:LCD_WIDTH],1)
                mylcd.lcd_display_string(name[LCD_WIDTH:],2)
            else:
                mylcd.lcd_display_string(name,2)
            mylcd.lcd_display_string(titel,3)
            mylcd.lcd_display_string("",4)
        else: # if it is not a stream
            album = GetMPC("mpc -f %album% current"  )
            titel = GetMPC("mpc -f %title% current")
            track = GetMPC("mpc -f %track% current")
            time = GetMPC("mpc -f %time% current")
            artist = GetMPC("mpc -f %artist% current")
            mylcd.lcd_display_string(""+album,1) # Albumname
            mylcd.lcd_display_string(""+artist,2) # Artist
            mylcd.lcd_display_string(track+". "+titel,3) # Tracknummer. Titel
            mylcd.lcd_display_string("",4)

        if playing == "[playing]": # If it is currently playing
            mylcd.lcd_write(0xD5)
            mylcd.lcd_write_char(0)
        elif playing == "[paused]": # If is is paused
            mylcd.lcd_write(0xD5)
            mylcd.lcd_write_char(31)     
        else:
            mylcd.lcd_display_string("",1)
            mylcd.lcd_display_string("",3)
            mylcd.lcd_display_string(" %s" %time.strftime("%H:%M %d.%m.%Y"),4,2)
            mylcd.lcd_display_string(("READY - WIPE CARD!",2,1)
            sleep(0.5)
            mylcd.lcd_display_string(("",2)
            sleep(0.2)            
    
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