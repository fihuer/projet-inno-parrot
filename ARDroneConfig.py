# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "ARDrone Config"
# version:
version = 1
# By Vianney Tran, Romain Fihue, Giulia Guid, Julien Lagarde
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
    

##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Viq (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    print "> This is a library only, please use the test instead"
