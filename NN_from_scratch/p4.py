import sys
import numpy as np
import matplotlib

print("Python: ", sys.version)
print("Numpy: ", np.__version__)
print("Matplotlib: ", matplotlib.__version__)

X = [[1, 2, 3, 2.5],
          [2, 5, 1, 2],
          [-1.5, 2.7, 3.3, 0.8]]


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
