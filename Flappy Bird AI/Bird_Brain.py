import random
#Create the Neuron class
class Neuron:
    def __init__(self, inputs, weights, bias):
        self.weights = weights
        self.bias = bias
        self.inputs = inputs

    def weighted_sum(self, inputs):
        output = 0
        for i in range(len(inputs)):
            output += self.weights[i]*inputs[i]
        output += self.bias
        return output
    
    def sigmoid(self, x):
        return 1 / (1 + pow(2.71828, -x))
    
    #"Bipolar" activation function (1, -1)"
    def bipolar(self, x):
        if x > 0:
            return 1
        else:
            return -1

#Define the Neural Network that connects each node.
class NeuralNetwork:
    def __init__(self, nodes):
        self.nodes = nodes
    
    def create_all(self):
        for node in self.nodes:
            node.weights = [random.uniform(-3, 3) for i in range(3)]
            node.bias = random.uniform(-1, 1)
    
    def fly(self, inputs):
        activations = []
        for i in range(len(self.nodes) - 1):
            activations.append(self.nodes[i].bipolar(self.nodes[i].weighted_sum([inputs[i], (inputs[i] + 1)])))
        choice1 = self.nodes[-2].sigmoid(self.nodes[-1].weighted_sum([activations[0], activations[1]]))
        choice2 = self.nodes[-1].sigmoid(self.nodes[-1].weighted_sum([activations[1], activations[2]]))
        if choice1 > choice2:
            return 1
        else:
            return 0
    
#For network visualisation see the "Network_Diagram" PNG file.
#DESCRIPTION: 4 inputs, 3 hidden nodes (2 inputs ea), 2 output nodes (2 inputs ea).