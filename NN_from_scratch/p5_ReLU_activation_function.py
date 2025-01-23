import sys
import numpy as np
import matplotlib
import nnfs
from nnfs.datasets import spiral_data

nnfs.init()

print("Python: ", sys.version)
print("Numpy: ", np.__version__)
print("Matplotlib: ", matplotlib.__version__)

'''
In this tutorial we use the package nnfs to initialize are inputs and labels. Then we implement a ReLU function that 
returns the input if the input is positive and a 0 if the input is negative. We create a layer object with 2 inputs and
5 neurons and apply the weights and biases by calling the forward method of the layer object. Then we apply the 
activation function of the neuron by passing the outputs of the layer as inputs to our ReLU object. 
'''


X, y = spiral_data(100, 3)


class ReLUActivation:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)


class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.rand(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, layer_inputs):
        self.output = np.dot(layer_inputs, self.weights) + self.biases

layer1 = LayerDense(2, 5)
activation1 = ReLUActivation()
layer1.forward(X)
print(layer1.output)
activation1.forward(layer1.output)
print(activation1.output)
