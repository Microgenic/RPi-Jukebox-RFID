#"C:\Program Files (x86)\Arduino\hardware\tools\avr/bin/avrdude.exe"

#-C"C:\Program Files (x86)\Arduino\hardware\tools\avr/etc/avrdude.conf" -v -patmega328p -carduino -PCOM3 -b115200 -D -Uflash:w:"$(ProjectDir)Debug\$(TargetName).hex":i 


from subprocess import check_output

def GetMPC(command):
    process = check_output(command.split())
    return process
	
def main():
	mpcstatus = GetMPC("mpc status")
	print(type(mpcstatus))
	#playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
	#file = GetMPC("mpc -f %file% current") # Get the current title

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
    pass
	finally: