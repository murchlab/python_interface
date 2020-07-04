import numpy as np
import sys
sys.path.append(r"C:\Users\crow104\Documents\Python Scripts\sequence_generator")
from generator_nonHermian import *
#from generator import *
import wx_programs
import os
pi = np.pi
import matplotlib.pyplot as plt




def es_transport(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    rabi_time = 4000
    pi_ge=34
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.09175
    ssm_hf = 0.205

#    p_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#    p_pi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#
#    p_pi_ef = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
#    p_pi_ef.phase = 180
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
#
    p_pi_ge = Pulse(start=6995-pi_ge/2, duration=-pi_ge/2, amplitude=.5, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    
    pt_pi_ef_r = Pulse(start=6995-pi_ge/2, duration=0, amplitude=.5, ssm_freq=ssm_ge, phase=180,phase_ini=0, t_loop=rabi_time, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
    pt_pi_ef_r.phase = 270
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pt_pi_ef = Pulse(start=6995-pi_ge/2, duration=0, amplitude=0.5, ssm_freq=ssm_ge, phase=270,phase_ini=1*np.pi/2, t_loop=rabi_time, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef)
    pt_pi_ef.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef)
    
    p_pi_ge_r = Pulse(start=6995, duration=-pi_ge/2, amplitude=.5, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,5000:7000], aspect='auto', extent=[5000,7000,200,0])
#        plt.plot(channel1_ch[50,:],'b--o')
 
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\test"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom



def es_drive(pi_ge=34): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    rabi_time = 2000
#    pi_ge=34
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205

#    p_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#    p_pi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#
#    p_pi_ef = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
#    p_pi_ef.phase = 180
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)

    p_pi_ge = Pulse(start=6995-pi_ge/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase =90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#
    p_pi_ge = Pulse(start=6995, duration=-pi_ge/2, amplitude=.5, ssm_freq=ssm_ge, phase=270)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    
    pt_pi_ef_r = Pulse(start=6995, duration=0, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
    pt_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)


    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,5000:7000], aspect='auto', extent=[5000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\test"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def es_drive_jump(amp_ef=0.3): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
#    detunlin = - 0.1
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class
# note: amp_ef 0.3 for eigenstate with less dissipation, phase 270, 360
    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    rabi_time = 200
    pi_ge=34
    pi_ef=28 
    pi_hf=26
    
    ssm_ef_detun = -0.01
#    amp_ef=0.2
    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205

#    p_pi_ge = Pulse(start=6995-pi_ef, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
#    p_pi_ge.phase =90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    ###
#    p_pi_ge = Pulse(start=6995-32-pi_ef, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#    p_pi_ge.phase =90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#
#    p_pi_ef = Pulse(start=6995-pi_ef, duration=-32, amplitude=amp_ef, ssm_freq=ssm_ef, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
#    p_pi_ef.phase = 180
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
#    
#    pt_pi_ef_r = Pulse(start=6995-pi_ef, duration=0, amplitude=.5, ssm_freq=ssm_ef+ssm_ef_detun, phase=0, detunlinear = ssm_ef_detun)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=3, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
#    pt_pi_ef_r.phase = 90
#    the_seq.add_sweep(channel=4,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
##
#    p_pi_ef = Pulse(start=6995, duration=-pi_ef, amplitude=0.25, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='phase_linear_detun', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
#    p_pi_ef.phase =90
#    the_seq.add_sweep(channel=2,  sweep_name='phase_linear_detun', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)  
# 
#    p_pi_ef = Pulse(start=6995, duration=-pi_ef, amplitude=0.25, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
#    p_pi_ef.phase =90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)     
    
    ###
    #### ###
    p_pi_ge = Pulse(start=6995-32-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase =90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)

    p_pi_ef = Pulse(start=6995-pi_ef/2, duration=-32, amplitude=amp_ef, ssm_freq=ssm_ef, phase=270, clock_freq=ssm_ef-ssm_ef_detun)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
    p_pi_ef.phase = 360
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
    
    pt_pi_ef_r = Pulse(start=6995-pi_ef/2, duration=0, amplitude=.5, ssm_freq=ssm_ef+ssm_ef_detun, phase=0, clock_freq=ssm_ef-ssm_ef_detun)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
    pt_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
    
    p_pi_ef = Pulse(start=6995, duration=-pi_ef/2, amplitude=0.5, ssm_freq=ssm_ef, phase=270, clock_freq=ssm_ef-ssm_ef_detun)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=p_pi_ef)
    p_pi_ef.phase = 360
    the_seq.add_sweep(channel=2,  sweep_name='none', initial_pulse=p_pi_ef)  
    #### ###
    
#    p_pi_ef = Pulse(start=6995, duration=-pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=p_pi_ef) 
#    p_pi_ef.phase =90
#    the_seq.add_sweep(channel=2,  sweep_name='none', initial_pulse=p_pi_ef)
#    
#    pt_pi_ef_r = Pulse(start=6995+pi_ef/2, duration=pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=3, sweep_name='phase_linear_detun', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
#    pt_pi_ef_r.phase = 90
#    the_seq.add_sweep(channel=4,  sweep_name='phase_linear_detun', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)


    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        plt.plot(channel1_ch[10,:],'b--o')
#        plt.plot(channel2_ch[2,:],'y--*')
#        plt.plot(channel3_ch[10,:],'r-s')
#        plt.xlim(6910,7000)
#        plt.show()
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\test"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
#  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def es_drive_ef(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    rabi_time = 2000
    pi_ge=34
    pi_ef=28 
    pi_hf=34

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.243

#    p_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#    p_pi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#
#    p_pi_ef = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
#    p_pi_ef.phase = 180
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)

    p_pi_ge = Pulse(start=6995-3*pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase =90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)

    p_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase =90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#
    p_pi_ge = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    
    pt_pi_ef_r = Pulse(start=6995, duration=0, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
    pt_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)


    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,5000:7000], aspect='auto', extent=[5000,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\test"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom


def phase_meas_esdrive(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    pi_ge=16
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205
#    off_set=0


#
    p_pi_ge = Pulse(start=6995-2*pi_ge-1*pi_ef-rabi_time, duration=-2*pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ef = Pulse(start=6995-2*pi_ge-pi_ef/2-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    

    p2_pi_ge = Pulse(start=6995-pi_ge-pi_ef/2-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=270)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p2_pi_ge)
    
    pt_pi_ge_r = Pulse(start=6995-pi_ge-pi_ef/2, duration=-rabi_time, amplitude=.3, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pt_pi_ge_r)

    
    p_pi_ge_r = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)

    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def phase_meas_esdrive_diff_ang(rabi_time = 100,off_set=0,ang=160): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    pi_ge=16
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205
#    off_set=0
    
    


#
    p_pi_ge = Pulse(start=6995-2*pi_ge-1*pi_ef-rabi_time, duration=-2*pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ef = Pulse(start=6995-2*pi_ge-pi_ef/2-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    

    p2_pi_ge = Pulse(start=6995-pi_ge-pi_ef/2-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=270+ang)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 0+ang
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p2_pi_ge)
    
    pt_pi_ge_r = Pulse(start=6995-pi_ge-pi_ef/2, duration=-rabi_time, amplitude=.3, ssm_freq=ssm_ge, phase=0+ang)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90+ang
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pt_pi_ge_r)

    
    p_pi_ge_r = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=90+ang)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 180+ang
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)

    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def phase_meas_esdrive_hf(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    pi_ge=34
    pi_ef=28 
    pi_hf=40

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.243
#    off_set=0
    esph=270


#
    p_pi_ge = Pulse(start=6995-pi_hf-3*pi_ef-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)

    p_pi_ef = Pulse(start=6995-pi_hf-pi_ef-pi_ef-rabi_time, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    
    p_pi_hf = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef-rabi_time, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_hf)
    p_pi_hf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_hf)
    

    p2_pi_ge = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef/2-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=90+esph)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 180+esph
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p2_pi_ge)
    
    pt_pi_ge_r = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef/2, duration=-rabi_time, amplitude=.1, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=pt_pi_ge_r)

    
    p_pi_ef_r = Pulse(start=6995-pi_hf/2-pi_ef, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=270+esph)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 0+esph
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef_r)


    rabi_ef = Pulse(start=6995-pi_ef, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=rabi_ef)
    rabi_ef.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=rabi_ef)

    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6500:7000], aspect='auto', extent=[6500,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def pi2prep(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    rabi_time = 0
    pi_ge=34
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205

    p_pi_ge = Pulse(start=6995-pi_ef, duration=-pi_ge, amplitude=0.52, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ge_r = Pulse(start=6995, duration=-pi_ef, amplitude=0, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='amplitude' , start=0, stop=1 ,initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='amplitude' , start=0, stop=1,initial_pulse=p_pi_ge_r)
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none' ,initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6900:7000], aspect='auto', extent=[6900,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\test"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def loading():
      

    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps)      
    write_dir = r"C:\Data\2019\encircling\rabi"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0,amp34=.4)
    
##END geom
 
def loading_jump():
      

    file_length = 8000
    num_steps = 2*301
    the_seq = Sequence(file_length, num_steps)      
    write_dir = r"C:\Data\2019\encircling\test"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def phase_meas_transport(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    pi_ge=16
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205
#    off_set=0


#
    p_pi_ge = Pulse(start=6995-2*pi_ge-1*pi_ef-rabi_time, duration=-2*pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ef = Pulse(start=6995-2*pi_ge-pi_ef/2-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    

    p2_pi_ge = Pulse(start=6995-pi_ge-pi_ef/2-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p2_pi_ge)
    
    pt_pi_ge_r = Pulse(start=6995-pi_ge-pi_ef/2, duration=-rabi_time, amplitude=1, ssm_freq=ssm_ge, phase=0,phase_ini=0, t_loop=rabi_time, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pt_pi_ge_r)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pt_pi_ge = Pulse(start=6995-pi_ge-pi_ef/2, duration=-rabi_time, amplitude=1, ssm_freq=ssm_ge, phase=90,phase_ini=1*np.pi/2, t_loop=rabi_time, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pt_pi_ge)
    pt_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pt_pi_ge)
    
    p_pi_ge_r = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=270)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)

    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def phase_meas_transport_hf(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    pi_ge=34
    pi_ef=28 
    pi_hf=40
    sphase = 90

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.243
#    off_set=0


#
    p_pi_ge = Pulse(start=6995-pi_hf-3*pi_ef-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ge = Pulse(start=6995-pi_hf-2*pi_ef-rabi_time, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)

    p_pi_hf = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef-rabi_time, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_hf)
    p_pi_hf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_hf)
    
    p_pi_ef = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef/2-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=270+sphase)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 0+sphase
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    
    
    pt_pi_ge_r = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef/2, duration=-rabi_time, amplitude=.1, ssm_freq=ssm_ef, phase=0,phase_ini=0, t_loop=rabi_time, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=pt_pi_ge_r)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pt_pi_ge = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef/2, duration=-rabi_time, amplitude=.1, ssm_freq=ssm_ef, phase=90,phase_ini=1*np.pi/2, t_loop=rabi_time, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pt_pi_ge)
    pt_pi_ge.phase = 180
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=pt_pi_ge)
    
    p_pi_ge_r = Pulse(start=6995-pi_hf/2-pi_ef, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=90+sphase)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 180+sphase
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)

    p_pi_ef_r = Pulse(start=6995-pi_ef, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)

    p_pi_ge = Pulse(start=6995, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6750:7000], aspect='auto', extent=[6750,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def phase_meas_partial_transport_hf(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    tloop=1500
    pi_ge=34
    pi_ef=28 
    pi_hf=40
    sphase = 0
    par=rabi_time/tloop
    

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.243
#    off_set=0


#
    p_pi_ge = Pulse(start=6995-pi_hf-3*pi_ef-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ge = Pulse(start=6995-pi_hf-2*pi_ef-rabi_time, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)

    p_pi_hf = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef-rabi_time, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_hf)
    p_pi_hf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_hf)
    
    p_pi_ef = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef/2-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=270+sphase)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 0+sphase
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    
    
    pt_pi_ge_r = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef/2, duration=-rabi_time, amplitude=.5, ssm_freq=ssm_ef, phase=0,phase_ini=0, t_loop=tloop, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=pt_pi_ge_r)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pt_pi_ge = Pulse(start=6995-pi_hf/2-pi_ef-pi_ef/2, duration=-rabi_time, amplitude=.5, ssm_freq=ssm_ef, phase=90,phase_ini=1*np.pi/2, t_loop=tloop, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pt_pi_ge)
    pt_pi_ge.phase = 180
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=pt_pi_ge)
    
    p_pi_ge_r = Pulse(start=6995-pi_hf/2-pi_ef, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=90+sphase+360/par)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 180+sphase+360/par
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)

    p_pi_ef_r = Pulse(start=6995-pi_ef, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)

    p_pi_ge = Pulse(start=6995, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6750:7000], aspect='auto', extent=[6750,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def phase_meas_partial_transport(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    tloop=1500
#    phase_ini=np.pi/2
#    rabi_time = 4000
    par=rabi_time/tloop
    pi_ge=16
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.2
#    off_set=0


#
    p_pi_ge = Pulse(start=6995-2*pi_ge-1*pi_ef-rabi_time, duration=-2*pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ef = Pulse(start=6995-2*pi_ge-pi_ef/2-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    

    p2_pi_ge = Pulse(start=6995-pi_ge-pi_ef/2-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p2_pi_ge)
    
    pt_pi_ge_r = Pulse(start=6995-pi_ge-pi_ef/2, duration=-rabi_time, amplitude=.5, ssm_freq=ssm_ge, phase=0,phase_ini=0, t_loop=tloop, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pt_pi_ge_r)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pt_pi_ge = Pulse(start=6995-pi_ge-pi_ef/2, duration=-rabi_time, amplitude=.5, ssm_freq=ssm_ge, phase=90,phase_ini=1*np.pi/2, t_loop=tloop, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pt_pi_ge)
    pt_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pt_pi_ge)
    
    p_pi_ge_r = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=270 + 360*1/par)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 0 + 360*1/par
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)

    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom


def xtransport_ef(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    tloop=2000
    rabi_time = 2000
    par=rabi_time/tloop
    pi_ge=34
    pi_ef=28 
    pi_hf=34
#    par=4/3
    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.243
    off_set=0


    p_pi_ge = Pulse(start=6995-2*pi_ef, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ge)
    
    p_pi_ge = Pulse(start=6995-pi_ef, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ge)
    
#    p_pi_ef = Pulse(start=6995-2*pi_ge-pi_ef/2, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ef)
#    p_pi_ef.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ef)
    

    p2_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p2_pi_ge)
    
    pt_pi_ge_r = Pulse(start=6995-pi_ef/2, duration=0, amplitude=.3, ssm_freq=ssm_ef, phase=0,phase_ini=0, t_loop=tloop, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width',start=0 , stop= -rabi_time ,initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width',start=0 , stop= -rabi_time ,initial_pulse=pt_pi_ge_r)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pt_pi_ge = Pulse(start=6995-pi_ef/2, duration=0, amplitude=.3, ssm_freq=ssm_ef, phase=90,phase_ini=1*np.pi/2, t_loop=tloop, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width',start=0 , stop= -rabi_time ,initial_pulse=pt_pi_ge)
    pt_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='width',start=0 , stop= -rabi_time ,initial_pulse=pt_pi_ge)
    
    p_pi_ge_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=270+360*1/par)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 0+360*1/par
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)

#    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',start=0, stop=360,initial_pulse=p_pi_ef_r)
#    p_pi_ef_r.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',start=0, stop=360,initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom


def xtransport(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    tloop=2000
    rabi_time = 1000
    par=rabi_time/tloop
    pi_ge=16
    pi_ef=28 
    pi_hf=26
#    par=4/3
    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205
    off_set=0


#
    p_pi_ge = Pulse(start=6995-2*pi_ge, duration=-2*pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ge)
    
#    p_pi_ef = Pulse(start=6995-2*pi_ge-pi_ef/2, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ef)
#    p_pi_ef.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p_pi_ef)
    

    p2_pi_ge = Pulse(start=6995-pi_ge, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='start',start=0 , stop= -rabi_time ,initial_pulse=p2_pi_ge)
    
    pt_pi_ge_r = Pulse(start=6995-pi_ge, duration=0, amplitude=.3, ssm_freq=ssm_ge, phase=0,phase_ini=0, t_loop=tloop, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width',start=0 , stop= -rabi_time ,initial_pulse=pt_pi_ge_r)
    pt_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width',start=0 , stop= -rabi_time ,initial_pulse=pt_pi_ge_r)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pt_pi_ge = Pulse(start=6995-pi_ge, duration=0, amplitude=.3, ssm_freq=ssm_ge, phase=90,phase_ini=1*np.pi/2, t_loop=tloop, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width',start=0 , stop= -rabi_time ,initial_pulse=pt_pi_ge)
    pt_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='width',start=0 , stop= -rabi_time ,initial_pulse=pt_pi_ge)
    
    p_pi_ge_r = Pulse(start=6995, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=270+360*1/par)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 0+360*1/par
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge_r)

