# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:12:43 2020

@author: mange
"""

#import numpy as np 
import classPMDA_v3


# define the name of the file to read from
filename = "READ.txt"

    
# open the file for reading
f = open(filename, 'r')

Prob = classPMDA_v3.PMDAProblem(f)

    
Prob.load(f)
action=Prob.actions(Prob.State)

#print(action)
# close the pointer to that file
f.close()