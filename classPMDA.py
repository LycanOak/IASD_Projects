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


            self.State = State(self.Initial_State, 0, waitingroom, self.Initial_State)
            # The last argument is the time spent by each patient with each doctor
            # At the initial state it is all zero so we can use self.Initial_State to def it.

#--------------------------------------------------------------------------------------------
    def actions(self,s):
        # s is of the class State
        actionlist = []
        p_in_wr = [] # codes of patients in waiting room
        p_in_wrP = [] # codes of patients in waiting room _PRIORITY
        doctors=[]
        aux=[]
        priTyWR = 0

        tsMD = 0
        for pp in range(np.size(self.Patients)):
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

        for spw in range(np.size(p_in_wr)):
            if (s.waiting_time_cntr[0][p_in_wr[spw]-1] + 5) > self.Labels[self.Patients[p_in_wr[spw]-1]['Label']-1]['Max_waiting_time']:
                priTyWR = 1
                p_in_wrP.append(p_in_wr[spw])
                #this patient is not on the common waiting room
                p_in_wr.pop(spw)

        if priTyWR == 1:

            if np.size(p_in_wrP) == np.size(self.Doctors):
                auxl=permutations(p_in_wrP,len(self.Doctors))
                #   A=math.factorial(len(p_in_wrP))/math.factorial(len(p_in_wrP)-len(self.Doctors))

                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],jj[j]))
                    actionlist.append(aux)
                    aux=[]

            elif  np.size(p_in_wrP) < np.size(self.Doctors):
                lp = len(p_in_wr)
                lpP = len(p_in_wrP)



                if (lp+lpP)>=len(self.Doctors):

                    auxpP = combinations(p_in_wrP,len(p_in_wrP))
                    auxp = combinations(p_in_wr, len(self.Doctors)-len(p_in_wrP))
                    auxppP = list(auxpP+auxp) #join two tupples and convert to list

                    auxl = permutations(auxppP,len(self.Doctors))
                    for jj in list(auxl):
                        for j in range(len(self.Doctors)):
                            aux.append((self.Doctors[j]['Doctor_code'],jj[j]))
                        actionlist.append(aux)
                        aux=[]

                else:
                    d = len(self.Doctors) - (lp+lpP)
                    auxpP = combinations(p_in_wrP,len(p_in_wrP))
                    auxp = combinations(p_in_wr, len(self.Doctors)-len(p_in_wrP))

                    empties = tuple(-np.ones((1,d)))
                    auxppP = list(auxpP+auxp+empties) #join two tupples and convert to list

                    auxl = permutations(auxppP,len(self.Doctors))
                    for jj in list(auxl):
                        for j in range(len(self.Doctors)):
                            aux.append((self.Doctors[j]['Doctor_code'],jj[j]))
                        actionlist.append(aux)
                        aux=[]
            else:
                self.has_sol = 0
                
        else:
            if len(p_in_wr)>=len(self.Doctors):
                auxl=permutations(p_in_wr,len(self.Doctors))
             #   A=math.factorial(len(p_in_wr))/math.factorial(len(p_in_wr)-len(self.Doctors))

                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],jj[j]))
                    actionlist.append(aux)
                    aux=[]
            else:
                #to do --- empty doctor
                d = len(self.Doctors) - len(p_in_wr)
                empties = -np.ones((1,d))
                p_in_wr.append(empties)
                auxl=permutations(p_in_wr,len(self.Doctors))
                
                
                auxl = permutations(auxppP,len(self.Doctors))
                for jj in list(auxl):
                    for j in range(len(self.Doctors)):
                        aux.append((self.Doctors[j]['Doctor_code'],jj[j]))
                    actionlist.append(aux)
                    aux=[]



        return actionlist

class State:

    def __init__(self, snow, time, waitingroom, TimeSpentMD):

        self.state = snow
        self.Time = time
        self.waiting_time_cntr = waitingroom
        self.TimeSpentMD = TimeSpentMD

