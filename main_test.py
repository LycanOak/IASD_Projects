# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:12:43 2020

@author: mange
"""

#import numpy as np 
import classPMDA_v6 as PMDA


# define the name of the file to read from
filename = "data2.txt"
#data2
    
# open the file for reading
f = open(filename, 'r')

Prob = PMDA.PMDAProblem(f)

    
Prob.load(f)
action=Prob.actions(Prob.State)
estado=Prob.result(Prob.State,action[0])
resutss=Prob.goal_test(estado)
#print(action)
# close the pointer to that file
f.close()