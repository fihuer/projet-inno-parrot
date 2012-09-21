# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone2 Lib"
# version:
version = 2
# By Viq
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import os, time,threading,socket,struct
import ARDroneNavdata

###############
### GLOBALS ###
###############

COMMAND_PORT = 5556
DATA_PORT = 5554
VIDEO_PORT = 5555
MAX_PACKET_SIZE = 1024*10
def nothing(arg1="",arg2=""):
    "Do nothing"
    pass

###############
### CLASSES ###
###############

class ARDrone():
    "Classe qui gere un drone"
    def __init__(self, ip = "192.168.1.1",data_callback=nothing):
        self.ip = ip
        # Check drone availability
        if not _check_telnet(self.ip):
            raise StandardError, "Cannot connect to AR.Drone2"
        # Initialise the communication thread
        self.com_thread = _CommandThread(self.ip)
        self.com_thread.start()
        self.c = self.com_thread.command # Alias
        # Initialize the navdata thread
        self.navthread = _NavdataThread(self.com_thread, data_callback)
        self.navthread.start()
        
    def stop(self):
        "Stop the AR.Drone"
        self.land()
        time.sleep(1)
        self.com_thread.stop()
        self.navthread.stop()
    # Issuable command
    ## Take Off/Land/Emergency
    def takeoff(self):
        "Take Off"
        return self.c("AT*REF=#ID#," + str(bin2dec("00010001010101000000001000000000")) + "\r")
    def land(self):
        "Land"
        return self.c("AT*REF=#ID#," + str(bin2dec("00010001010101000000000000000000")) + "\r")
    def emergency(self):
        "Enter in emergency mode"
        return self.c("AT*REF=#ID#," + str(bin2dec("00010001010101000000000100000000")) + "\r")
    def reset(self):
        "Reset the state of the drone"
        # Issue an emergency command
        self.emergency()
        time.sleep(0.5)
        # Then normal state
        return self.land()
    
    ## Calibrate sensors
    def calibrate(self):
        "Calibrate sensors"
        return self.c("AT*FTRIM=#ID#\r")

    ## Navigate
    def hover(self):
        "Make the drone stationary"
        return self.c("AT*PCMD=#ID#,0,0,0,0,0\r")
    def navigate(self, left_right=0, front_back=0, up_down=0, angle_change=0):
        "Command the drone, all the arguments are between -1 and 1"
        lr = float2dec(left_right)
        fb = float2dec(front_back)
        ud = float2dec(up_down)
        ac = float2dec(angle_change)
        return self.c("AT*PCMD=#ID#,1,"+str(lr)+","+str(fb)+","+str(ud)+","+str(ac)+"\r")
    def forward(self,speed=0.2):
        "Make the drone go forward, speed is between 0 and 1"
        return self.navigate(front_back=-speed)
    def backward(self,speed=0.2):
        "Make the drone go backward, speed is between 0 and 1"
        return self.navigate(front_back=speed)
    def left(self,speed=0.2):
        "Make the drone go left, speed is between 0 and 1"
        return self.navigate(left_right=-speed)
    def right(self,speed=0.2):
        "Make the drone go right, speed is between 0 and 1"
        return self.navigate(left_right=speed)
    def up(self,speed=0.2):
        "Make the drone rise in the air, speed is between 0 and 1"
        return self.navigate(up_down=speed)
    def down(self,speed=0.2):
        "Make the drone descend, speed is between 0 and 1"
        return self.navigate(up_down=-speed)
    def rotate_left(self,speed=0.8):
        "Make the drone turn left, speed is between 0 and 1"
        return self.navigate(angle_change=-speed)
    def rotate_right(self,speed=0.8):
        "Make the drone turn right, speed is between 0 and 1"
        return self.navigate(angle_change=speed)

    ## Special 

class _CommandThread(threading.Thread):
    "Classe qui gere les commandes Parrot car on doit en envoyer souvent"
    def __init__(self,ip):
        "Create the Command Thread"
        self.running = True
        self.ip = ip
        self.counter = 10
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
            self.sock.send("AT*COMWDG\r")
            if com != None:
                com = com.replace("#ID#",str(self.counter))
                self.sock.send(com)
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

class _NavdataThread(threading.Thread):
    "Manage the incoming data"
    def __init__(self, communication, callback):
        "Create the navdata handler thread"
        self.running = True
        self.port = DATA_PORT
        self.size = MAX_PACKET_SIZE
        self.com = communication
        self.ip = self.com.ip
        self.callback = callback
        self.f = ARDroneNavdata.navdata_decode
        # Initialize the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0',self.port))
        self.sock.setblocking(0)
        threading.Thread.__init__(self)

    def run(self):
        "Start the data handler"
        # Initialize the drone to send the data
        self.sock.sendto("\x01\x00\x00\x00", (self.ip,self.port))
        time.sleep(0.05)
        self.com.sock.send("""AT*CONFIG=1,"general:navdata_demo","TRUE"\r""")
        time.sleep(0.05)
        self.com.sock.send("AT*CTRL=2,0\r")
        while self.running:
            try:
                rep, client = self.sock.recvfrom(self.size)
            except socket.error:
                time.sleep(0.05)
            else:
                self.callback(self.f(rep))
        
    def stop(self):
        "Stop the communication"
        self.sock.close()
        self.running = False
        time.sleep(0.05)
        
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
        sock.close()
        return True

def bin2dec(bin):
    "Convert a binary number to an int"
    return int(bin,2)
def float2dec(my_float):
    "Convert a python float to an int"
    return int(struct.unpack("l",struct.pack("f",float(my_float)))[0])
    

    
    

##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Viq (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    print "> This is a library only, please use the test instead"
