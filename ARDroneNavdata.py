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

import struct

###############
### GLOBALS ###
###############

###############
### CLASSES ###
###############


###################
### DEFINITIONS ###
###################

def _drone_status_decode(packet):
    "Decode the block which contains Drone Status"
    # NavData packet has been splited let's go decode it
    drone_state=dict() #It's in block[0]'s second 32bits int = block[0][1]
    drone_state['flying']              = packet       & 1
    drone_state['video_on']            = packet>>1    & 1
    drone_state['vision_on']           = packet>>2    & 1
    drone_state['angle_algo']          = packet>>3    & 1
    drone_state['altitude_algo']       = packet>>4    & 1
    drone_state['user_feedback']       = packet>>5    & 1
    drone_state['command_ack']         = packet>>6    & 1
    drone_state['fw_ok']               = packet>>7    & 1
    drone_state['fw_new']              = packet>>8    & 1
    drone_state['fw_update']           = packet>>9    & 1
    drone_state['navdata_demo']        = packet>>10   & 1 
    drone_state['navdata_bootstrap']   = packet>>11   & 1
    drone_state['motor_status']        = packet>>12   & 1 
    drone_state['com_lost']            = packet>>13   & 1
    drone_state['vbat_low']            = packet>>15   & 1
    drone_state['user_emergency']      = packet>>16   & 1
    drone_state['timer_elapsed']       = packet>>17   & 1
    drone_state['too_much_angle']      = packet>>19   & 1
    drone_state['ultrasound_ok']       = packet>>21   & 1
    drone_state['cutout']              = packet>>22   & 1
    drone_state['pic_version_ok']      = packet>>23   & 1
    drone_state['atcodec_thread_on']   = packet>>24   & 1
    drone_state['navdata_thread_on']   = packet>>25   & 1
    drone_state['video_thread_on']     = packet>>26   & 1
    drone_state['acq_thread_on']       = packet>>27   & 1
    drone_state['ctrl_watchdog']       = packet>>28   & 1
    drone_state['adc_watchdog']        = packet>>29   & 1
    drone_state['com_watchdog']        = packet>>30   & 1
    drone_state['emergency']           = packet>>31   & 1
    return drone_state

##def _vision_detect_decode(packet):
##    "Decode the vision detection packet, packet is (id=13, size, data)"
##    if packet[0] != 16:
##        raise IOError("Packet is not vision packet")
##    # Have to check if there isn't tag and size first
##    decoded = struct.unpack_from("IIIIIIIf",packet[2],0)
##    vision_detect = dict()
##    vision_detect["nb_detected"] = decoded[0]
##    vision_detect["type"] = decoded[1]
##    vision_detect["xc"] = decoded[2]
##    vision_detect["yc"] = decoded[3]
##    vision_detect["width"] = decoded[4]
##    vision_detect["height"] = decoded[5]
##    vision_detect["dist"] = decoded[6]
##    vision_detect["orientation"] = decoded[7]
##    vision_detect["p"] = packet[2]
##    return vision_detect

def _vision_detect_decode(packet):
    "Decode the vision detection packet, packet is (id=13, size, data)"
    if packet[0] != 16:
        raise IOError("Packet is not vision packet")
    # Have to check if there isn't tag and size first
    vision_detect = dict()
    vision_detect["nb_detected"] = struct.unpack_from("=I",packet[2][0:20])[0]
    vision_detect["xc"] = struct.unpack_from("=I",packet[2][20:36])[0]
    vision_detect["yc"] = struct.unpack_from("=I",packet[2][36:52])[0]
    vision_detect["width"] = struct.unpack_from("=I",packet[2][52:68])[0]
    vision_detect["height"] = struct.unpack_from("=I",packet[2][68:84])[0]
    vision_detect["dist"] = struct.unpack_from("=I",packet[2][84:100])[0]
    #vision_detect["p"] = packet[2]
    return vision_detect
    
    
    
    

def navdata_decode(packet):
    "Split then decodes the navdata packet gathered from UDP 5554"
    position=0
    offset = 0
    block=[]
    block.append(struct.unpack_from("=IIII",packet,position))
    offset += struct.calcsize("=IIII")
    i=1

    while 1:
        try:
            block.append([])
            block[i]=list(struct.unpack_from("=HH",packet,offset)) #Separate Option ID & Size of option int
            offset += struct.calcsize("=HH")
        except struct.error:
            break
        block[i].append(packet[offset:offset-struct.calcsize("=HH")+int(block[i][1])])
        offset += block[i][1] - struct.calcsize("=HH")
        i=i+1
    # block[0]      is (header, drone_state, sequence_number, vision_flag)
    # block[1:-1]   is Option0, Option1 ...
    # block[-1]     is checksum
    
    # Decode the drone state
    drone_state = _drone_status_decode(block[0][1])
    vision_detect = None

    # For each option
    unsupported_option = []
    for i in range(1,len(block)):
        if block[i] != []:
            # Vision detection option
            if block[i][0]==16:
                vision_detect = _vision_detect_decode(block[i])
            # Checksum option
            elif block[i][0] == 65535:
                pass
            # Else we don't know
            else:
                unsupported_option.append(block[i][0])
                
    
    navdata=dict()
    navdata['drone_state']=drone_state
    navdata['vision_detect']=vision_detect
    navdata['unsupported_option'] = unsupported_option
    #navdata['vision_flag']=block[0][3]
    return navdata
    
    

##################
###  __MAIN__  ###
##################
