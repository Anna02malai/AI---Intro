import math

def sigmoid(z): #Sigmoid Function
    return 1/(1+math.exp(-1.0*z))

def perceptron_fnc(input_data): #Perceptron Function
    w = [0.0, 0.0]         #initalizing the Weights to 0

    for iteration in range(100):
        for data in input_data:                   
            data = data.strip('()').split(',')   #Input formating

            x1, x2, y = int(data[0]), int(data[1]), int(data[2])  
            y_pred = 1 if ((w[0] * x1) + (w[1] * x2)) >= 0 else -1    #Perceptron Logic prediction

            if y_pred != y:               #Checking pred = original classification
                y = -1.0 * y_pred
                w[0] += y * x1            #Updating the Weights
                w[1] += y * x2

    return w

def logistic_fnc(input_data):       #logistic regression Function

    w = [0.0, 0.0]                # Intializing weights to 0
    alpha = 0.1                   # Setting up the learning rate

    for iteration in range(100):
        for data in input_data:
            data = data.strip('()').split(',')         #input Formating

            x1, x2, y = int(data[0]), int(data[1]), (int(data[2])/2)+0.5    # Assigning data and Normalizing it for the classes
            z = (w[0] * x1) + (w[1] * x2)          #Calculating the Weighted sum
  
            g_z = sigmoid(z)            #Plugging ithe sum to the sigmoid function

            w[0] += alpha * ((y-g_z)* x1)    #Updating the weights respectively
            w[1] += alpha * ((y-g_z)* x2)  

    return w

def main():
        
    inp = input("Enter Input: ")
    output_type, input_data  = inp[0],inp[2:]     #Input parsing and formating
    input_data = input_data.replace(" ",'')
    input_data = input_data.replace(")",') ').split()

    if output_type == "P":                        # Printing the output for Perceptron Input
        weights = perceptron_fnc(input_data)  
        print(f'{weights[0]}, {weights[1]}')

    elif output_type == "L":                      # Printing the output for Logistic Regression
        weights = logistic_fnc(input_data)
        for data in input_data:
            data = data.strip('()').split(',')
            x1, x2, y = int(data[0]), int(data[1]), int(data[2])   #Input formatting

            z = (weights[0] * x1) + (weights[1] * x2)      #Calculating the Weighted Sum
            probability = sigmoid(z)                       #Passing the sum to Sigmoid Function
            print(f'{round(probability,2)}', end=' ')      #printing the probabilities as per required format

    else:
        print("Enter a valid Input")

if __name__ == '__main__':
   main()