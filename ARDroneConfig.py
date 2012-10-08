# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone Config"
# version:
version = 1
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import os, time

###############
### GLOBALS ###
###############

###############
### CLASSES ###
###############


###################
### DEFINITIONS ###
###################

def activate_drone_detection(drone, color=0):
    """ Send the config to the drone to activate drone detection
        0 is the blue-orange color
        1 is the yellow-orange color"""
    if color == 1:  tag_color = "2"
    else:           tag_color = "3"
    drone.comThread.config("general:navdata_demo","FALSE")
    drone.comThread.config("detect:detect_type","13")
    drone.comThread.config("detect:enemy_colors",tag_color)
    drone.comThread.config("detect:enemy_without_shell","0")
    return True
    
def goto_gps_point(drone, longitude, latitude, altitude=3, cap=0):
    "Send the drone to the GPS point, cap is in degre"
    if (longitude is None) or (latitude is None):   return False
    if (longitude == 0) or (latitude == 0):   return False # Try not to send drone to somewhere weird
    print "> Sending drone to GPS point ",longitude,latitude,altitude,"..."
    # Compute each data
    longi = int(longitude*1000000)
    lati = int(latitude*1000000)
    alt = int(altitude*1000)
    cap = int(cap)
    # Create the right parameter according to doc
    param1 = "0,8,"+str(longi)+","+str(lati)+","+str(alt)+",0,0,0," + str(cap) + ",0"
    # Let's go !
    drone.comThread.config("control:autonomous_flight","FALSE")
    drone.comThread.config("control:travelling_mode",param1)
    drone.comThread.config("control:travelling_enable","TRUE")
    print "-> Command issued"
    return True
    
##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    print "> This is a library only, please use the test instead"

