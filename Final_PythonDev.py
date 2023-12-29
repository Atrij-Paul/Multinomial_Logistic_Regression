import numpy as np
import time

def calc_probabilities(params , data):
   try:
      independent = []  #List for varibale coefficients
      constants = []    #List for constants

      #Segregating the constants and the variable coefficients from the params dictionary
      for key in params:
        if ('C' in str(key)):
           constants.append(params[key])
        else:
           independent.append(params[key])
    
      #Checking the count of varible coefficients with that of the Independent Variables
      if ((len(independent) + 1) != len(list(data.keys()))):
        raise ValueError(f"Independent variable count mismatch with coefficients {key}")
      
      f_data = []   #Storing the independent variables other than Sero
      l_data = []   #Storing the Sero data or the last variable
      
      #Size or length of the values in the data
      size = len(data[list((data.keys()))[0]])
      
      for key in data:
         if("Sero" in str(key)):
             if (len(data[key]) != size):
                 raise ValueError(f"Dimension mismatch for independent variable {key}")
             l_data.append(data[key])
         else:
            if (len(data[key]) != size):
                raise ValueError(f"Dimension mismatch for independent variable {key}")
            f_data.append(data[key])
      l_data.append(data['Sero'])
      
      f_data = np.array(f_data)
      l_data = np.array(l_data)
      independent = np.array(independent)
      constants = np.array(constants)
      
      result = []
      for i in range(len(f_data)):
         #Dot product , vectorisation to make the process fast
         result.append(constants[i] + np.dot(independent , f_data))
      
      #Last Sero variable len(constants) - 1
      result.append(constants[len(constants) - 1] + np.dot(independent , l_data))
      
      #Converting the list to a numpy array for greater functionality
      result_array = np.array(result)
      
      #Taking the exponential
      result_expo = np.exp(result_array)
      
      total = np.sum(result_expo , axis = 0)
      
      #Calculating the probailities by diving the total from each element
      probs = result_expo / total
      
      #Entering the probabilities in the dictionary 
      final_result = {f'p{i+1}' : probs[i] for i in range(len(probs))}
      
      return final_result  #Returning the probabilities of each datapoint
    
   #Error Handling  
   except Exception as e:
        return f"Error: {str(e)}"   

f = True  #Loop Controller
data = {}  #Data dictionary
param = {}  #Parameter dictionary

#Counter Variable
c = 1

while f:
    #Cautionary instructions to the users to avoid Exceptions
    if(c > 1):
        print("The number of data points must be equal to the previous entry")
    
    #Accepting the Independent Variables
    print("Enter the key value pairs")
    key = input("Enter the Independent variable ")
    values_str = input("Enter values (comma-seperated) : ")
    values_list = [float(item.strip()) for item in values_str.split(',')]
    data[key] = values_list
                   
    #Accepting the independent coefficients and the constants for each Independent Variable 
    print("Enter the constant coefficient for the independent variable ")
    print("Enter the constant as C ")
    
    key_param_c = input("Enter the Constant Key ") + str(c)
    value_c = float(input("Enter the value "))
    
    param[key_param_c] = value_c
                   
    #Giving the user to go on entering independent variables
    choice = input('''Enter "YES" or "yes" if you want to continue choosing or enter "NO" or "no" if you want to discontinue''')
    if("Yes" in choice or "YES" in choice or "yes" in choice):
                   f = True
    else:
                   f = False
    c = c + 1

#Accepting the Variable Coefficients
count = len(list(param.keys()))
for i in range(count):
    print("Enter the variable coefficients")
    key_param = input("Enter the Variable Coefficient Key as B") + str(i)
    value = float(input("Enter the value "))
    
    param[key_param] = value

#Adding the last independent variable
length = len(data[list(data.keys())[0]])
data["Sero"] = [0 for i in range (length)]

print("Enter the constant coefficient for Sero")
key_param = input("Enter the constant coefficient Key as ") + str(length)
value = float(input("Enter the value "))
param[key_param] = value

#For calculating the time 
begin = time.time()
#Getting a dictionary of Probabilities
probablities = calc_probabilities(param , data)
end = time.time()

print(probablities)

print(f"Operation time is {end - begin}")