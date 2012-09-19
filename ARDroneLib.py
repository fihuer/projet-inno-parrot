# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone2 Lib"
# version:
version = 1
# By Viq
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import os, time,threading,socket

###############
### GLOBALS ###
###############

COMMAND_PORT = 5556
DATA_PORT = 5554
VIDEO_PORT = 5555

###############
### CLASSES ###
###############

class ARDrone():
    "Classe qui gere un drone"
    def __init__(self, ip = "192.168.1.1"):
        self.ip = ip
        # Check drone availability
        if not _check_telnet(self.ip):
            raise StandardError, "Cannot connect to AR.Drone2"
        
        
        


###################
### DEFINITIONS ###
###################

def _check_telnet(self,IP):
    "Check if we can connect to telnet"
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket.connect((IP, 23))
    except:
        return False
    else:
        socket.close()
        return True
    
    
    

##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Viq (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
