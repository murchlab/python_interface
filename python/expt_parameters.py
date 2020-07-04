# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 13:00:39 2020

@author: P. M. Harrington, 06 March 2020
"""
import numpy as np
from Nop_class import Nop

def expt_parameters(expt_name=None):
    if expt_name is None:
        expt = Nop("expt")
    else:
        expt = Nop(expt_name)
    
    expt.device = get_device_parameters()
    expt.awg_pulses = get_expt_cal()
    expt.pattern_parameters = get_pattern_parameters()
    
    return expt

def get_device_parameters():    
    #
    device = Nop("device")    
    
    #
    freq = Nop("transition_frequencies")
    freq.carrier = 5.3201
    freq.ge = 5.7075
    freq.ef = 5.41185

    #
    device.freq = freq
    
    return device

def get_expt_cal():
    # define pulse parameters
    
    # get device transition frequencies
    device = get_device_parameters()
    freq = device.freq
    
    #    
    ssm = Nop("single_sideband_modulation")
    ssm.ge = np.round(freq.ge - freq.carrier, decimals=6) #+0.20035
    ssm.ef = np.round(freq.ef - freq.carrier, decimals=6) #-0.095
    ssm.hf = None
    

    pi_time = Nop("pi_pulse_time")
    pi_time.ge = 20
    pi_time.ef = 24
    
    pi_amp = Nop("pi_pulse_amplitude")
    pi_amp.ge = 0.80
    pi_amp.ef = 0.64
    
    channel_pair = Nop("pulse_channel_pair")
    channel_pair.ge = "ch3ch4"
    channel_pair.ef = "ch3ch4"
    
    #
    expt_cal = Nop("awg_pulses")
    expt_cal.ssm = ssm
    expt_cal.pi_time = pi_time
    expt_cal.pi_amp = pi_amp
    expt_cal.channel_pair = channel_pair

    return expt_cal

def get_pattern_parameters():
    pat = Nop("pattern_parameters")
    pat.pat_length = 8000
    
    # readout
    pat.readout_duration = 1000
    pat.readout_start = pat.pat_length - pat.readout_duration
    pat.readout_amplitude = 1
    
    # readout trigger
    pat.readout_trig_start = pat.readout_start - 1000
    pat.readout_trig_duration = 1000
    
    #
    pat.final_pulse_end = pat.readout_start - 5
    
    return pat

def get_daq_parameters():
    daq_params = Nop("daq_parameters")
    
    #        
    daq_params.iq_angle_deg = -45
    daq_params.threshold = [145, 157.86] #[146.9, 157.86]
    
    # note: daq_alazar sets the clock to 250 MS/s
    daq_params.readout_start = 348 #1100
    daq_params.readout_duration = 120 #1000
    
    return daq_params

def get_instrument_address(instrument_name):
    if instrument_name=='wx':
        return '128.252.134.53'
    
if __name__=="__main__":
    pass