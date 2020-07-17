# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:04:16 2020

@author: J. Monroe
"""
import numpy as np
import pyvisa
# manual: https://www.thinksrs.com/downloads/pdfs/manuals/DG535m.pdf

## constants
# see table in manual p13, RHS column.
# 0 corresponds to trigger input
T0 = 1
A  = 2
B  = 3
AB = 4 # also !AB ??
# !AB = 4
C  = 5
D  = 6
CD = 7

## open the resource. The handle will stay here.


def initialize_dg535():
    rm = pyvisa.ResourceManager()
    dg_handle = rm.open_resource('GPIB0::15::INSTR' )
    
    dg_handle.write("CL")

    ## trigger one at a time.
    dg_handle.write("TM 0") # trigger mode to internal (0)
    dg_handle.write("TR 0, 10e3") # 10 kHz trigger rate
    
    ## prep all outputs for variable signaling
    #  allows variable amplitudes.
    dg_handle.write(f"OM {T0}, 3")
    dg_handle.write(f"OM {A}, 3") # 3 is VARiable mode
    dg_handle.write(f"OM {B}, 3")
    dg_handle.write(f"OM {AB}, 3")
    dg_handle.write(f"OM {C}, 3")
    dg_handle.write(f"OM {D}, 3") 
    dg_handle.write(f"OM {CD}, 3") 
    
    ## set channel impedences to 50 Ohms
    dg_handle.write(f"TZ {AB}, 0") # 0 is 50 Ohms, 1 is 'high Z'.
    dg_handle.write(f"TZ {CD}, 0")
    dg_handle.write(f"TZ {T0}, 0")
#    
#    ## turn output off while setting commands
    dg_handle.write(f"OO {T0}, -0.1") # start with Output Offset set to -0.1 V.
    dg_handle.write(f"OA {T0}, 0.1") # Output Amplitude to 0.1 V.
    
    ## channel offsets
    # ensure these are set to zero (offset is tuned with DC supply)
    dg_handle.write(f"OO {CD}, 0") # cavity
    dg_handle.write(f"OO {AB}, 0") # qubit
    
    ## set delays
    # apparently, if any channel has not been given a delay then the joint
    #   channels (eg CD) won't generate pulses. (Have not checked directly.)
    dg_handle.write(F"DT {A},{T0}, 0")
    dg_handle.write(F"DT {B},{A}, 0") # no idea why this must be set for CD to pulse
    dg_handle.write(F"DT {C},{T0}, 0")
    dg_handle.write(F"DT {D},{C}, 0")
    
    output = dg_handle.query("ES")
    dg_handle.close()
    
    return output
##END initialize_dg535
    

def set_state(on_flag):
    rm = pyvisa.ResourceManager()
    dg_handle = rm.open_resource('GPIB0::15::INSTR' )
    
    if on_flag:
        dg_handle.write(f"OA {T0}, 3")
        # testing on 07/10/20 showed alazar triggered consistently with 1.5 V.
        # this used with 5% trigger level ( "135" daq_alazar line 95)
        dg_handle.write(f"OO {T0}, 0")
    else:
        dg_handle.write(f"OO {T0}, -0.1")
        dg_handle.write(f"OA {T0}, 0.1")
        
    ## check for errors
    output = dg_handle.query("ES")
    dg_handle.close()
    return output
##END start_dg535


def always_on_seq(flag_qubit=1):
    
    rm = pyvisa.ResourceManager()
    dg_handle = rm.open_resource('GPIB0::15::INSTR' )
    
    seq_len_s = 100E-6 # 10 kHz rep rate --> 100 us.
    
    ## amplitudes
    # NOTE: 0.1 is minimum value; returns error "4" =0B0100 = bit 2 = value outside range
    # NOTE: 0.01 is increment.
    '''
    cavity_amp_V = amp_V
    qubit_amp_V = amp_V
    '''
    if flag_qubit:
        cavity_amp_V = 1.5 # units: volts
        qubit_amp_V  = 0.5 # units: volts
        print("qubit on")
    else:
        cavity_amp_V = 1.5
        qubit_amp_V = 0.1
        print("qubit off")

    ## cavity on
    dg_handle.write(f"DT {C}, {T0}, {0.01}E-6")
    dg_handle.write(f"DT {D}, {C}, {seq_len_s-3E-6}") 
    dg_handle.write(f"OA {CD}, {cavity_amp_V}") 
#    dg_handle.write(f"DT {B}, {A}, 97.85E-6")
    # good numbers 97,97.8, 97.85
    # bad numbers: 97.9, 98

    ## qubit pulse
    dg_handle.write(f"DT {A}, {T0}, {0.1}E-6")
    dg_handle.write(f"DT {B}, {A}, {seq_len_s-3E-6}")
    dg_handle.write(f"OA {AB}, {qubit_amp_V}")
    
    ## check for errors
    output =  dg_handle.query("ES")
    dg_handle.close()
    
    return output
##END always_on

    
def single_pulse(flag_qubit_on=0):
    
    ## setup VISA session
    rm = pyvisa.ResourceManager()
    dg_handle = rm.open_resource('GPIB0::15::INSTR' )
    
    ## amplitudes
    # NOTE: 0.1 is minimum value; returns error "4" =0B0100 = bit 2 = value outside range
    # NOTE: 0.01 is increment.
    if flag_qubit_on:
        cavity_amp_V = 1.5 # units: volts
        qubit_amp_V  = 0.5 # units: volts
        print("qubit pulse on")
    else:
        cavity_amp_V = 1.5
        qubit_amp_V = 0.1
        print("qubit pulse off")

    ## cavity pulse
    start_us = 2
    dur_us = 2
    dg_handle.write(f"DT {C}, {T0}, {start_us*1E-6}")
    dg_handle.write(f"DT {D}, {C}, {dur_us*1E-6}") 
    dg_handle.write(f"OA {CD}, {cavity_amp_V}") 

    ## qubit pulse
    dg_handle.write(f"DT {A}, {T0}, {0.01*1E-6}")
    dg_handle.write(f"DT {B}, {A}, {97E-6}")
    dg_handle.write(f"OA {AB}, {qubit_amp_V}")
    
    ## check for errors
    output =  dg_handle.query("ES")
    dg_handle.close()
    
    return output
##END single_pulse


def rabi_seq(dg_handle, step_num, total_steps=51):
    rabi_time_us = 0.200  
    
    ## cavity pulse
    cavity_pulse_dur_us = 2
    cavity_pulse_start_us = 2
    dg_handle.write(f"DT {C}, {T0}, {cavity_pulse_start_us}E-6")
    dg_handle.write(f"DT {D}, {C}, {cavity_pulse_dur_us}E-6")
    #dg_handle.write(f"OA {CD}, 1.5") # amplitude set to 1 V.
    
    ## qubit pulse
    pulse_length_us = np.round( step_num/total_steps* rabi_time_us, 3)
    pulse_start_us = cavity_pulse_start_us - pulse_length_us  - 10E-3
    dg_handle.write(f"DT {A}, {T0}, {pulse_start_us}E-6")  # T0 to A delay is 1 us.
    dg_handle.write(f"DT {B}, {A}, {pulse_length_us}E-6" ) # A to B delay is step's rabi length
    
    dg_handle.write(f"OA {AB}, 1") # amplitude set to 1 V
    
    ## beginnning of seqeunce: turn from -0.1 V to +1V.
    ## enable output on A, B
    
    return dg_handle.query("ES")
##END rabi_seq