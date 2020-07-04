# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:58:35 2020

@author: P. M. Harrington
"""

import numpy as np

def parabola(x, a, b, c):
    return a*x**2 + b*x + c

def exp_decay(x, amplitude, gamma, offset):
    return amplitude*np.exp(-gamma*x) + offset 

def sine_decay(time, freq_Hz, gamma, amplitude, phase_deg, offset):
#    phase_deg = 90. # fix the phase
    return amplitude*np.exp(-gamma*time)*np.sin(time*2*np.pi*freq_Hz + 
                           np.pi*phase_deg/180) + offset
                           
def gaussian(x_in, w0, mu0, s0):
    g0 = 1/np.sqrt(2*np.pi*s0**2)*np.exp(-(x_in-mu0)**2/(2*s0**2))
    
    return abs(w0)*g0

def two_gaussians(x_in, w0, w1, mu0, mu1, s0, s1):
    g0 = 1/np.sqrt(2*np.pi*s0**2)*np.exp(-(x_in-mu0)**2/(2*s0**2))
    g1 = 1/np.sqrt(2*np.pi*s1**2)*np.exp(-(x_in-mu1)**2/(2*s1**2))
    
    return abs(w0)*g0 + abs(w1)*g1

def three_gaussians(x_in, w0, w1, w2, mu0, mu1, mu2, s0, s1, s2):
    g0 = 1/np.sqrt(2*np.pi*s0**2)*np.exp(-(x_in-mu0)**2/(2*s0**2))
    g1 = 1/np.sqrt(2*np.pi*s1**2)*np.exp(-(x_in-mu1)**2/(2*s1**2))
    g2 = 1/np.sqrt(2*np.pi*s2**2)*np.exp(-(x_in-mu2)**2/(2*s2**2))
    
    return abs(w0)*g0 + abs(w1)*g1 + abs(w2)*g2

def lorentzian(x_in, amp, b, offset, freq):
    return amp/(b+(x_in-freq)**2) + offset

def line(x_in, m, b):
    return m*x_in+b

if __name__=="__main__":
    pass