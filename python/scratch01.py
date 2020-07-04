# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:26:49 2020

@author: crow104
"""

import numpy as np
import matplotlib.pyplot as plt
import daq_programs
import daq_alazar
import wx_programs
from Nop_class import Nop

if __name__=="__main__":
    num_patterns=3
    num_records_per_pattern=3
    # get parameters: number of patterns, etc.
    daq_params = daq_programs.get_daq_parameters(num_patterns=num_patterns, 
                                    num_records_per_pattern=num_records_per_pattern)
    alazar_params = daq_programs.get_alazar_parameters(daq_params=daq_params)
    
    alazar_params.post_trigger_samples = 2048
    
    print("\nSetup Alazar configuration")
    board = ats.Board(systemId = 1, boardId = 1)
    daq_alazar.configure_board(alazar_params, board)
    
    # setup wx to start at first pattern
    print("Initialize WX")
    wx_programs.wx_initialize()
    
    #
    print("Acquire data\n")
    (rec_avg_all, rec_readout, rec_all_raw) = acquire_data(daq_params, alazar_params, board)
    
#    plt.figure()
#    plt.plot(rec_all_raw[0].T)
#    plt.show()
    
    plt.figure()
    plt.plot(rec_all_raw[1].T)
    plt.show()
    
    
    times = np.linspace(0,alazar_params.post_trigger_samples*4*1e-3, alazar_params.post_trigger_samples)
    for r in rec_all_raw[1]:
        plt.figure()    
        plt.plot(times, r)
        plt.ylim([0, 255])
        plt.show()