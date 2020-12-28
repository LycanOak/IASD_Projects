# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 14:16:23 2020

@author: Pedro Palmeiro
"""

import probability

class MDProblem:
    def __init__(self,fh):
        diseases=[]
        symp=[]
        tests=[]
        exams=[]
        for line in fh:
            words=line.split()
            if words[0]=='D':
                diseases=words
                diseases.pop(0)
            elif words[0]=='S':
                symp.append({'sympthom':words[1],'diseases':words[2:]})
            elif words[0]=='E':
                tests.append({'exam':words[1],'disease':words[2],'TPR':words[3],'FPR':words[4]})
            elif words[0]=='M':
                for i in range(1,len(words),2):
                    exams.append({'exam':words[i],'result':words[i+1]})
            elif words[0]=='P':
                pro=words[1]
            else:
                continue
        print(diseases)
        print(symp)
        print(tests)
        print(exams)
        print(pro)
        
        
        
        
        
    def solve(self):
        
        
        
        
        
        
        
        return(disease,likelihood)