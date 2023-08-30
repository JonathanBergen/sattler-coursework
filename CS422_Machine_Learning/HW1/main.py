def compute_output(w, x):
    z = 0.0

    for i in range(len(w)):
        z += x[i] * w[i]  # Compute sum of weighted inputs

    if z < 0:  # Apply sign function
        return -1
    else:
        return 1


print(compute_output([1, 2, 3], [1, 2, 3]))

import random


def show_learning(w):
    print("w0 =", '%5.2f' % w[0], ', w1 =', '%5.2f' % w[1], ', w2 =', '%5.2f' % w[2])


random.seed(7)  # To make repeatable
LEARNING_RATE = 0.1
index_list = [0, 1, 2, 3]  # Used to randomize order

# Define training examples.
x_train = [(1.0, -1.0, -1.0), (1.0, -1.0, 1.0),
           (1.0, 1.0, -1.0), (1.0, 1.0, 1.0)]  # Inputs
y_train = [1.0, 1.0, 1.0, -1.0]  # Output (ground truth)

# Define perceptron weights.
w = [0.2, -0.6, 0.25]  # Initialize to some “random” numbers

# Print initial weights.
show_learning(w)
