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
        # Initialise the communication thread
        self.com_thread = _CommandThread(self.ip)
        self.com_thread.start()
    def stop(self):
        "Stop the AR.Drone"
        self.land()
        time.sleep(1)
        self.com_thread.stop()
    # Issuable command
    def takeoff(self):
        "Take Off"
        return self.com_thread.command("AT*REF=#ID#," + bin2dec("00010001010101000000001000000000") + "\r")
    def land(self):
        "Land"
        return self.com_thread.command("AT*REF=#ID#," + bin2dec("00010001010101000000000000000000") + "\r")
    def emergency(self):
        "Enter in emergency mode"
        return self.com_thread.command("AT*REF=#ID#," + bin2dec("00010001010101000000000100000000") + "\r")
        

class _CommandThread(threading.Thread):
    "Classe qui gere les commandes Parrot car on doit en envoyer souvent"
    def __init__(self,ip):
        "Create the Command Thread"
        self.running = True
        self.ip = ip
        self.counter = 1
        self.com = None
        self.port = COMMAND_PORT
        # Create the UDP Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.ip, self.port))
        
        threading.Thread.__init__(self)
        
    def run(self):
        "Send commands every 30ms"
        while self.running:
            com = self.com
            if com != None:
                com = com.replace("#ID#",str(self.counter))
                self.sock.send(self.com)
                self.counter += 1
            time.sleep(0.03)
    
    def stop(self):
        "Stop the communication"
        self.sock.close()
        self.running = False
        time.sleep(0.05)
        return True
    def command(self,command):
        "Send a command to the AR.Drone"
        self.com = command
        return True
        
        
        
        
        
        


###################
### DEFINITIONS ###
###################

def _check_telnet(IP):
    "Check if we can connect to telnet"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((IP, 23))
    except:
        return False
    else:
        socket.close()
        return True

def bin2dec(bin):
    return int(bin,2)
    
    
    
    

##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Viq (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