#    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',start=0, stop=360,initial_pulse=p_pi_ef_r)
#    p_pi_ef_r.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',start=0, stop=360,initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_measurement"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def phase_meas_no_transport(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    pi_ge=16
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205
#    off_set=0

#    p_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#    p_pi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#

#
    p_pi_ge = Pulse(start=6995-2*pi_ef-rabi_time, duration=-pi_ge, amplitude=1, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ef = Pulse(start=6995-pi_ef/2-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    


    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_ntransport"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def phase_meas_no_transport_hf(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    pi_ge=34
    pi_ef=28 
    pi_hf=40

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.243
#    off_set=0

#    p_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#    p_pi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#

#
    p_pi_ge = Pulse(start=6995-pi_ef-pi_hf-pi_ef-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)

    p_pi_ef = Pulse(start=6995-pi_hf-pi_ef-rabi_time, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    
    p_pi_hf = Pulse(start=6995-pi_hf/2-pi_ef-rabi_time, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_hf)
    p_pi_hf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_hf)
    


    p_pi_ef_r = Pulse(start=6995-pi_ef, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)

    p_pi_ef2 = Pulse(start=6995, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef2)
    p_pi_ef2.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef2)    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_ntransport"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom    
    
def phase_meas_xf(rabi_time = 100,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 37
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
#    rabi_time = 4000
    pi_ge=16
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205
#    off_set=0

#    p_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#    p_pi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
#

#
    p_pi_ge = Pulse(start=6995-pi_ef-2*pi_ge-rabi_time, duration=-pi_ge, amplitude=1, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ef = Pulse(start=6995-pi_ef/2-2*pi_ge-rabi_time, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)
    
    p_pi_ge = Pulse(start=6995-pi_ef/2-pi_ge-rabi_time, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)

    p_pi_ge = Pulse(start=6995-pi_ef/2, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=270)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)
    
    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=.5, ssm_freq=ssm_ef, phase=0)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='phase',start=0, stop=360,initial_pulse=p_pi_ef_r)
    
    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\phase_ntransport"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def es_evolution(amp=.5): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    rabi_time = 400
    pi_ge=34
    pi_ef=28 
    pi_hf=26

    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.205
    

