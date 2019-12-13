#!/bin/bash
#
# see https://github.com/MiczFlor/RPi-Jukebox-RFID for details
# Especially the docs folder for documentation

# The absolute path to the folder which contains this script
PATHDATA="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

clear
echo "##################################################### 
#    ___  __ ______  _  __________ ____   __  _  _  #
#   / _ \/ // / __ \/ |/ /  _/ __/(  _ \ /  \( \/ ) #
#  / ___/ _  / /_/ /    // // _/   ) _ ((  O ))  (  #
# /_/  /_//_/\____/_/|_/___/____/ (____/ \__/(_/\_) #
#                                                   #
##################################################### 

Welcome to the backup config script.

This script will backup Phoniebox configuration from
your Raspberry Pi.
Only the rfid card and playbackmode config will be backed up.
The music and folder structure must be backed up itself.

If you are ready, hit ENTER"
read INPUT


rfid_trigger_play.sh