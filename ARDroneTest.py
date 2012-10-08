# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone Test"
# version:
version = 3
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import time, sys, os
import ARDroneLib, ARDroneGUI, ARDroneConfig

###############
### GLOBALS ###
###############

gui = None
last_coord=(None,None)
all_coords = dict()

###############
### CLASSES ###
###############

class Log():
    "Log data to file"
    def __init__(self, filename):
        "Open the file to log data"
        self.f = open(filename,"w")
        self.data = dict()
    def close(self):
        "Close the file"
        # Write data to csv
        nb_lines = 0
        for value in self.data.values():
            if len(value) > nb_lines:   nb_lines = len(value)
        for i in range(nb_lines):
            pass # ToDo
        # Then close
        self.f.close()
        return True
    def __del__(self):
        "Called when the object is destroyed to close the file"
        self.close()
    def log(self, dataname, data):
        "Log data into file"
        if not dataname in self.data: # If there is no key dataname in the db, create it
            self.data = [str(dataname)]
        self.data[dataname].append(data)
        return True

class GPS_Coord():
    "Very little class to store GPS Coord"
    def __init__(self, longi=None, lati=None):
        self.lo = longi
        self.la = lati
    setPoint = __init__
    def getPoint(self): return (self.lo, self.la)
###################
### DEFINITIONS ###
###################

######################
# CALLBACK FUNCTIONS #
######################

def print_navdata(navdata):
    "Print the navdata as RAW text" 
    print navdata
    pass

def update_gui(navdata):
    "Update the GUI box"
    global gui
    if gui == None: return True
    if navdata["gps_info"] == None:    return True
    new_text = ""
    new_text = new_text + "Battery: " + str(navdata["navdata_demo"]["battery_percentage"]) + "%\n"
    new_text = new_text + "Unsupported options: " + str(navdata["unsupported_option"]) + "\n"
    
    # GPS
    new_text = new_text + "Latitude: " + str(navdata["gps_info"]["latitude"]) + "\n"
    new_text = new_text + "Longitude: " + str(navdata["gps_info"]["longitude"]) + "\n"
    new_text = new_text + "Elevation: " + str(navdata["gps_info"]["elevation"]) + "\n"
    new_text = new_text + "Hdop: " + str(navdata["gps_info"]["hdop"]) + "\n"
    new_text = new_text + "State: " + str(navdata["gps_info"]["data_available"]) + "\n"
    # Tags
##    new_text = new_text + "Number of tags: " + str(navdata["vision_detect"]["nb_detected"]) + "\n"
##    new_text = new_text + "XC: " + str(navdata["vision_detect"]["xc"]) + "\n"
##    new_text = new_text + "YC: " + str(navdata["vision_detect"]["yc"]) + "\n"
##    new_text = new_text + "Width: " + str(navdata["vision_detect"]["width"]) + "\n"
##    new_text = new_text + "Height: " + str(navdata["vision_detect"]["height"]) + "\n"
##    new_text = new_text + "Distance " + str(navdata["vision_detect"]["dist"]) + "\n"
    gui.change_text(new_text)
    return True

def save_gps_coord(navdata):
    "Save the last navdata coordinate in a global var"
    global last_coord, gui
    # Updata coord
    if navdata["gps_info"] == None:    return False
    last_coord = (navdata["gps_info"]["longitude"],navdata["gps_info"]["latitude"])

    # And GUI
    if gui == None: return False
    new_text = ""
    new_text = new_text + "Battery: " + str(navdata["navdata_demo"]["battery_percentage"]) + "%\n"
    new_text = new_text + "Unsupported options: " + str(navdata["unsupported_option"]) + "\n"
    # GPS
    new_text = new_text + "Latitude: " + str(navdata["gps_info"]["latitude"]) + "\n"
    new_text = new_text + "Longitude: " + str(navdata["gps_info"]["longitude"]) + "\n"
    new_text = new_text + "Elevation: " + str(navdata["gps_info"]["elevation"]) + "\n"
    new_text = new_text + "Hdop: " + str(navdata["gps_info"]["hdop"]) + "\n"
    new_text = new_text + "State: " + str(navdata["gps_info"]["data_available"]) + "\n"
    gui.change_text(new_text)    
    return True

##################
# TEST FUNCTIONS #
##################

# Choose your test
def choose_sequence(drone):
    "Choose a test program sequence"
    print "Please choose a test program you want to run:"
    print "1 - Take Off & Land"
    print "2 - Command line test"
    print "3 - GUI Command Test"
    print "4 - GPS Test"
    result = raw_input(">")
    if result == "1":
        takeoff_land(drone)
    elif result == "2":
        menu_list(drone)
    elif result == "3":
        print "-> Launching GUI ..."
        Command_GUI(drone)
    elif result == "4":
        print "-> Starting GPS Test ..."