#
    p_pi_ge = Pulse(start=6995-pi_ge/2, duration=-pi_ge/2, amplitude=amp, ssm_freq=ssm_ge, phase=90)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    
    pt_pi_ef_r = Pulse(start=6995-pi_ge/2, duration=0, amplitude=.5, ssm_freq=ssm_ge, phase=180)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)
    pt_pi_ef_r.phase = 270
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pt_pi_ef_r)


    #main readout 
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,5000:7000], aspect='auto', extent=[5000,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\test"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
def rabi_ge_with_2pi_phase_shift(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
#    t_loop=2000
#    phase_ini=np.pi/2
    rabi_time = 1000
    ssm_ge = 0.3885
    p_pi_ge_r = Pulse(start=6995, duration=0, amplitude=1, ssm_freq=ssm_ge, phase=0,phase_ini=0, t_loop=rabi_time, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=p_pi_ge_r)
    p_pi_ge_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=p_pi_ge_r)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    p_pi_ge = Pulse(start=6995, duration=0, amplitude=1, ssm_freq=ssm_ge, phase=90,phase_ini=np.pi/2, t_loop=rabi_time, ff=1)#, phase_ini=np.pi/2, t_loop=400, ff=1) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 180
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1)
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\test"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def rabi_ef(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=29
    rabi_time = 100
    ssm_ge = 0.3885
    ssm_ef = 0.0917
    p_pi_ge = Pulse(start=6995, duration= -pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)

#    p_pi_ef = Pulse(start=6995, duration= -pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
#    p_pi_ef.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)

    rabi_ef = Pulse(start=6995, duration=0, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ef)
    rabi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ef)




#    g_ge = Pulse(start=6997, duration=100, amplitude=0.5E-20, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=g_ge)
#    g_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=g_ge)

    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6840:7000], aspect='auto', extent=[6840,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\rabi_ef"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def unbroken_es(phases=0,off_set=0): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=13
    rabi_time = 50
    ssm_ge = 0.3885
    ssm_ef = 0.0917
    p_pi_ge = Pulse(start=6995-pi_ef-rabi_time, duration= -pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ge)

    p_pi_ef = Pulse(start=6995-rabi_time, duration= -pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0+phases) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90+phases
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=p_pi_ef)

    rabi_ef = Pulse(start=6995, duration=rabi_time, amplitude=0, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='amplitude', start=0, stop=.3,initial_pulse=rabi_ef)
    rabi_ef.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='amplitude', start=0, stop=.3,initial_pulse=rabi_ef)



