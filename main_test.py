# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:12:43 2020

@author: mange
"""

#import numpy as np 
from array import array
import classPMDA


# define the name of the file to read from
filename = "READ.txt"

    
# open the file for reading
f = open(filename, 'r')

Prob = classPMDA.PMDAProblem(f)

Prob.load(f)

# close the pointer to that file
f.close()