import numpy as np
class PMDAProblem:
  
    def __init__(self, f):   # f, patients, doctors, labels
        "Associates a data file to the information of the problem"
        self.file = f
        #self.Patients = patients
        #self.Doctors = doctors
        #self.Labels = labels
      #  self.init_state = []
        #can we build classes (or subclasses) here? or just make structs
        
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
                dictionary_doctor = {"Doctor_code": arr_doctors[i][0], "effi": arr_doctors[i][1]}
                doctors_arr.append(dictionary_doctor.copy())
            self.Doctors = doctors_arr
            
            labels_arr = []
            for i in range(len(labels)):
                dictionary_labels = {"Label_code": arr_labels[i][0], "Max_waiting_time": arr_labels[i][1], "Consult_time": arr_labels[i][2]}
                labels_arr.append(dictionary_labels.copy())
            self.Labels = labels_arr
            
            patients_arr = []
            for i in range(len(patients)):
                dictionary_patients = {"patient_code": arr_patients[i][0], "Current_waiting_time": arr_patients[i][1], "Consult_time": arr_patients[i][2]}
                patients_arr.append(dictionary_patients.copy())
            self.Patients = patients_arr