#    g_ge = Pulse(start=6997, duration=100, amplitude=0.5E-20, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=g_ge)
#    g_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=g_ge)

    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6840:7000], aspect='auto', extent=[6840,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\rabi_ef"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=1887+off_set, write_binary=True)
  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def rabi_hf(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=28
    rabi_time = 100
    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = .2424
    p_pi_ge = Pulse(start=6995-2*pi_ef, duration=-pi_ge, amplitude=.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ge)

    p_pi_ef = Pulse(start=6995-pi_ef, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=p_pi_ef)

    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    rabi_hf = Pulse(start=6995-pi_ef, duration=0, amplitude=1, ssm_freq=ssm_hf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_hf)
    rabi_hf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_hf)

    pi_ef_in = Pulse(start=6995, duration=-pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ef_in)
    pi_ef_in.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi_ef_in)

    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\rabi_hf"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def rabi_det(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class
    off_set=0
    ## channels  
    pi_ge=34
    rabi_time = 100
    ssm_ge = 0.01
    rabi_ge = Pulse(start=6995, duration=-50, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=rabi_ge)
    rabi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=rabi_ge)
    
    rabi_ge = Pulse(start=6995, duration=0, amplitude=0.5, ssm_freq=ssm_ge+.012, phase=0, detunlinear=0.012) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ge)
    rabi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ge)


    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.plot(channel2_ch[20,6800:7000])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
    write_dir = r"C:\Data\2019\encircling\rabi"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
#  
#    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    

def rabi(ssm_ge = .387): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class
    off_set=0
    ## channels  
    pi_ge=34
    rabi_time = 100
#    ssm_ge = .387

    rabi_ge = Pulse(start=6995, duration=0, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ge)
    rabi_ge.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ge)


    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.plot(channel1_ch[50,6800:7000],'b--o')
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
    write_dir = r"C:\Data\2019\encircling\rabi"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
    wx_programs.wx_set_and_amplitude_and_offset()
##END geom
    
    
def two_level_ep(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 201
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class
    off_set=0
    ## channels  
    pi_ge=34
    rabi_time = 2000
    ssm_ge = 0.3885+0.001
    
    rabi_ge2 = Pulse(start=6995, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=rabi_ge2)
    rabi_ge2.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=rabi_ge2)
    
    rabi_ge = Pulse(start=6995, duration=0, amplitude=0.1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ge)
    rabi_ge.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ge)

    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
    write_dir = r"C:\Data\2019\encircling\rabi"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0,amp34=.5)
##END geom
    
def calibrating_offset(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 3
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class
    off_set=2
    ## channels  
    pi_ge=34
    pi_ef=28
    rabi_time=6999
    ssm_ef=0.0935
    ssm_ge = 0.1
    rabi_ge = Pulse(start=6999, duration=-rabi_time, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=rabi_ge)
    rabi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=rabi_ge)

#    g_ge = Pulse(start=6997, duration=-(pi_ge+2), amplitude=0.5E-20, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=g_ge)
#    g_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=g_ge)
#    
#    rabi_ge = Pulse(start=6995-pi_ef, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=rabi_ge)
#    rabi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=rabi_ge)
#    
#    rabi_ef = Pulse(start=6995, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=rabi_ef)
#    rabi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=rabi_ef)
    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
    write_dir = r"C:\Data\2019\encircling\rabi"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
    
