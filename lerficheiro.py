# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 11:04:43 2020

@author: a1ugu
"""

# importing numpy 
import numpy as np 
from array import array


# define the name of the file to read from
filename = "READ.txt"

arr1 = np.array([])
    
# open the file for reading
filehandle = open(filename, 'r')

while True:
    # read a single line
    line = filehandle.readline()
    arr1 = np.append(arr1, line)
    if not line:
        break
    print(arr1)

# close the pointer to that file
filehandle.close()

# Remove empty lines
filtered = [x for x in arr1 if len(x.strip()) > 0]
# Transform list to array
filtered = np.array(filtered)

# Create array of available doctors, labels and patients
doctors = np.array([])
labels = np.array([])
patients = np.array([])

# for i in range(len(filtered)):
#     if 'MD' in filtered[i]:
#         doctors = np.append(doctors,filtered[i])

#     elif 'PL' in filtered[i]:
#         labels = np.append(labels,filtered[i])
#         filtered_2 = np.delete(filtered, i)
        

#     elif 'P' in filtered[i]:
#         patients = np.append(patients,filtered[i])
        

        
#with open('READ.txt', 'r') as f:
 #   lists = [line.strip().split() for line in f]
  #  lists = np.array(lists)
    


for i in range(len(filtered)):
    if 'MD' in filtered[i]:
        doctors = np.append(doctors,filtered[i])

    elif 'PL' in filtered[i]:
        labels = np.append(labels,filtered[i])
        filtered_2 = np.delete(filtered, i)
        
    elif 'P' in filtered[i]:
        patients = np.append(patients,filtered[i])
     