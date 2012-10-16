# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone Config"
# version:
version = 2
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
def activate_tag(drone, color=0):
    """ Send the config to the drone to activate drone detection
        0 is the blue-orange color
        1 is the yellow-orange color"""
    if color == 1:  tag_color = "2"
    else:           tag_color = "3"
    drone.configure("detect:detect_type","13")
    drone.configure("detect:enemy_colors",tag_color)
    drone.configure("detect:enemy_without_shell","0")
    return True

# Autonomous Flight
def goto_gps_point(drone, longitude, latitude, altitude=2, cap=0):
    "Send the drone to the GPS point, cap is in degre"
    if (longitude is None) or (latitude is None):   return False
    if (longitude == 0) or (latitude == 0):   return False # Try not to send drone to somewhere weird
    print "> Sending drone to GPS point ",longitude,latitude,altitude,"..."
    # Compute each data
    longi = int(longitude*10000000)
    lati = int(latitude*10000000)
    alt = int(altitude*1000)
    cap = int(cap)
    # Create the right parameter according to doc
    param1 = "10,5,"+str(lati)+","+str(longi)+","+str(alt)+",0,0,0," + str(cap) + ",0"
    #param1 = "0,10,1500,0,0,0,0,0,0,0,0" # Forward traveling (1500 is x speed)
    # Let's go !
    drone.configure("control:flying_mode","0")
    drone.configure("control:autonomous_flight","FALSE")
    drone.configure("control:travelling_mode",param1)
    drone.continuous_config("control:travelling_enable","TRUE")
    return True

    
##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    print "> This is a library only, please use the test instead"

