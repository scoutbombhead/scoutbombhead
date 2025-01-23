import numpy as np
import math

'''
In this section we will calculate the categorical cross entropy loss for our predictions. The predictions which are 
given as probabilities will be multiplied with the one-hot-encoded vector in which only the index of the correct class
has 1 and the rest of the values are 0. The result will then be added together and the natural logarithm of the sum will
be calculated, the negative of which will be our loss.
'''

softmax_output = [0.7, 0.1, 0.2]
target_output = [1, 0, 0]

loss = -(math.log(softmax_output[0]) * target_output[0] +
         math.log(softmax_output[1]) * target_output[1] +
         math.log(softmax_output[2]) * target_output[2])

print(loss)

'''
In case of a batch of outputs for which we have the target classes and  the loss needs to be computed, we first get a 
list of confidences by indexing the output array according to the list of class targets. This is done by creating a list
of all the indexes of the rows of the output array, and indexing it at the index of the target class.
'''

softmax_outputs = np.array([[0.7, 0.1, 0.2],
                            [0.1, 0.5, 0.4],
                            [0.02, 0.9, 0.08]])

class_targets_sparse = [0, 1, 1]
list_of_confidences = softmax_outputs[range(len(softmax_outputs)), class_targets_sparse]
print(list_of_confidences)
neg_log = -np.log(list_of_confidences)
print(neg_log)
average_loss = np.mean(neg_log)
print(average_loss)

'''
If we have a batch of outputs and the one-hot-encoded vectors of the true classifications we also want the calculation
to work. We check the target values if they are sparse or one-hot-encoded by checking their dimensions. Then we do the 
corresponding calculation
'''

class_targets_ohe = np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 1, 0]])

list_of_confidences = np.sum(softmax_outputs*class_targets_ohe, axis=1)
neg_log = -np.log(list_of_confidences)
print(neg_log)
average_loss = np.mean(neg_log)
print(average_loss)

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

loss_function = CategoricalCrossEntropy()
loss = loss_function.calculate(softmax_outputs, class_targets_ohe)
print(loss)

