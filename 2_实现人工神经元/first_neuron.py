import math

def sigmoid(h):
    y = 1 / (1 + math.exp(-h))
    return y

def activate(inputs,weights):
    #input and net input 
    h = 0
    for x,w in zip(inputs,weights):

        h += x*w
    return sigmoid(h)


if __name__ == "__main__":
    inputs = [0.5, 0.3, 0.2]
    weights = [0.4, 0.7, 0.2]
    output = activate(inputs, weights)
    print(output)