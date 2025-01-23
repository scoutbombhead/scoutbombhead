import sys
import numpy as np
import matplotlib

print("Python: ", sys.version)
print("Numpy: ", np.__version__)
print("Matplotlib: ", matplotlib.__version__)

'''
In this tutorial we implement a feed-forward neural network with 2 layers. X represents the batch of inputs. We have 4
features per input and 3 samples of inputs. We use a batch of inputs for efficiency. Then we create a dense layer class.
Dense layer means fully connected layer in which each neuron in a layer is connected to every other neuron in the 
next layer. For the init function, we take the number of inputs and the number of neurons as input parameter. Then we 
initialize the weights with random values and the biases and outputs with zeroes. After that we define a function for 
the forward pass, that we pass the parameter inputs for that layer. THe outputs are calculated by computing the dot 
product of the inputs and weights ahd adding the biases. Then first we create the first layer with 4 inputs because
we have 4 features per sample. The number of neurons can be chosen arbitrarily. The second layer has to have 5 inputs
because we have 5 outputs from the first layer. Then we call the forward method of the first layer and pass the 3 
batches of inputs to it which calculates the output. Then we forward the outputs of the first layer into the second 
layer and print the outputs. 
'''

X = [[1, 2, 3, 2.5],
     [2, 5, -1, 2],
     [-1.5, 2.7, 3.3, -0.8]]


class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.rand(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
        self.outputs = np.zeros(n_inputs)

    def forward(self, layer_inputs):
        self.outputs = np.dot(layer_inputs, self.weights) + self.biases
        return self.outputs


layer1 = LayerDense(4, 5)
layer2 = LayerDense(5, 4)
layer1.forward(X)
print(layer1.outputs)
layer2.forward(layer1.outputs)
print(layer2.outputs)
