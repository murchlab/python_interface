#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:41:39 2019

@author: crow104

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import fileinput
import json
import importlib.util
import ntpath


def main():
    for line in fileinput.input():
        data = json.loads(line)
        print(data)
        module_path = data['module']
        _, module_name = ntpath.split(module_path)
        module_name = module_name.rstrip('.py')
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        eval_str = 'module.' + data['function'] + '('
        first_arg = True
        for argument in data['arguments']:
            arg = argument['0']
            val = argument['1']
            print((arg, val))
            if not first_arg:
                eval_str += ', '
            else:
                first_arg = False
            if arg:
                eval_str += arg + '='
            eval_str += str(val)
        eval_str += ')'
        eval(eval_str)
        print(eval_str)
    
##END main
    
if __name__ == '__main__':
    main()

