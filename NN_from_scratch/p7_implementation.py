import sys
import numpy as np
import matplotlib
import nnfs
from nnfs.datasets import spiral_data

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
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities

# Common loss class
class Loss:
    # Calculates the data and regularization losses
    # given model output and ground truth values
    def calculate(self, output, y):
        # Calculate sample losses
        sample_losses = self.forward(output, y)
        # Calculate mean loss
        data_loss = np.mean(sample_losses)
        return data_loss

class CategoricalCrossEntropy(Loss):
    def forward(self, y_pred, y_true):
        # Clip data to prevent division by 0
        # Clip both sides to not drag mean towards any value
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)
        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[range(len(y_pred)), y_true]
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(y_pred_clipped*y_true, axis=1)
        #Losses
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods

X, y = spiral_data(100, 3)

layer_1 = LayerDense(2, 3)
activation_1 = ReLUActivation()
layer_2 = LayerDense(3, 3)
activation_2 = SoftmaxActivation()
loss_function = CategoricalCrossEntropy()

layer_1.forward(X)
activation_1.forward(layer_1.output)
layer_2.forward(activation_1.output)
activation_2.forward(layer_2.output)

print(activation_2.output[:5])

loss = loss_function.calculate(activation_2.output, y)
print(loss)