def no_pi_pi_pipi(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 3
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class
    off_set=2
    ## channels  
    pi_ge=34
    pi_ef=28
    ssm_ef=0.092
    ssm_ge = 0.3885
#    rabi_ge = Pulse(start=6995, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=rabi_ge)
#    rabi_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=rabi_ge)
###
    
    rabi_ge = Pulse(start=6995-pi_ef, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=rabi_ge)
    rabi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=rabi_ge)
    
    rabi_ef = Pulse(start=6995, duration=-pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=rabi_ef)
    rabi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=rabi_ef)
    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
    write_dir = r"C:\Data\2019\encircling\rabi"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def readout_only(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 3
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class
    off_set=2
    ## channels  
    pi_ge=34
    pi_ef=28
    ssm_ef=.092
    ssm_ge = 0.3885

    #main readout
    main_pulse = Pulse(start = 0,duration = 8000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
    write_dir = r"C:\Data\2019\encircling\rabi"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def t1(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    off_set=0
    pi_ge=34
    t1_time = 1000
    ssm_ge = 0.386

    t1_ge = Pulse(start=6995, duration= -pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=t1_ge)
    t1_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=t1_ge)

#    g_ge = Pulse(start=6997, duration=50, amplitude=0.5E-20, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=g_ge)
#    g_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=g_ge)

    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
#    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
#    
#    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
#    qubit_gate = create_gate(both_ch1_ch2)
#    the_seq.channel_list[0][1] = qubit_gate
#    the_seq.channel_list[1][1] = qubit_gate
#    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:100,6000:7000], aspect='auto', extent=[6000,7000,100,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"

    write_dir = r"C:\Data\2019\encircling\t1"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=off_set, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
#    wx_programs.wx_set_and_amplitude_and_offset()
##END geom
def ramsey(ssm_ge = 0.3885): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=17
    t1_time = 1000
#    ssm_ge = 0.3885
    t2_ge = Pulse(start=6995-pi_ge, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=t2_ge)
    t2_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=t2_ge)

    t2_ge = Pulse(start=6995, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase', start=0, stop=1800,initial_pulse=t2_ge)
    t2_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='phase', start=0, stop=1800,initial_pulse=t2_ge)
# some small pulse to open the gate
#    g_ge = Pulse(start=6997, duration=100, amplitude=0.5E-20, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=g_ge)
#    g_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=g_ge)
    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6800:7000], aspect='auto', extent=[6800,7000,200,0])
#        plt.show()
#        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\ramsey"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
    wx_programs.wx_set_and_amplitude_and_offset()

##END geom    
def t1_ef(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=28   
    t1_time = 6000
    ssm_ge = 0.3885
    ssm_ef = 0.0917

    p_pi_ge = Pulse(start=6995-pi_ef, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ge)

    t1_ef = Pulse(start=6995, duration=-pi_ef, amplitude=.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=t1_ef)
    t1_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=t1_ef)

#    g_ge = Pulse(start=6997, duration=100, amplitude=5E-20, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=g_ge)
#    g_ge.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=g_ge)

    #main readout

    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)

#    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
#    the_seq.add_sweep(channel=2, marker=1, sweep_name='none',initial_pulse=main_pulse)    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate
    the_seq.channel_list[1][1] = qubit_gate
    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:25,6000:7000], aspect='auto', extent=[6000,7000,25,0])
        plt.plot(channel2_ch[0:0,6000:7000])
        plt.show()
        
    ## write output
    write_dir = r"C:\Data\2019\encircling\t1_ef"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
#    write_dir = r"C:\Data\2019\encircling\
## 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
#  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def ramsey_ef_phase(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=28    
    t1_time = 1000
    ssm_ge = 0.3885
    ssm_ef = 0.0917
    p_pi_ge = Pulse(start=6995-pi_ef, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ge)

    t2_ef = Pulse(start=6995-pi_ef/2, duration=-pi_ef/2, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='start', start=0, stop=-t1_time,initial_pulse=t2_ef)
    t2_ef.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=t2_ef)

    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef/2, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='phase', start=0, stop=360*5 ,initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=4, sweep_name='phase', start=0, stop=360*5 ,initial_pulse=p_pi_ef_r)


    #main readout

    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
#    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
#    
#    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
#    qubit_gate = create_gate(both_ch1_ch2)
#    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\ramsey_ef"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def ramsey_ef(ssm_ef = 0.0917): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=28    
    t1_time = 1000
    ssm_ge = 0.3885
#    ssm_ef = 0.0917
    p_pi_ge = Pulse(start=6995-pi_ef, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ge)

    t2_ef = Pulse(start=6995-pi_ef/2, duration=-pi_ef/2, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=t2_ef)
    t2_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=t2_ef)

    p_pi_ge = Pulse(start=6995, duration=-pi_ef/2, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='phase', start=0, stop=1800,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='phase', start=0, stop=1800,initial_pulse=p_pi_ge)


    #main readout

    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
