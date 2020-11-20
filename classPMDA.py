import numpy as np
import math as math
from itertools import permutations
from itertools import combinations
class PMDAProblem:

    def __init__(self, f):   # f, patients, doctors, labels
        "Associates a data file to the information of the problem"
        self.file = f
        self.solution = []  #???
        
        self.Doctors = []
        self.Labels = []
        self.Patients = []
        
        self.Goal_State = []
        self.Initial_State = []
        

    def load(self, f):

        arr1 = []

        while True:
        # read a single line
          line = f.readline()
          arr1.append(line)
          if not line:
             break
        # Remove empty lines
        filtered = [x for x in arr1 if len(x.strip()) > 0]



        # Create array of available doctors, labels and patients
        doctors = []
        labels = []
        patients = []
        mds = []
        pls = []
        ps = []
        
        print(filtered)
        for i in range(len(filtered)):
            if 'MD' in filtered[i]:
                doctors.append(filtered[i])
                mds.append(filtered[i].split(" ")) # returns ['MD', '0001', '1']
                print(mds)
            elif 'PL' in filtered[i]:
                labels.append(filtered[i])
                pls.append(filtered[i].split(" ")) # returns ['PL', '01', '10', '15']
                print(pls)

            elif 'P' in filtered[i]:
                patients.append(filtered[i])
                ps.append(filtered[i].split(" ")) #returns ['P', '001', '5', '01']
                print(ps)
                                
            doctors_arr = []
            for i in range(len(mds)):
                dictionary_doctor = {"Doctor_code": int(mds[i][1]), "effi": float(mds[i][2])}
                doctors_arr.append(dictionary_doctor.copy())
            self.Doctors = doctors_arr

            labels_arr = []
            for i in range(len(labels)):
                dictionary_labels = {"Label_code": int(pls[i][1]), "Max_waiting_time": int(pls[i][2]), "Consult_time": int(pls[i][3])}
                labels_arr.append(dictionary_labels.copy())
            self.Labels = labels_arr

            patients_arr = []
            for i in range(len(patients)):
                dictionary_patients = {"patient_code": int(ps[i][1]), "Current_waiting_time": int(ps[i][2]), "Label": int(ps[i][3])}
                patients_arr.append(dictionary_patients.copy())           
            self.Patients = patients_arr

            #define goal state: All consults have ended. Represented by a matrix of -1    
            for d in range(len(self.Doctors)):
                for p in range(len(self.Patients)):
                    self.Goal_State.append(-1)
                    self.Initial_State.append(0)
                                
            waitingroom = []
            for pp in range(len(self.Patients)):
                waitingroom.append(self.Patients[pp]['Current_waiting_time'])


            self.State = State(self.Initial_State, 0, waitingroom, self.Initial_State)
            # The last argument is the time spent by each patient with each doctor
            # At the initial state it is all zero so we can use self.Initial_State to def it.

#--------------------------------------------------------------------------------------------
    def actions(self,s):
        # s is of the class State
        actionlist = []
        p_in_wr = [] # codes of patients in waiting room
        p_in_wrP = [] # codes of patients in waiting room _PRIORITY
        aux=[]
        priTyWR = 0
        apppp=[]
        tsMD = 0
        allc = []
        comb_auxpP = []
        comb_auxp = []
        patients = []
        
        
        for pp in range(len(self.Patients)):
            patients.append(self.Patients[pp]['patient_code'])
            # exclude patients whose consult is done
            if s.state[pp + 0*len(self.Patients)] != -1:
                #pick up a column for a patient
                ppp = []
                for d in range(len(self.Doctors)):
                    ppp.append(s.state[pp+d*len(self.Doctors)])
                
                if any(ppp):

                    for i in range(len(self.Doctors)):
                        tsMD = tsMD + self.Doctors[i]['effi']*s.TimeSpentMD[pp+i*len(self.Patients)]

                    if not (tsMD == self.Labels[self.Patients[pp]['Label']-1]['Consult_time']):
                        p_in_wr.append(self.Patients[pp]['patient_code'])
                else:
                    p_in_wr.append(self.Patients[pp]['patient_code'])


        # search for priorities in waiting room
        for spw in range(0,len(p_in_wr)):

            if (s.waiting_time_cntr[spw] + 5) > self.Labels[self.Patients[spw]['Label']-1]['Max_waiting_time']:
                
                priTyWR = 1
                p_in_wrP.append(p_in_wr[spw])

        
        pmP = len(p_in_wr)-len(p_in_wrP)
        i = 0
        while len(p_in_wr) > pmP:
            ii = p_in_wr.index(p_in_wrP[i])
            p_in_wr.pop(ii)
            i = i + 1   
        
        print('p_in_wr at beg', p_in_wr)
        print('p_in_wrP at beg', p_in_wrP)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        if priTyWR == 1:
            print('there is a priority')

            if len(p_in_wrP) == len(self.Doctors):
                print('p_in_wrP == Doctors')
                auxl=permutations(p_in_wrP,len(self.Doctors))

                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                    actionlist.append(aux)
                    aux=[]

            elif len(p_in_wrP) < len(self.Doctors):
                print('p_in_wrP < Doctors')
                lp = len(p_in_wr)
                lpP = len(p_in_wrP)

                
                if (lp+lpP)>=len(self.Doctors):
                    print('p_in_wrP + p_in_wrP >= Doctors')

                    auxpP = combinations(p_in_wrP,len(p_in_wrP))
                    for jj in list(auxpP):
                        comb_auxpP.append(list(jj))
                        
                    auxp = combinations(p_in_wr, len(self.Doctors)-len(p_in_wrP))
                    for jj in list(auxp):
                        comb_auxp.append(list(jj))
                        
                    allc = np.empty([len(comb_auxp),len(comb_auxpP[0])+len(comb_auxp[0])])

                    for i in range(0,len(comb_auxp)):
                        a = comb_auxpP[0]

                        a=a+comb_auxp[i]#a.append(comb_auxp[i])
                        allc[i] = a
                        a.pop()
                        

                    for i in range(len(allc)):
                        auxxxx=permutations(allc[i])
                        for jj in list(auxxxx):
                            apppp.append(jj)
