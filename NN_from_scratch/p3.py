import sys
import numpy as np
import matplotlib

print("Python: ", sys.version)
print("Numpy: ", np.__version__)
print("Matplotlib: ", matplotlib.__version__)

inputs = [1, 2, 3, 2.5]
weights1 = [0.2, 0.8, -0.5, 1]
weights2 = [0.5, -0.91, 0.26, -0.5]
weights3 = [-0.26, -0.27, 0.17, 0.87]
weights = [[0.2, 0.8, -0.5, 1],
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]
biases = [2, 3,  0.5]

output = np.dot(weights, inputs) + biases
print(output)
