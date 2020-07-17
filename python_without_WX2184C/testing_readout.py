# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:27:24 2020

@author: Crow108
"""
import numpy as np
import matplotlib.pyplot as plt

import daq_programs
plt.style.use('ggplot')

def fun():
    num_pats = 1
    num_reps = 3000## 
    
    ([avg_rec_chA, avg_rec_chB],[readout_chA,readout_chB]) = daq_programs.run_daq2(num_pats, num_reps, verbose=False)
    
    sample_rate = 250E6
    ts_us = np.linspace(0, avg_rec_chA.size/sample_rate, avg_rec_chA.size) *1E6
    
    avg_start = 567
    avg_end = 1567
    
    print( "A std",  np.round( np.std(avg_rec_chA[avg_start:avg_end]), 4) )
    A_avg = np.round( np.mean(avg_rec_chA[avg_start:avg_end]), 2)
    B_avg = np.round( np.mean(avg_rec_chB[avg_start:avg_end]), 2) # variance is ~0.6 for 1k reps
    print(f"A:{A_avg}, B:{B_avg}")
    
    # min max gives amplitude of sine resulting from heterodyne interference.
    #print("A min/max {0:.2f}, {1:.2f}".format( np.min(avg_rec_chA[100:]-A_avg), np.max(avg_rec_chA[100:]-A_avg)))
    #print("B min/max {0:.2f}, {1:.2f}".format( np.min(avg_rec_chB[100:]-B_avg), np.max(avg_rec_chB[100:]-B_avg)))
               
    ## Find pulse starts
    avg_window = np.ones(100)/100. # a 1/M window to average M points via convolution.
    rolling_avg_A = np.convolve(avg_rec_chA-127, avg_window)
    rolling_avg_B = np.convolve(avg_rec_chB-127, avg_window)
    derivative = np.gradient( rolling_avg_A )
    print("Pulse start width [ns]", 4*np.argmin(derivative), 4*(np.argmax(derivative)-np.argmin(derivative)) )
    plt.plot(ts_us, rolling_avg_A[:-99], label='avg A')
    plt.plot(ts_us, rolling_avg_B[:-99], label='avg B')
    
    ## make plots
    #plt.plot(avg_rec_chA-127, label='A' )
    #seplt.plot(avg_rec_chB-127 , label='B')
    
    plt.legend()
    
    plt.xlabel("Time")
    plt.ylabel("Digitizer Value")
    
    return avg_rec_chA
##END fun
    
    
if __name__ == '__main__':
    xs = fun()