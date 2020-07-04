# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 11:18:02 2020

@author: P. M. Harrington, 27 January 2020
"""

import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import integrate
import csv
import fit_functions as fitfun

class Nop():
    pass

def readout_fnotf(p_readout):
    num_pats_each = p_readout.shape[1]//2
    
    p_readout_pi_f = p_readout.T[:num_pats_each].T
    p_readout_pi_t = p_readout.T[num_pats_each:].T
    
    p_readout_fnotf = []
    p_readout_fnotf.append(p_readout_pi_t[0])
    p_readout_fnotf.append(p_readout_pi_t[2])
    p_readout_fnotf.append(p_readout_pi_f[2])
    p_readout_fnotf = np.array(p_readout_fnotf)
    
#    pf = 0.5 + 0.5*(p_readout_fnotf[2]-p_readout_fnotf[1])/(p_readout_fnotf[2]+p_readout_fnotf[1])
#    pe = 1-pf
#    p_post_fnotf = []
#    p_post_fnotf.append(0*pf)
#    p_post_fnotf.append(pe)
#    p_post_fnotf.append(pf)
#    p_post_fnotf = np.array(p_post_fnotf)
    
    pf = p_readout_fnotf[2]/(p_readout_fnotf[2]+p_readout_fnotf[1])
    pe = 1-pf
    p_post_fnotf = []
    p_post_fnotf.append(0*pf)
    p_post_fnotf.append(pe)
    p_post_fnotf.append(pf)
    p_post_fnotf = np.array(p_post_fnotf)
    
    
    return p_readout_fnotf, p_post_fnotf

def p_readout_postselected(p_readout=[None, None, None]):
    p_readout_post = [None]*3
    
    p_e = p_readout[1]
    p_f = p_readout[2]
    p_readout_post[0] = 0*p_e
    p_readout_post[1] = p_e/(p_e+p_f)
    p_readout_post[2] = p_f/(p_e+p_f)
    
    return p_readout_post

def get_threshold_value_from_gaussians(a_vals, b_vals):
    #
    w_a = abs(a_vals[0])
    mu_a = a_vals[1]
    s_a = a_vals[2]
    #
    w_b = abs(b_vals[0])
    mu_b = b_vals[1]
    s_b = b_vals[2]
    
    #
    a = 1/(2*s_a**2) - 1/(2*s_b**2)
    b = -(mu_a/s_a**2 - mu_b/s_b**2)
    c = mu_a**2/(2*s_a**2) - mu_b**2/(2*s_b**2) + np.log(w_b/w_a)
    
    #
    x0 = -b/(2*a) - np.sqrt(b**2 - 4*a*c)/(2*a)
    x1 = -b/(2*a) + np.sqrt(b**2 - 4*a*c)/(2*a)
    
    return x0, x1
    

def fit_parabola(x_vals, y_vals, guess_vals=None):
    if guess_vals is None:
        guess_a = 1.0
        guess_b = 1.0
        guess_c = 1.0
        guess_vals = [guess_a, guess_b, guess_c]
        

    #
    fit = curve_fit(fitfun.parabola, x_vals, y_vals, p0=guess_vals)
    y_vals_fit = fitfun.parabola(x_vals, *fit[0])
    
    plt.figure(figsize=(6,4))
    plt.plot(x_vals, y_vals)
    plt.plot(x_vals, y_vals_fit)
    plt.show()
    
    print("\n")
    var_str = ['a', 'b', 'c']
    for idx, v in enumerate(var_str):
        print(v+": {}".format(fit[0][idx]))
        
    print("min (fit): {}".format(-fit[0][1]/(2*fit[0][0])))
    
    return (fit, y_vals_fit)

def fit_exp_decay(x_vals, y_vals, guess_vals=None):
    if guess_vals is None:
        guess_amplitude = -1.0
        guess_gamma = 1.0
        guess_offset = 0
        guess_vals = [guess_amplitude, guess_gamma, guess_offset]
        

    #
    popt, pcov = curve_fit(fitfun.exp_decay, x_vals, y_vals, p0=guess_vals)
    perr = np.sqrt(np.diag(pcov))
    y_vals_fit = fitfun.exp_decay(x_vals, *popt)

    plt.figure(figsize=(6,4))
    plt.plot(x_vals, y_vals)
    plt.plot(x_vals, y_vals_fit)
    plt.show()
    
    print("\n")
    var_str = ["   amp", " gamma", "offset"]
    for idx, v in enumerate(var_str):
        print(v+": {}".format(popt[idx]))
    
    return (popt, perr, y_vals_fit, pcov)

def fit_sine_decay(x_vals, y_vals, guess_vals=None):
    if guess_vals is None:
        guess_freq_Hz = 5
        guess_gamma = 5
        guess_amplitude = 0.5
        guess_phase_deg = -90
        guess_offset = 0.5
        
        guess_vals = [guess_freq_Hz, guess_gamma, guess_amplitude, guess_phase_deg, guess_offset]

    #
    popt = np.full(len(guess_vals), np.nan)
    pcov = np.full((len(guess_vals), len(guess_vals)), np.nan)
    y_vals_fit = np.full(len(x_vals), np.nan)
    try:
        popt, pcov = curve_fit(fitfun.sine_decay, x_vals, y_vals, p0=guess_vals)
        y_vals_fit = fitfun.sine_decay(x_vals, *popt)
    except RuntimeError:
        print("RuntimeError")
        
    perr = np.sqrt(np.diag(pcov))
        
    y_vals_fit = fitfun.sine_decay(x_vals, *popt)
    
    plt.figure(figsize=(6,4))
    plt.plot(x_vals, y_vals)
    plt.plot(x_vals, y_vals_fit)
    plt.show()
    
    print("\n")
    var_str = ["  freq", " gamma", "   amp", " phase", "offset"]
    for idx, v in enumerate(var_str):
        print(v+": {} +/- {}".format(popt[idx], perr[idx]))
        
    print("pi_pulse time"+": {} +/- {}".format(1/2/popt[0], perr[0]))
    return (popt, perr, y_vals_fit, pcov)
    
def fit_lorentzian(x_vals, y_vals, guess_vals=None):
    if guess_vals is None:
        guess_amplitude = -1.0
        guess_b = 1.0
        guess_offset = 0
        guess_freq = 7.3
        guess_vals = [guess_amplitude, guess_b, guess_offset, guess_freq]
        

    #
    popt, pcov = curve_fit(fitfun.lorentzian, x_vals, y_vals, p0=guess_vals)
    perr = np.sqrt(np.diag(pcov))
    y_vals_fit = fitfun.lorentzian(x_vals, *popt)

    plt.figure(figsize=(6,4))
    plt.plot(x_vals, y_vals)
    plt.plot(x_vals, y_vals_fit)
    plt.show()
    
    print("\n")
    var_str = ["   amp", " b", "offset", "  freq"]
    for idx, v in enumerate(var_str):
        print(v+": {}".format(popt[idx]))
    
    return (popt, perr, y_vals_fit, pcov)

def fit_line(x_vals, y_vals, guess_vals=None):
    if guess_vals is None:
        guess_m = -1.0
        guess_b = 1.0
        guess_vals = [guess_m, guess_b]

    #
    popt, pcov = curve_fit(fitfun.line, x_vals, y_vals, p0=guess_vals)
    perr = np.sqrt(np.diag(pcov))
    y_vals_fit = fitfun.line(x_vals, *popt)

    plt.figure(figsize=(6,4))
    plt.plot(x_vals, y_vals)
    plt.plot(x_vals, y_vals_fit)
    plt.show()
    
    print("\n")
    var_str = ["m", "b"]
    for idx, v in enumerate(var_str):
        print(v+": {}".format(popt[idx]))
    
    return (popt, perr, y_vals_fit, pcov)


def fit_readout_histogram(rec_readout, hist_bins, hist_counts, num_gaussians=3):
    w0 = max(hist_counts)/3
    w1 = max(hist_counts)/3
    w2 = max(hist_counts)/3
    s0 = 0.2*np.std(rec_readout)
    s1 = 0.2*np.std(rec_readout)
    s2 = 0.2*np.std(rec_readout)
    mu0 = -160. #np.mean(rec_readout) - 1*s0
    mu1 = -153. #np.mean(rec_readout)
    mu2 = -142. #np.mean(rec_readout) + 1*s0
#    mu0 = np.mean(rec_readout) - 0.5*s0
#    mu1 = np.mean(rec_readout)
#    mu2 = np.mean(rec_readout) + 0.5*s0
    
#    guess_vals = [w0, w2, mu0, mu2, s0, s2]
    guess_vals = [w0, w1, w2, mu0, mu1, mu2, s0, s1, s2]
    
#    #
#    fit = curve_fit(fitfun.two_gaussians, hist_bins, hist_counts, p0=guess_vals)
#    hist_fit = fitfun.two_gaussians(hist_bins, *fit[0])

    #
    fit = curve_fit(fitfun.three_gaussians, hist_bins, hist_counts, p0=guess_vals)
    hist_fit = fitfun.three_gaussians(hist_bins, *fit[0])
    
    #
    plt.figure(figsize=(6,4))
    plt.plot(hist_bins, hist_counts)
    plt.plot(hist_bins, hist_fit)
    
    ## get individual gaussians
    for k in range(num_gaussians):
        f = fitfun.gaussian(hist_bins, *fit[0][k::3])
        plt.plot(hist_bins, f)
        
        
    get_threshold_value_from_gaussians(fit[0][0::3], fit[0][1::3])
    get_threshold_value_from_gaussians(fit[0][1::3], fit[0][2::3])
    
    
    
    return fit, hist_fit
    
def fit_gaussian(rec_readout, hist_bins, hist_counts):
    w0 = max(hist_counts)
    s0 = np.std(rec_readout)
    mu0 = np.mean(rec_readout)
    
    guess_vals = [w0, mu0,s0]

    #
    fit = curve_fit(fitfun.gaussian, hist_bins, hist_counts, p0=guess_vals)
    hist_fit = fitfun.gaussian(hist_bins, *fit[0])
    
    #
    plt.figure(figsize=(6,4))
    plt.plot(hist_bins, hist_counts)
    plt.plot(hist_bins, hist_fit)
    
    ## get individual gaussians
    f = fitfun.gaussian(hist_bins, *fit[0])
    plt.plot(hist_bins, f)
    plt.show()
        
    return fit, hist_fit

def save_csv(folder_name=None, file_name=None, data_in=[]):
    # transpose data for loading into Igor
    data_to_save = np.vstack(data_in).T
    
    #
    cwd = os.getcwd()
    path_data_folder = os.path.abspath(os.path.join(cwd, os.pardir)) + "/data"
    
    if (not os.path.isdir(path_data_folder)):
            os.mkdir(path_data_folder)
    
    path_name_folder = os.path.abspath(os.path.join(cwd, os.pardir)) + "/data" + "/" + folder_name
    
    if (not os.path.isdir(path_name_folder)):
            os.mkdir(path_name_folder)
            
    time_when_saving = datetime.datetime.now()
    if file_name is not None:
        file_name = folder_name+file_name+"_{}".format(time_when_saving.strftime("%Y%m%d_%H%M%S"))
    else:
        file_name = folder_name+"_{}".format(time_when_saving.strftime("%Y%m%d_%H%M%S"))
    file_path = path_name_folder + "/" + file_name + ".txt"
    
    header = () #("N_list", "e_gnd", "e_gap")
    table = []
    for idx, d in enumerate(data_to_save):
        table.append(d)
    
    table.insert(0, header)
    
    f = open(file_path, "w", newline="")
    writer = csv.writer(f)
    writer.writerows(table)
    
if __name__ == "__main__":
    pass