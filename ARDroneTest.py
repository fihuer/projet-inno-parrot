# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone Test"
# version:
version = 3
# By Viq
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import time, sys, os
import ARDroneLib, ARDroneGUI

###############
### GLOBALS ###
###############

gui = None

###############
### CLASSES ###
###############


###################
### DEFINITIONS ###
###################

def choose_sequence(drone):
    "Choose a test program sequence"
    print "Please choose a test program you want to run:"
    print "1 - Take Off & Land"
    print "2 - Command line test"
    print "3 - GUI Command Test"
    result = raw_input(">")
    if result == "1":
        takeoff_land(drone)
    elif result == "2":
        menu_list(drone)
    elif result == "3":
        print "-> Launching GUI ..."
        Command_GUI(drone)

def takeoff_land(drone):
    "Routine just to test takeoff_land"
    wait= raw_input("Press enter to take off...")
    drone.takeoff()
    wait= raw_input("Press enter to land..")
    drone.land()
    time.sleep(1)
    drone.stop()

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
        
def Command_GUI(drone):
    "Create a GUI to command the drone"
    global gui
    print "-> Press o in the GUI to start tag regognition ..."
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
    gui.add_action("<o>",try_config)
    gui.start()

def print_it(navdata):
    "Print the msg"
    global a    
    #print navdata["vision_detect"]
    pass
def update_gui(navdata):
    "Update the GUI box"
    global gui
    if gui == None: return True
    if navdata["vision_detect"] == None:    return True
    new_text = ""
    new_text = new_text + "Unsupported options: " + str(navdata["unsupported_option"]) + "\n"
    new_text = new_text + "Number of tags: " + str(navdata["vision_detect"]["nb_detected"]) + "\n"
    new_text = new_text + "XC: " + str(navdata["vision_detect"]["xc"]) + "\n"
    new_text = new_text + "YC: " + str(navdata["vision_detect"]["yc"]) + "\n"
    new_text = new_text + "Width: " + str(navdata["vision_detect"]["width"]) + "\n"
    new_text = new_text + "Height: " + str(navdata["vision_detect"]["height"]) + "\n"
    new_text = new_text + "Distance " + str(navdata["vision_detect"]["dist"]) + "\n"
##    new_text = new_text + str(navdata['navdata_demo'])
    
    gui.change_text(new_text)
    
def try_config():
    "Try to issue a command"
    global drone
    print "-> Starting recognition ...."
    drone.comThread.config("general:navdata_demo","FALSE")
    drone.comThread.config("detect:detect_type","13")
    #color = "2"# Yellow-Orange
    color = "3" # Blue-Orange
    drone.comThread.config("detect:enemy_colors",color)
    drone.comThread.config("detect:enemy_without_shell","0")
    print "-> Started ..."
    

##################
###  __MAIN__  ###
##################
if __name__ == "__main__":
    global drone
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Viq (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    # Create the drone
    drone = ARDroneLib.ARDrone(data_callback=update_gui)
##    try:
##        drone = ARDroneLib.ARDrone(data_callback=print_it)
##    except StandardError:
##        wait = raw_input("Cannot connect to drone !")
##        sys.exit()

    # Tests
    choose_sequence(drone)
    drone.stop()
    
    
    print "Done !" 
