def navdata_decode(packet):
    """Split then decodes the navdata packet gathered from UDP 5554"""
    import struct
    position=0
    block=[]
    block[0]=struct.unpack_from("IIII",packet,position)
    offset += struct.calcsize("IIII")
    i=1
    while 1:
        try:
            block[i]=[]
            block[i]=struct.unpack_from("HH",packet,position) #Separate Option ID & Size of option int
            position += struct.calcsize("HH")
        except struct.error:
            break
        block[i][2]=[]
        for j in range(block[i][1]-struct.calcsize("HH")):#Number of data bits
            block[i][2].append(struct.unpack_from("c",packet,position)[0])
            position+=struct.calcsize("c")
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

     navdata=dict()
     navdata['drone_state']=drone_state
     navdata['header']=block[0][0]
     navdata['sequence_nb']=block[0][2]
     navdata['vision_flag']=block[0][3]

     while 1:
         try:
             for i in range (1,len(block)):
                 navdata_decode_option(navdata,block[i]) #To implement with the pattern of option, block[i]=[id,size,[data]]
            except IndexError:
                break
            except NameError: #Since navdata_decode_option is implemented
                break
            
     
     return navdata
    
    
