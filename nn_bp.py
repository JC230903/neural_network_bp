from random import random as rd, seed
from math import exp



def in_net(n_inputs,n_hidden, n_outputs):
    network=list()
    hidden_layer=[ {'weights': [0.10*rd() for i in range(n_inputs+1)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer=[ {'weights': [0.10*rd() for i in range(n_hidden+1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network


#
# network=in_net(3,2,2)
#
# #print(network)
#
# for l in network:
#     print(l)
#     print()


def activation_function(weights,inputs):
    activation=weights[-1]
    for i in range(len(weights)-1):
        activation=activation+weights[i]*inputs[i]

    return activation

# l=activation_function([0.5050456011842431, 0.6911727238501713, 0.44395220544711134],[0.16033830118244297, 0.6250418489993605])
# print (l)

def trasfer(activation):
    output=(1.0/(1.0+exp(-activation)))
    return output


def forward(network,rows):
    inputs=rows
    for layer in network:
        new_inputs=[]
        for neuron in layer:
            activate=activation_function(neuron['weights'],inputs)
            neuron['output']=trasfer(activate)
            new_inputs.append(neuron['output'])

    inputs=new_inputs

    return inputs

# network = [[{'weights': [0.13436424411240122, 0.8474337369372327, 0.763774618976614]}],
# 		[{'weights': [0.2550690257394217, 0.49543508709194095]}, {'weights': [0.4494910647887381, 0.651592972722763]}]]
# row = [1, 0, None]
# output = forward(network, row)
# print(output)

def transfer_derivative(output):
    return output*(1-output)


def back_propagation_err(network,expected):
    for i in reversed(range(len(network))):
        layer=network[i]
        errors=list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error=0.0
                for neuron in network[i+1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                    errors.append(error)

        else:
            for j in range(len(layer)):
                neuron=layer[j]
                errors.append(neuron['output']-expected[j])
        for j in range(len(layer)):
            neuron=layer[j]
            neuron['delta']=errors[j] *transfer_derivative(neuron['output'])


# network = [[{'output': 0.7105668883115941, 'weights': [0.13436424411240122, 0.8474337369372327, 0.763774618976614]}],
# 		[{'output': 0.6213859615555266, 'weights': [0.2550690257394217, 0.49543508709194095]}, {'output': 0.6573693455986976, 'weights': [0.4494910647887381, 0.651592972722763]}]]
# expected = [0, 1]
# back_propagation_err(network, expected)
# for layer in network:
# 	print(layer)


def update_weights(network,row,l_rate):

    for i in range(len(network)):
        inputs=row[:-1]
        if  i !=0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                 neuron['weights'][j] -= l_rate*neuron['delta'] * inputs[j]

        neuron['weights'][-1] -= l_rate * neuron['delta']


# Train a network for a fixed number of epochs
def train_network(network, train, l_rate, n_epoch, n_outputs):
	for epoch in range(n_epoch):
		sum_error = 0
		for row in train:
			outputs = forward(network, row)
			expected = [0 for i in range(n_outputs)]
			expected[row[-1]] = 1
			sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
			back_propagation_err(network, expected)
			update_weights(network, row, l_rate)
		print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))


#predictions
def predict(network, row):
	outputs = forward(network, row)
	return outputs.index(max(outputs))


#testing the data
seed(1)

dataset = [[2.7810836,2.550537003,0],
	[1.465489372,2.362125076,0],
	[3.396561688,4.400293529,0],
	[1.38807019,1.850220317,0],
	[3.06407232,3.005305973,0],
	[7.627531214,2.759262235,1],
	[5.332441248,2.088626775,1],
	[6.922596716,1.77106367,1],
	[8.675418651,-0.242068655,1],
	[7.673756466,3.508563011,1]]

n_inputs = len(dataset[0]) - 1
n_outputs = len(set([row[-1] for row in dataset]))
network = in_net(n_inputs, 2,n_outputs)
train_network(network, dataset, 0.5, 1000,n_outputs)
print(network)
print()

for layer in network:
	print(layer)

for row in dataset:
    prediction = predict(network, row)
    print('Expected=%d, Got=%d' % (row[-1], prediction))














