import numpy as np
import math as math
from itertools import permutations
from itertools import combinations
class PMDAProblem:

    def __init__(self, f):   # f, patients, doctors, labels
        "Associates a data file to the information of the problem"
        self.file = f
        self.solution = []  #???

    def load(self, f):

        arr1 = np.array([])

        while True:
        # read a single line
          line = f.readline()
          arr1 = np.append(arr1, line)
          if not line:
             break
        # Remove empty lines
        filtered = [x for x in arr1 if len(x.strip()) > 0]
        # Transform list to array
        filtered = np.array(filtered)

        # Create array of available doctors, labels and patients
        doctors = np.array([])
        labels = np.array([])
        patients = np.array([])

        for i in range(len(filtered)):
            if 'MD' in filtered[i]:
                doctors = np.append(doctors,filtered[i])

            elif 'PL' in filtered[i]:
                labels = np.append(labels,filtered[i])
                filtered_2 = np.delete(filtered, i)

            elif 'P' in filtered[i]:
                patients = np.append(patients,filtered[i])

            arr_doctors = np.zeros([len(doctors),2])
            for k in range(len(doctors)):
                arr = [float(i.strip()) for i in doctors[k][3:-1].split(" ")]
                arr = np.array(arr)
                arr_doctors[k,:]= arr


            arr_labels = np.zeros([len(labels),3])
            for k in range(len(labels)):
                arr = [float(i.strip()) for i in labels[k][3:-1].split(" ")]
                arr = np.array(arr)
                arr_labels[k,:]= arr

            arr_patients = np.zeros([len(patients),3])
            for k in range(len(patients)):
                arr = [float(i.strip()) for i in patients[k][2:-1].split(" ")]
                arr = np.array(arr)
                arr_patients[k,:]= arr
#
            doctors_arr = []
            for i in range(len(doctors)):
                dictionary_doctor = {"Doctor_code": int(arr_doctors[i][0]), "effi": arr_doctors[i][1]}
                doctors_arr.append(dictionary_doctor.copy())
            self.Doctors = doctors_arr

            labels_arr = []
            for i in range(len(labels)):
                dictionary_labels = {"Label_code": int(arr_labels[i][0]), "Max_waiting_time": int(arr_labels[i][1]), "Consult_time": int(arr_labels[i][2])}
                labels_arr.append(dictionary_labels.copy())
            self.Labels = labels_arr

            patients_arr = []
            for i in range(len(patients)):
                dictionary_patients = {"patient_code": int(arr_patients[i][0]), "Current_waiting_time": int(arr_patients[i][1]), "Label": int(arr_patients[i][2])}
                patients_arr.append(dictionary_patients.copy())
            self.Patients = patients_arr

            #define goal state: All consults have ended. Represented by a matrix of -1
            self.Goal_State = - np.ones((np.size(self.Doctors), np.size(self.Patients)));

            #define initial state: No consult has started yet. Represented by a matrix of 0
            self.Initial_State = np.zeros((np.size(self.Doctors), np.size(self.Patients)));

            waitingroom = np.zeros((1, np.size(self.Patients)))
            for pp in range(np.size(self.Patients)):
                waitingroom[0][pp] = self.Patients[pp]['Current_waiting_time']

            print(waitingroom[0])
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
        patients=[]
        
        
        for pp in range(np.size(self.Patients)):
            patients.append(self.Patients[pp]['patient_code'])
            # exclude patients whose consult is done
            if s.state[0][pp] != -1:
                #pick up a column for a patient
                ppp = s.state[:,pp]
                if any(ppp):

                    for i in range(np.size(s.TimeSpentMD[:,pp])):
                        tsMD = tsMD + self.Doctors[i]['effi']*s.TimeSpentMD[i,pp]

                    if not (tsMD == self.Labels[self.Patients[pp]['Label']-1]['Consult_time']):
                        p_in_wr.append(self.Patients[pp]['patient_code'])
                else:
                    p_in_wr.append(self.Patients[pp]['patient_code'])


        # search for priorities in waiting room
        print('========')
        #print(np.size(p_in_wr))
        #print(range(np.size(p_in_wr)))
        
        print(p_in_wr)
        for spw in range(0,np.size(p_in_wr)):
            print('--------')
            
            if (s.waiting_time_cntr[0][spw] + 5) > self.Labels[self.Patients[spw]['Label']-1]['Max_waiting_time']:
                
                priTyWR = 1
                p_in_wrP.append(p_in_wr[spw])
                #this patient is not on the common waiting room
                #p_in_wr.pop(spw)
        
        pmP = len(p_in_wr)-len(p_in_wrP)
        i = 0
        print('before')
        print('p_in_wr',p_in_wr)
        print('p_in_wrP',p_in_wrP)
        while len(p_in_wr) > pmP:
            ii = p_in_wr.index(p_in_wrP[i])
            p_in_wr.pop(ii)
            i = i + 1
        print('after')
        print('p_in_wr',p_in_wr)
        print('p_in_wrP',p_in_wrP)    
        
        if priTyWR == 1:

            if np.size(p_in_wrP) == np.size(self.Doctors):
                auxl=permutations(p_in_wrP,len(self.Doctors))
                #   A=math.factorial(len(p_in_wrP))/math.factorial(len(p_in_wrP)-len(self.Doctors))

                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                    actionlist.append(aux)
                    aux=[]

            elif  np.size(p_in_wrP) < np.size(self.Doctors):
                lp = len(p_in_wr)
                lpP = len(p_in_wrP)

                
                if (lp+lpP)>=len(self.Doctors):

                    auxpP = combinations(p_in_wrP,len(p_in_wrP))
                    for jj in list(auxpP):
                        comb_auxpP.append(list(jj))
                        
                    print('com_pP',comb_auxpP[0])
                    print(len(p_in_wr),'---------',len(self.Doctors)-len(p_in_wrP))
                    auxp = combinations(p_in_wr, len(self.Doctors)-len(p_in_wrP))
                    for jj in list(auxp):
                        comb_auxp.append(list(jj))
                        
                    print('com_p',comb_auxp)
                    
                    print(len(comb_auxp))
                    print(len(comb_auxpP))
                    print(len(comb_auxp[0]))
                    allc = np.empty([len(comb_auxp),len(comb_auxpP[0])+len(comb_auxp[0])])