#    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
#    
#    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
#    qubit_gate = create_gate(both_ch1_ch2)
#    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\ramsey_ef"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def t1_hf(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=28 
    pi_hf=34
    t1_time = 4000
    ssm_ge = 0.3885
    ssm_ef = 0.0917
    ssm_hf = 0.243
    
    p_pi_ge = Pulse(start=6995-pi_ef-pi_hf-pi_ef, duration=pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ge)

    p_pi_ef = Pulse(start=6995-pi_hf-pi_ef, duration=pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=p_pi_ef)

    t1_hf = Pulse(start=6995-pi_ef, duration=pi_hf, amplitude=0.5, ssm_freq=ssm_hf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t1_time,initial_pulse=t1_hf)
    t1_hf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t1_time,initial_pulse=t1_hf)

    p_pi_ef_r = Pulse(start=6995, duration=pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none', initial_pulse=p_pi_ef_r)


    #main readout

    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\t1_hf"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
  
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def ramsey_hf(ssm_hf=.243): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=28 
    pi_hf=40
    t2_time = 1000
    ssm_ge = 0.3885
    ssm_ef = 0.0917
#    ssm_hf=.2424
    
    p_pi_ge = Pulse(start=6995-2*pi_ef-2*pi_hf, duration=-pi_ge, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t2_time,initial_pulse=p_pi_ge)
    p_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t2_time,initial_pulse=p_pi_ge)

    p_pi_ef = Pulse(start=6995-pi_hf-2*pi_ef, duration=-pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t2_time,initial_pulse=p_pi_ef)
    p_pi_ef.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t2_time,initial_pulse=p_pi_ef)

    t2_hf = Pulse(start=6995-pi_ef-pi_hf, duration=-pi_hf/2, amplitude=0.5, ssm_freq=ssm_hf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t2_time,initial_pulse=t2_hf)
    t2_hf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t2_time,initial_pulse=t2_hf)
 
    pi2_hf = Pulse(start=6995-pi_ef, duration=-pi_hf/2, amplitude=.5, ssm_freq=ssm_hf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none' , initial_pulse=pi2_hf)
    pi2_hf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none' , initial_pulse=pi2_hf)
    

    p_pi_ef_r = Pulse(start=6995, duration=-pi_ef, amplitude=0.5, ssm_freq=ssm_ef, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=p_pi_ef_r)
    p_pi_ef_r.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none', initial_pulse=p_pi_ef_r)


    #main readout

    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
#        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()

    ## write output
    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\ramsey_hf"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def ch12_leakage(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 3
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=28
    pi_hf=50
    t2_time = 7000
    ssm_ge = 0.3885
    ssm_ef = 0.1105
    ssm_hf = 0.22265
    
    p2_pi_ge = Pulse(start=7000, duration=-t2_time, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-t2_time,initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-t2_time,initial_pulse=p2_pi_ge)


    #main readout

    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\ramsey_hf"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def ch34_leakage(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 3
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels  
    pi_ge=34
    pi_ef=28 
    pi_hf=50
    t2_time = 7000
    ssm_ge = 0.3885
    ssm_ef = 0.1105
    ssm_hf = 0.22265
    
    p2_pi_ge = Pulse(start=7000, duration=-t2_time, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=3, sweep_name='start', start=0, stop=-t2_time,initial_pulse=p2_pi_ge)
    p2_pi_ge.phase = 90
    the_seq.add_sweep(channel=4,  sweep_name='start', start=0, stop=-t2_time,initial_pulse=p2_pi_ge)


    #main readout

    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=1, marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-2000, duration=1000, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\Data\2019\encircling\ramsey_hf"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.53', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

if __name__ == '__main__':
    pass

    
#    readout_only()
#    ch34_leakage()
#    calibrating_offset()
#    no_pi_pi_pipi()
#    rabi_ge_with_2pi_phase_shift()
#    rabi()
#    ramsey()
#    t1_ef()
#    rabi_ef()
#    ramsey_ef()
#    t1_hf()
#    rabi_hf()
#    ramsey_hf()
#    rabi_det()
#    es_transport()
#    es_evolution()
#    phase_meas_transport()
#    xtransport()
#    phase_meas_xf()
#    t1()
#    pi2prep()
#    loading()
#    phase_meas_no_transport()
#    ramsey_ef_phase()
#    es_drive()
#    phase_meas_esdrive()
#    phase_meas_partial_transport()
#    phase_meas_partial_transport_hf()
#    xtransport_ef()
#    es_drive_ef()
#    phase_meas_no_transport_hf()
#    phase_meas_esdrive_hf()
#    phase_meas_transport_hf()
#    phase_meas_esdrive_diff_ang()
#    unbroken_es()
#    two_level_ep()
#    es_drive_jump()
#    loading_jump()
#    wx_programs.wx_set_and_amplitude_and_offset()
    