# 1st Test: Just testing commands
def takeoff_land(drone):
    "Routine just to test takeoff_land"
    wait= raw_input("Press enter to take off...")
    drone.takeoff()
    wait= raw_input("Press enter to land..")
    drone.land()
    time.sleep(1)
    drone.stop()

# 2st Test: Command line
def menu_list(drone):
    "List of function you can perform"
    print "Choose your command:"
    print "0 - Emergency"
    print "1 - Hover"
    print "2 - Take Off"
    print "3 - Land"
    print "4 - Forward"
    print "5 - Backward"
    print "6 - Left"
    print "7 - Right"
    print "8 - Calibrate sensors"
    print "a - Reset"
    print "9 - Quit"
    result = ""
    while result != "9":
        result = raw_input(">")
        if result == "0": drone.emergency()
        if result == "1": drone.hover()
        if result == "2": drone.takeoff()
        if result == "3": drone.land()
        if result == "4": drone.forward()
        if result == "5": drone.backward()
        if result == "6": drone.left()
        if result == "7": drone.right()
        if result == "8": drone.calibrate()
        if result == "a": drone.reset()
        if result == "z": drone.up()
        if result == "s": drone.down()
        if result == "q": drone.rotate_left()
        if result == "d": drone.rotate_right()
        if result == "o": try_config()

# 3nd test
def Command_GUI(drone):
    "Create a GUI to command the drone"
    global gui
    gui = ARDroneGUI.ControlWindow(default_action=drone.hover)
    gui.add_action("<Up>",drone.forward)
    gui.add_action("<Down>",drone.backward)
    gui.add_action("<Left>",drone.left)
    gui.add_action("<Right>",drone.right)
    gui.add_action("<z>",drone.up)
    gui.add_action("<s>",drone.down)
    gui.add_action("<q>",drone.rotate_left)
    gui.add_action("<d>",drone.rotate_right)
    gui.add_action("<a>",drone.takeoff)
    gui.add_action("<space>",drone.land)
    gui.add_action("<Return>",drone.emergency)
    gui.add_action("<t>",drone.reset)
    gui.add_action("<y>",drone.calibrate)
    gui.add_action("<o>",lambda arg=drone: ARDroneConfig.activate_drone_detection(drone))
    gui.change_text("Waiting data ...\nYou can press o to start reception...\nCommands:\nArrows: Navigate\nZ-D: Up-Down\nQ-D: Rotate\nA-Space: TakeOff, Land\nReturn: Emergency\nT,Y,N: Reset, Calibrate, Activate data reception")
    gui.start()

# 4st test
def GPS_Command(drone):
    "Create a GUI to command the GPS"
    global gui, last_coord
    pos1 = GPS_Coord()
    pos2 = GPS_Coord()
    pos3 = GPS_Coord()
    gui.add_action("<d>",drone.rotate_right)
    gui.add_action("<a>",drone.takeoff)
    gui.add_action("<space>",drone.land)
    gui.add_action("<Return>",drone.emergency)
    gui.add_action("<t>",drone.reset)
    gui.add_action("<y>",drone.calibrate)
    gui.add_action("<o>",lambda arg=drone: ARDroneConfig.activate_drone_detection(drone))
    # GPS
    gui.add_action("<f>",lambda arg=last_coord: pos1.setPoint(last_coord))
    gui.add_action("<g>",lambda arg=last_coord: pos2.setPoint(last_coord))
    gui.add_action("<h>",lambda arg=last_coord: pos3.setPoint(last_coord))

    gui.add_action("<v>",lambda arg=pos1: ARDroneConfig.goto_gps_point(drone,arg.getPoint()[0],arg.getPoint()[1]))
    gui.add_action("<b>",lambda arg=pos2: ARDroneConfig.goto_gps_point(drone,arg.getPoint()[0],arg.getPoint()[1]))
    gui.add_action("<n>",lambda arg=pos3: ARDroneConfig.goto_gps_point(drone,arg.getPoint()[0],arg.getPoint()[1]))
    gui.change_text("Press o to start reception...\nF,G,H - Save GPS point\n V,B,N - GOTO GPS Point")
    gui.start()



    

##################
###  __MAIN__  ###
##################
if __name__ == "__main__":
    global drone
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Viq (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    # Create the drone
    drone = ARDroneLib.Drone(data_callback=update_gui)
##    try:
##        drone = ARDroneLib.ARDrone(data_callback=print_it)
##    except IOError:
##        wait = raw_input("Cannot connect to drone !")
##        sys.exit()

    # Tests
    choose_sequence(drone)
    drone.stop()
    
    
    print "Done !" 
