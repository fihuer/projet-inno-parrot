# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone Lib"
# version:
version = 4
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import os, time,threading,socket,struct, random
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

class Drone():
    "Classe qui gere un drone"
    def __init__(self, ip = "192.168.1.1",data_callback=nothing):
        self.ip = ip
        # Check drone availability
        if not _check_telnet(self.ip):
            raise IOError, "Cannot connect to AR.Drone 2"
        # Initialise the communication thread
        self.comThread = _CommandThread(ip)
        self.comThread.start()
        self.c = self.comThread.command # Alias
        # Initialize the navdata thread
        self.navThread = _NavdataThread(self.comThread, data_callback)
        self.navThread.start()
        
    def stop(self):
        "Stop the AR.Drone"
        self.land()
        time.sleep(1)
        self.comThread.stop()
        self.navThread.stop()
    def change_callback(self, new_callback):
        "Change the callback function"
        # Check if the argument is a function
        if not hasattr(new_callback, '__call__'):   raise TypeError("Need a function")
        return self.navThread.change_callback(new_callback)

    # Special config
    def configure(self, argument, value):
        "Set a configuration onto the drone"
        return self.comThread.configure(argument,value)
    def continuous_config(self, argument,value):
        "Set a configuration onto the drone which will be sent frenquently"
        return self.comThread.continuous_config(argument,value)
        
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
        # Release all lock to be sure command is issued
        return self.c("AT*REF=#ID#," + str(bin2dec("00010001010101000000000100000000")) + "\r")
    def reset(self):
        "Reset the state of the drone"
        # Issue an emergency command
        self.emergency()
        time.sleep(0.5)
        # Then normal state
        return self.land()
    
    ## Calibrate
    def start_navdata(self):
        "Start reception of navdata"
        return self.configure("general:navdata_demo","FALSE")
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
    def __init__(self, ip = "192.168.1.1", port = COMMAND_PORT):
        "Create the Command Thread"
        self.running = True
        self.ip = ip
        self.port = port        
        self.counter = 10 # Counter to issue AT command in order
        self.continous_config = None # If not set to None, will issue this command each time instead of command
        self.com = None # Last command to issue
        self.socket_lock = threading.Lock() # Create the lock for the socket
        self.__ack = False
        # Create the UDP Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.ip, self.port))
        
        # Create random ids
        self.session_id =   "".join(random.sample("0123456789abcdef",8))
        self.profile_id =   "".join(random.sample("0123456789abcdef",8))
        self.app_id =       "".join(random.sample("0123456789abcdef",8))
        self.is_configurated = False
        threading.Thread.__init__(self)
        
    # Usable commands
    def command(self,command):
        "Send a command to the AR.Drone"
        self.continous_config = None
        self.com = command
        return True
    def continuous_config(self, argument,value):
        "Set a configuration onto the drone which will be sent frenquently"
        self.com = None
        self.continous_config = (argument,value)
        return True

    def configure(self, argument, value):
        "Set a configuration onto the drone"
        # Check if it's the first time we send a config
        if not self.is_configurated:
            # Activate the config
            self.is_configurated = True
            self.configure("custom:session_id",self.session_id)
            self.configure("custom:profile_id",self.profile_id)
            self.configure("custom:application_id",self.app_id)
        self.socket_lock.acquire()
        tries = 0
        while tries <= 3:
            to_send = "AT*CONFIG_IDS="+str(self.counter) + ',"' + self.session_id + '","' + self.profile_id + '","' + self.app_id + '"\r'
            self.sock.send(to_send)
            time.sleep(0.05)
            to_send = "AT*CONFIG="+str(self.counter+1)+',"' + str(argument) + '","' + str(value) + '"\r'
            #print to_send # Printing the AT*CONFIG we are sending
            self.sock.send(to_send)
            self.counter = self.counter + 2
            # Check if we receive acknowledgement
            time.sleep(0.05)
            if self.__ack:
                self.__ack = False
                break
            tries += 1
        self.sock.send("AT*CTRL="+str(self.counter)+",5,0")
        self.counter = self.counter + 1
        self.socket_lock.release()
        if tries < 4:
            return True
        else:
            return False
    # Internal functions
    def _ack_command(self):
        "Call this function when the command is acknoledge"
        self.__ack = True
        return True
    
    def run(self):
        "Send commands every 30ms"
        while self.running:
            com = self.com
            conf = self.continous_config
            self.socket_lock.acquire() # Ask for the permission to send msg
            self.sock.send("AT*COMWDG\r")
            if com != None:
                com = com.replace("#ID#",str(self.counter))
                self.sock.send(com)
                self.counter += 1
            if conf != None:
                self.socket_lock.release()
                self.configure(conf[0],conf[1])
                self.socket_lock.acquire()
            self.socket_lock.release()
            time.sleep(0.03)
        self.sock.close()
    
    def stop(self):
        "Stop the communication"
        self.running = False
        time.sleep(0.05)
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
        self.last_drone_status = None
        # Initialize the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0',self.port))
        self.sock.setblocking(0)
        threading.Thread.__init__(self)
    def change_callback(self, new_callback):
        "Change the callback function"
        # Check if the argument is a function
        if not hasattr(new_callback, '__call__'):   return False
        self.callback = new_callback
        return True

    def run(self):
        "Start the data handler"
        # Initialize the drone to send the data
        self.sock.sendto("\x01\x00\x00\x00", (self.ip,self.port))
        time.sleep(0.05)
        #self.com.sock.send("""AT*CONFIG=1,"general:navdata_demo","TRUE"\r""")
        #time.sleep(0.05)
        #self.com.sock.send("AT*CTRL=2,0\r")
        while self.running:
            try:
                rep, client = self.sock.recvfrom(self.size)
            except socket.error:
                time.sleep(0.05)
            else:
                rep = self.f(rep)
                self.last_navdata = rep
                if rep["drone_state"]['command_ack'] == 1:
                    self.com._ack_command()
                self.callback(rep)
        self.sock.close()
        
    def stop(self):
        "Stop the communication"
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
    return int(struct.unpack("=l",struct.pack("f",float(my_float)))[0])
    

    
    

##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    print "> This is a library only, please use the test instead"