#                        apppp.append((allc[i][1],allc[i][0]))
#                        print(apppp)

#                    auxl = permutations(apppp,len(self.Doctors)) #change
                    for jj in list(apppp):
                        for j in range(len(self.Doctors)):
                            aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                        actionlist.append(aux)
                        aux=[]

                else:
                    print('p_in_wrP + p_in_wrP < Doctors')
                    d = len(self.Doctors) - (lp+lpP)
                    auxpP = combinations(p_in_wrP,len(p_in_wrP))
                    for i in list(auxpP):
                        comb_auxpP.append(list(i))

                    if len(self.Doctors)-len(p_in_wrP)>len(p_in_wr):
                        for i in range((len(self.Doctors)-len(p_in_wrP))-len(p_in_wr)):
                            p_in_wr.append(-1)
                    auxp = combinations(p_in_wr, len(self.Doctors)-len(p_in_wrP))
                    for i in list(auxp):
                        comb_auxp.append(list(i))

                    allc = np.empty([len(comb_auxp),len(comb_auxpP[0])+len(comb_auxp[0])])
#                    print(allc)
                    for i in range(0,len(comb_auxp)):

                        a = comb_auxpP[0]

                        a=a+comb_auxp[i]#a.append(comb_auxp[i][:])

                        allc[i] = a
                        a.pop()

#                    for i in range(len(allc)):
#                        apppp.append((allc[i][0],allc[i][1]))
#                        apppp.append((allc[i][1],allc[i][0]))
#                    print(auxli)
#                    auxppP=auxiliar+auxli
#                    print(auxppP)
                    
                    auxl = permutations(allc[0],len(self.Doctors))
                    for jj in list(auxl):

                        for j in range(len(self.Doctors)):
                            aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                        actionlist.append(aux)
                        aux=[]
            else:
                self.has_sol = 0
                print('INFEASABLE')
                
        else:
            print('No priority')
            if len(p_in_wr)>=len(self.Doctors):
                print('p_in_wr >= Doctors')

                auxl=permutations(p_in_wr,len(self.Doctors))
             #   A=math.factorial(len(p_in_wr))/math.factorial(len(p_in_wr)-len(self.Doctors))

                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                    actionlist.append(aux)
                    aux=[]
            else:
                print('p_in_wr < Doctors')
                
                d = len(self.Doctors) - len(p_in_wr)
                for dd in range(d):
                    p_in_wr.append(-1)
                
                auxl=permutations(p_in_wr,len(self.Doctors))
                
                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                    actionlist.append(aux)
                    aux=[]


#        print(actionlist)
        return actionlist


    def result(self, s, a):
        
        print('RESULT()')
        snew = State(s.state, s.Time, s.waiting_time_cntr, s.TimeSpentMD)
        
        snew.Time = snew.Time + 5
        print('enter for i')
        for i in range(len(self.Patients)):
            print('i',i)
            print('snew.waiting_time_cntr\n',snew.waiting_time_cntr)
            if snew.state[i+ 0*len(self.Doctors)] != -1:
                sss = []
                for t in range(len(self.Doctors)):
                    sss.append(s.state[i+t*len(self.Doctors)])                      

                if any(sss):
                    
                    # update the time of the last consults
                    for j in range(len(self.Doctors)):
                        if snew.state[i+j*len(self.Patients)] == 1:
                            snew.TimeSpentMD[i+j*len(self.Patients)] += 5                    
                    
                    auxcnt = 0
                    for k in range(len(self.Doctors)):
                        auxcnt = auxcnt + snew.TimeSpentMD[i+k*len(self.Patients)]*self.Doctors[k]['effi']
                        
                    if auxcnt >= self.Labels[self.Patients[i]['Label']-1]['Consult_time']:
                        # the patient has ended his consult
                        for kk in range(len(self.Doctors)):
                            snew.state[i+kk*len(self.Patients)] = -1
                    else:
                        #by default set all entries to zero. to be changed afterwards
                        snew.state[i+j*len(self.Patients)] = 0
                else:
                    #patient was not in colncult in the last 5 minutes
                    snew.waiting_time_cntr[i] += 5
                
        # apply actions    
        print('a',a)
        print('snew.state\n',snew.state)
        print('enter for actions')
        for aa in range(len(a)):
            print('aa',aa)
            if a[aa][1] == -1:
                print('hi')
                continue
            else:
                snew.state[(a[aa][1]-1)+(a[aa][0]-1)*len(self.Patients)] = 1
                print('snew.state\n',snew.state)
                                  
        return snew
    
    
    def goal_test(self,s):
        if s.state.all()==-1:
            return True
        else:
            return False
        

class State:

    def __init__(self, snow, time, waitingroom, TimeSpentMD):

        self.state = snow
        self.Time = time
        self.waiting_time_cntr = waitingroom
        self.TimeSpentMD = TimeSpentMD