#                    print(allc)
                    print(len(comb_auxp))
                    for i in range(0,len(comb_auxp)):
                        a = comb_auxpP[0]
                        print('a1',a)
                        print(len(a))
                        print(comb_auxp[i][0])
                        a=a+comb_auxp[i]#a.append(comb_auxp[i])
                        print('a2',a)
                        allc[i] = a
                        a.pop()
                        
#                    print('allc',allc)
#                    print(len(allc))
#                    print(allc[0])
                    for i in range(len(allc)):
                        auxxxx=permutations(allc[i])
                        for jj in list(auxxxx):
                            apppp.append(jj)
#                        apppp.append((allc[i][1],allc[i][0]))
#                        print(apppp)
                    #FROM HERE ON THERE IS STLL WORK TO BE DONE
#                    auxl = permutations(apppp,len(self.Doctors)) #change
                    for jj in list(apppp):
                        print(jj)
                        for j in range(len(self.Doctors)):
                            aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                        actionlist.append(aux)
                        aux=[]

                else:
                    d = len(self.Doctors) - (lp+lpP)
                    auxpP = combinations(p_in_wrP,len(p_in_wrP))
                    for i in list(auxpP):
                        comb_auxpP.append(list(i))
                    print('com_pP',comb_auxpP[0])
                    if len(self.Doctors)-len(p_in_wrP)>len(p_in_wr):
                        for i in range((len(self.Doctors)-len(p_in_wrP))-len(p_in_wr)):
                            p_in_wr.append(-1)
                    auxp = combinations(p_in_wr, len(self.Doctors)-len(p_in_wrP))
                    for i in list(auxp):
                        comb_auxp.append(list(i))
                        print(comb_auxp)
                    print('com_p',comb_auxp)
                    print(len(comb_auxp))
                    allc = np.empty([len(comb_auxp),len(comb_auxpP[0])+len(comb_auxp[0])])
#                    print(allc)
                    for i in range(0,len(comb_auxp)):
                        print(999999999999999)
                        a = comb_auxpP[0]
                        print('a1',a)
                        print(len(a))
                        print(comb_auxp[i][0])
                        a=a+comb_auxp[i]#a.append(comb_auxp[i][:])
                        print('a2',a)
                        allc[i] = a
                        a.pop()
                    print('alllllllll',allc)
#                    for i in range(len(allc)):
#                        apppp.append((allc[i][0],allc[i][1]))
#                        apppp.append((allc[i][1],allc[i][0]))
#                    print(auxli)
#                    auxppP=auxiliar+auxli
#                    print(auxppP)
                    
                    auxl = permutations(allc[0],len(self.Doctors))
                    for jj in list(auxl):
                        print(jj)
                        for j in range(len(self.Doctors)):
                            aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                        actionlist.append(aux)
                        aux=[]
            else:
                self.has_sol = 0
                print('INFEASABLE')
                
        else:
            if len(p_in_wr)>=len(self.Doctors):
                print(111111111111)
                auxl=permutations(p_in_wr,len(self.Doctors))
             #   A=math.factorial(len(p_in_wr))/math.factorial(len(p_in_wr)-len(self.Doctors))

                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                    actionlist.append(aux)
                    aux=[]
            else:
                #to do --- empty doctor
                d = len(self.Doctors) - len(p_in_wr)
                #print(d)
                empties = -np.ones(d)
                #print(empties)
                p_in_wr = np.concatenate([p_in_wr, empties])
                #print(p_in_wr)
                auxl=permutations(p_in_wr,len(self.Doctors))
                #print(list(auxl))
                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],int(jj[j])))
                    actionlist.append(aux)
                    aux=[]


#        print(actionlist)
        return actionlist


    def result(self,s,a):
        doctors=[]
        patients=[]
        for i in range(len(self.Doctors)):
            doctors.append(self.Doctors[i]['Doctor_code'])
        print('doo-----',doctors)
        for i in range(len(self.Patients)):
            patients.append(self.Patients[i]['patient_code'])
        print('patt----',patients)
        self.State.Time=self.State.Time+5
        for i in range(len(a)):
            j=doctors.index(a[i][0])
            if a[i][1]==-1:
                continue
            else:
                jj=patients.index(a[i][1])
            self.State.state[j][jj]=1
        self.State.TimeSpentMD=self.State.TimeSpentMD*5
        print(self.State.waiting_time_cntr)
        self.State.waiting_time_cntr=self.State.waiting_time_cntr+5
        print(self.State.waiting_time_cntr)
        for i in range(len(a)):
            j=doctors.index(a[i][0])
            self.State.waiting_time_cntr[0][j]=self.State.waiting_time_cntr[0][j]-5
        est=self.State
#        for i in range(len(self.State.state)):
#            for j in range(len(self.State.state[i])):
#                if self.State.state[i][j]==0:
#                    self.State.
        return est
    
    
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

