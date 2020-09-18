""" Load any modules necessary """
import pygame
import random
import scipy.special

import numpy as np

class NeuralNetwork:
	""" A class to manage the neural network """

	def __init__(self, num_input, num_hidden, num_output):
		""" Initialize the neural network atributes """
		self.num_input = num_input
		self.num_hidden = num_hidden
		self.num_output = num_output
		self.weight_input_hidden = np.random.uniform(-0.5, 0.5, size = (self.num_hidden, self.num_input))
		self.weight_hidden_output = np.random.uniform(-0.5, 0.5, size = (self.num_output, self.num_hidden))
		self.bias_input_hidden = np.random.uniform(0, 0, size = (self.num_hidden, 1))
		self.bias_hidden_output = np.random.uniform(0, 0, size = (self.num_output, 1))
		self.activation_function = lambda x: scipy.special.expit(x)

	def get_outputs(self, input_list, verbose = False):
		""" Get the outputs """
		inputs = np.array(input_list, ndmin = 2).T 
		hidden_inputs = np.dot(self.weight_input_hidden, inputs)
		hidden_outputs = self.activation_function(hidden_inputs + self.bias_input_hidden)
		final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)
		final_outputs = self.activation_function(final_inputs + self.bias_hidden_output)
		return final_outputs

	def modify_weights(self):
		""" mutate weights """
		NeuralNetwork.modify_array(self.weight_input_hidden)
		NeuralNetwork.modify_array(self.weight_hidden_output)
		NeuralNetwork.modify_array(self.bias_input_hidden)
		NeuralNetwork.modify_array(self.bias_hidden_output)

	def create_mixed_weights(self, net1, net2):
		""" Breeding """
		self.weight_input_hidden = NeuralNetwork.get_mix_from_arrays(net1.weight_input_hidden, net2.weight_input_hidden)
		self.weight_hidden_output = NeuralNetwork.get_mix_from_arrays(net1.weight_hidden_output, net2.weight_hidden_output)
		self.bias_input_hidden = NeuralNetwork.get_mix_from_bias(net1.bias_input_hidden, net2.bias_input_hidden)
		self.bias_hidden_output = NeuralNetwork.get_mix_from_bias(net1.bias_hidden_output, net2.bias_hidden_output)

	def modify_array(a):
		""" random mutations """
		for x in np.nditer(a, op_flags=['readwrite']):
			if random.random() < 0.2:
				new_val = np.random.random_sample()*(1 - (-1)) - 1
				x[...] = new_val

	def get_mix_from_bias(b1, b2):
		""" mix parents to get children """
		total_entries = b1.size
		num_rows = b1.shape[0]

		num_to_take = total_entries - int(total_entries * 0.5)
		idx = np.random.choice(np.arange(total_entries), num_to_take, replace = False)
		res = np.random.rand(num_rows, 1)

		for row in range(0, num_rows):
			if row in idx:
				res[row] = b1[row]
			else:
				res[row] = b2[row]
		return res

	def get_mix_from_arrays(ar1, ar2):
		""" mix parents to get children """
		total_entries = ar1.size
		num_rows = ar1.shape[0]
		num_cols = ar1.shape[1]

		num_to_take = total_entries - int(total_entries * 0.5)
		idx = np.random.choice(np.arange(total_entries), num_to_take, replace = False)
		res = np.random.rand(num_rows, num_cols)

		for row in range(0, num_rows):
			for col in range(0, num_cols):
				index = row * num_cols + col
				if index in idx:
					res[row][col] = ar1[row][col]
				else:
					res[row][col] = ar2[row][col]
		return res