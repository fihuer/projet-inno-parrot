# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone NavData"
# version:
version = 1
# By Viq
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############

###############
### GLOBALS ###
###############

###############
### CLASSES ###
###############


###################
### DEFINITIONS ###
###################

def navdata_decode(packet):
    """Split then decodes the navdata packet gathered from UDP 5554"""
    import struct
    position=0
    offset = 0
    block=[]
    block.append(struct.unpack_from("IIII",packet,position))
    offset += struct.calcsize("IIII")
    i=1

    while 1:
        try:
            block.append([])
            block[i]=list(struct.unpack_from("HH",packet,offset)) #Separate Option ID & Size of option int
            offset += struct.calcsize("HH")
        except struct.error:
            break
        block[i].append(packet[offset:offset-struct.calcsize("HH")+int(block[i][1])])
        offset += block[i][1] - struct.calcsize("HH")
        i=i+1
        

    
            
     # NavData packet has been splited let's go decode it
    drone_state=dict() #It's in block[0]'s second 32bits int = block[0][1]
    drone_state['flying']              =block[0][1]       & 1
    drone_state['video_on']            =block[0][1]>>1    & 1
    drone_state['vision_on']           =block[0][1]>>2    & 1
    drone_state['angle_algo']          =block[0][1]>>3    & 1
    drone_state['altitude_algo']       =block[0][1]>>4    & 1
    drone_state['user_feedback']       =block[0][1]>>5    & 1
    drone_state['command_ack']         =block[0][1]>>6    & 1
    drone_state['fw_ok']               =block[0][1]>>7    & 1
    drone_state['fw_new']              =block[0][1]>>8    & 1
    drone_state['fw_update']           =block[0][1]>>9    & 1
    drone_state['navdata_demo']        =block[0][1]>>10   & 1 
    drone_state['navdata_bootstrap']   =block[0][1]>>11   & 1
    drone_state['motor_status']        =block[0][1]>>12   & 1 
    drone_state['com_lost']            =block[0][1]>>13   & 1
    drone_state['vbat_low']            =block[0][1]>>15   & 1
    drone_state['user_emergency']      =block[0][1]>>16   & 1
    drone_state['timer_elapsed']       =block[0][1]>>17   & 1
    drone_state['too_much_angle']      =block[0][1]>>19   & 1
    drone_state['ultrasound_ok']       =block[0][1]>>21   & 1
    drone_state['cutout']              =block[0][1]>>22   & 1
    drone_state['pic_version_ok']      =block[0][1]>>23   & 1
    drone_state['atcodec_thread_on']   =block[0][1]>>24   & 1
    drone_state['navdata_thread_on']   =block[0][1]>>25   & 1
    drone_state['video_thread_on']     =block[0][1]>>26   & 1
    drone_state['acq_thread_on']       =block[0][1]>>27   & 1
    drone_state['ctrl_watchdog']       =block[0][1]>>28   & 1
    drone_state['adc_watchdog']        =block[0][1]>>29   & 1
    drone_state['com_watchdog']        =block[0][1]>>30   & 1
    drone_state['emergency']           =block[0][1]>>31   & 1
    vision_detect=dict()
    for i in range(1,len(block)):
        if block[i][0]==16:
            vision_detect["nb_detected"]=block[i][2][0:2]
            vision_detect["type"]=block[i][2][2:4]
            vision_detect["xc"]=block[i][2][4:6]
            vision_detect["yc"]=block[i][2][6:8]
            vision_detect["width"]=block[i][2][8:10]
            vision_detect["height"]=block[i][2][10:12]
            vision_detect["dist"]=block[i][2][12:14]
            vision_detect["nb_detected"]=float(block[i][2][14:])
    
    navdata=dict()
    navdata['drone_state']=drone_state
    navdata['vision_detect']=vision_detect
    #navdata['vision'] = block[1]
    #navdata['header']=block[0][0]
    #navdata['sequence_nb']=block[0][2]
    #navdata['vision_flag']=block[0][3]
            
     
    return navdata
    
    

##################
###  __MAIN__  ###
##################
