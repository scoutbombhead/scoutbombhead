import sys
import numpy as np
import matplotlib

print("Python: ", sys.version)
print("Numpy: ", np.__version__)
print("Matplotlib: ", matplotlib.__version__)

'''
In this tutorial we create a neural network layer with 3 neurons and 4 inputs each. Each input has a weight assigned to 
it for each neuron and each neuron has a unique bias. Each set of weight represents the weight of the corresponding 
input for that neuron. Since we have neurons in the layer, we will have 3 sets of weights. The same goes for the biases.
To calculate the output of the neurons, we add the products of the inputs and the weights and subsequently add the 
bias. The output is an array with each value corresponding to the output of the 3 neurons.
'''

inputs = [1, 2, 3, 2.5]
weights1 = [0.2, 0.8, -0.5, 1]
weights2 = [0.5, -0.91, 0.26 , -0.5]
weights3 = [-0.26, -0.27, 0.17, 0.87]
bias1 = 2
bias2 = 3
bias3 = 0.5

output = [inputs[0] * weights1[0] + inputs[1] * weights1[1] + inputs[2] * weights1[2] + inputs[3] * weights1[3] + bias1,
          inputs[0] * weights2[0] + inputs[1] * weights2[1] + inputs[2] * weights2[2] + inputs[3] * weights2[3] + bias2,
          inputs[0] * weights3[0] + inputs[1] * weights3[1] + inputs[2] * weights3[2] + inputs[3] * weights3[3] + bias3]
print(output)

