# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone GUI"
# version:
version = 2
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import os, time, threading
from Tkinter import *


###############
### GLOBALS ###
###############

###############
### CLASSES ###
###############

class ControlWindow():
    "Create a window to control the drone"
    def __init__(self,default_action):
        "Create a window to control the drone"
        self.actions = []
        self.bhandler = ButtonHandler(default_action)
        self.bhandler.start()
        self.text = None
        self.to_print = list()
        
    def add_action(self,button_bind,function_call):
        "Add an action when a key is pressed"
        self.actions.append((button_bind,function_call))
        return True
    def add_printable_data(self, description, tree):
        "Add something in navdata to print, tree is a tulpe"
        # Check if the arguments are good
        if type(tree) != type((0,0)):   raise TypeError("Tree must be a tulpe")
        self.to_print.append((str(description),tree))
        return True

    def callback(self, navdata):
        "Callback function that can be given to Navdata filter"
        new_text = ""
        if navdata["navdata_demo"] is None: return False
        for p in self.to_print:
            # Get data
            data = navdata
            # Get the tree
            for key in p[1]:
                if data != None:
                    data = data[str(key)]
                else:
                    data = "No data"
                    break
            # Format
            new_text = new_text + str(p[0]) + ": " + str(data) + "\n"
        # And done
        return self.change_text(new_text)
    def start(self):
        "Activate the window (and keep the thread)"
        self.fen = Tk()
        cadre = Frame(self.fen, width=500, height = 200, bg="grey")
        self.text = Label(self.fen,text="Waiting data ...", fg = "black")
        self.text.pack()
        for act in self.actions:
            self.bhandler.add_action(act[0],act[1])
            self.fen.bind(act[0],lambda a=act[0]: self.bhandler.trigger(a))
        cadre.pack()
        self.fen.protocol("WM_DELETE_WINDOW", lambda a=1: kill_fen(self))
        self.fen.mainloop()
    def change_text(self, new_text):
        "Change the text inside the box"
        if self.bhandler.running == False:  return False
        if self.text == None:               return False
        self.text.configure(text=str(new_text))
        return True

class ButtonHandler(threading.Thread):
    "Handle when the key are pressed or released"
    def __init__(self,default_action):
        self.running = True
        self.last_time = time.time()
        self.last_action = None
        self.default_action = default_action
        self.actions = {}
        threading.Thread.__init__(self)
        
    def add_action(self, event, action):
        "Add an action to the list"
        self.actions[event] = action

    def run(self):
        "Refresh action every 0.1 sec"
        last_action = None
        timer = time.time()
        while self.running:
            if (time.time() - self.last_time) > 0.2:
                if last_action != None:
                    self.default_action()
                    last_action = None
            else:
                if last_action != self.last_action:
                    last_action = self.last_action
                    self.actions[last_action]()
            time.sleep(0.01)
    def trigger(self,action):
        "Called when a button is pressed or hold"
        action = "<" + action.keysym + ">"
        self.last_action = action
        self.last_time = time.time()
    def stop(self):
        "Stop the handler"
        self.running = False

###################
### DEFINITIONS ###
###################
def kill_fen(root):
    "Kill the window that called"
    root.bhandler.stop()
    root.fen.destroy()
    root.fen.quit()
    return lambda a=1:a

def nothing():
    "Do nothing"
    pass

##################
###  __MAIN__  ###
##################
if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    gui = ControlWindow(nothing)
    gui.add_action("<Up>",lambda arg=gui:gui.change_text("Up Arrow pressed"))
    gui.add_action("<a>",lambda arg=gui:arg.change_text("A button pressed"))
    gui.bhandler.default_action = lambda arg="a": gui.change_text("No button pressed")
    gui.change_text("Press a button to start example ...")
    gui.start()
