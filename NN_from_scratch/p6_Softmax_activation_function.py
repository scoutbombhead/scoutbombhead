import sys
import numpy as np
import matplotlib
import nnfs
from nnfs.datasets import spiral_data

'''
In this part we will implement a softmax activation function and then apply it to our spiral data. In the softmax
function the inputs will be exponentiated which ensures that all values are positive. To avoid overflowing, all inputs
are subtracted by the highest input value so that the highest input will be 0 whereas all other inputs will negative. 
After exponentiation, the values are all divided by the sum of the inputs to give normalized values between 0 and 1. 
While summing, the axis=1 option is used so that the rows are added. The keepdims=True option ensures that the output
is a nx1 matrix. 
'''

nnfs.init()

print("Python: ", sys.version)
print("Numpy: ", np.__version__)
print("Matplotlib: ", matplotlib.__version__)

class ReLUActivation:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.rand(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, layer_inputs):
        self.output = np.dot(layer_inputs, self.weights) + self.biases

class SoftmaxActivation:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs))
        self.probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)

X, y = spiral_data(100, 3)

layer_1 = LayerDense(2, 3)
activation_1 = ReLUActivation()
layer_2 = LayerDense(3, 3)
activation_2 = SoftmaxActivation()

layer_1.forward(X)
activation_1.forward(layer_1.output)
layer_2.forward(activation_1.output)
activation_2.forward(layer_2.output)

print(activation_2.probabilities[5:])
