# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 07:23:40 2020

@author: crow104
"""

def foo():
    for k in range(4):
        print(k)
        
        try:
            raise RuntimeError
        except RuntimeError:
            print("RuntimeError")
            print('a')
            continue
            print('b')
            return
        finally:
            print("finally")
            