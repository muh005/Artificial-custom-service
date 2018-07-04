import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
import numpy as np
import time
import argparse
stemmer = LancasterStemmer()

training_data = []

# createDataSet - create a dataset for training
training_data.append({"class":"greeting", "sentence":"how are you"})
training_data.append({"class":"greeting", "sentence":"how is your day?"})
training_data.append({"class":"greeting", "sentence":"good day"})
training_data.append({"class":"greeting", "sentence":"how is it going today?"})

training_data.append({"class":"goodbye", "sentence":"have a nice day"})
training_data.append({"class":"goodbye", "sentence":"see you later"})
training_data.append({"class":"goodbye", "sentence":"have a nice day"})
training_data.append({"class":"goodbye", "sentence":"talk to you soon"})

training_data.append({"class":"sandwich", "sentence":"make me a sandwich"})
training_data.append({"class":"sandwich", "sentence":"can you make a sandwich?"})
training_data.append({"class":"sandwich", "sentence":"having a sandwich today?"})
training_data.append({"class":"sandwich", "sentence":"what's for lunch?"})
print ("%s sentences in training data" % len(training_data))

# preprocess - tokenize each word, remove duplicates, to lower case 
words = []
classes = []
documents = []
ignore_words = ['?']

for pattern in training_data:
	#tokenize each word in the sentence and append to word list
	w = nltk.word_tokenize(pattern['sentence'])
	words.extend(w)
	documents.append((w, pattern['class']))
	if pattern['class'] not in classes:
		classes.append(pattern['class'])

# remove the duplicate and toLowerCase
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))
classes = list(set(classes))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "words", words)

training = []
output = []
output_empty = [0] * len(classes)

for doc in documents:
	# list of tokenized words for the pattern
	bag = []
	pattern_words = doc[0]
	# stem each word
	pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
	for w in words:
		if w in pattern_words:
			bag.append(1)
		else:
			bag.append(0)
	training.append(bag)
	output_row = list(output_empty)
	output_row[classes.index(doc[1])] = 1
	output.append(output_row)
i = 0
w = documents[i][0]
print([stemmer.stem(word.lower()) for word in w])
print(training[i])
print(output[i])

# sigmoid - compute sigmoid nonlinearity
# x - parameter
# math formula 1/(1+exp(-x))
#
def sigmoid(x):
	return (1/(1+np.exp(-x)))

# derive_sigmoid - convert output of sigmoid to its derivative
# x - parameter
# math formula x*(1-x)
def derive_sigmoid(x):
	return (x*(1-x))

# clean - tokenize pattern and stem each word
# sentence
#
def clean(sentence):
	# tokenize the pattern
	sentence_words = nltk.word_tokenize(sentence)
	# stem word
	sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
	return sentence_words

# vectorize - vectorize the words by their tokens
# sentence - sentence to process
# words - to vectorize
#
def vectorize(sentence, words):
	# tokenize the pattern
	sentence_words = clean(sentence)
	# bag of words
	bag = [0]*len(words)
	for s in sentence_words:
		for i, w in enumerate(words):
			if w == s:
				bag[i] = 1
	return (np.array(bag))

# think - three layer process
# sentence - sentence to process
#
def think(sentence):
	x = vectorize(sentence.lower(), words)
	# input layer (l0) is words
	l0 = x
	# hidden layer (l1) is matrix multiplication
	l1 = sigmoid(np.dot(l0, synapse_0))
	# output layer
	l2 = sigmoid(np.dot(l1, synapse_1))
	return l2

# train - train our neural net with training data
# achieve our goal by minimize the error
# X - training data
# y - output
# hidden_neurons - to compose neural net, default to 10
# alpha - gradient descent, default to 1
# epochs - training epochs, default to 50000
# dropout - dropout, default to False
# dropout_rate - dropout_rate, default to 0.5
#
def train(X, y, hidden_neurons= 10, alpha=1, epochs = 50000, dropout = False, dropout_rate = 0.5):
	print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_rate if dropout else ''))
	print ("Input matrix: %sx%s Output matrix: %sx%s" % (len(X),len(X[0]),1, len(classes)))
	np.random.seed(1)
	last_mean_error = 1
    # randomly initialize our weights with mean 0
	synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons))-1
	synapse_1 = 2*np.random.random((hidden_neurons,len(classes)))-1

	prev_synapse_0_weight = np.zeros_like(synapse_0)
	prev_synapse_1_weight = np.zeros_like(synapse_1)

	synapse_0_direction_count = np.zeros_like(synapse_0)
	synapse_1_direction_count = np.zeros_like(synapse_1)

	for j in iter(range(epochs+1)):
    	# think through layer 0, 1, 2
		layer_0 = X
		layer_1 = sigmoid(np.dot(layer_0, synapse_0))

		if(dropout):
			layer_1 *= np.random.binomial([np.ones((len(X),hidden_neurons))],1-dropout_rate)[0] * (1.0/(1-dropout_rate))

		layer_2 = sigmoid(np.dot(layer_1, synapse_1))

		# miss the target value
		layer_2_error = y - layer_2

		if(j % 10000) == 0 and j > 5000:
			if np.mean(np.abs(layer_2_error)) < last_mean_error:
				print("delta after " + str(j) + " iterations: " + str(np.mean(np.abs(layer_2_error))))
				last_mean_error = np.mean(np.abs(layer_2_error))
			else:
				print("break: ", np.mean(np.abs(layer_2_error)), " > ", last_mean_error)
				break

		# check the direction of target layer 2
		layer_2_delta = layer_2_error * derive_sigmoid(layer_2)
		# layer 1 error contributes to layer 2 error
		layer_1_error = layer_2_delta.dot(synapse_1.T)

		# check the direction of target layer 1
		layer_1_delta = layer_1_error * derive_sigmoid(layer_1)
	
		synapse_1_weight = (layer_1.T.dot(layer_2_delta))
		synapse_0_weight = (layer_0.T.dot(layer_1_delta))

		if(j > 0):
			synapse_0_direction_count += np.abs(((synapse_0_weight > 0) + 0) - ((prev_synapse_0_weight > 0) + 0))
			synapse_1_direction_count += np.abs(((synapse_1_weight > 0) + 0) - ((prev_synapse_1_weight > 0) + 0))
		
		# use alpha as parameters of gradient descent
		synapse_1 += alpha * synapse_1_weight
		synapse_0 += alpha * synapse_0_weight

		prev_synapse_0_weight = synapse_0_weight
		prev_synapse_1_weight = synapse_1_weight

	now = datetime.datetime.now()

	# presist synapse
	synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
           	   'datetime': now.strftime("%Y-%m-%d %H:%M"),
               'words': words,
               'classes': classes
	     	   }
	synapse_file = "synapses.json"

	with open(synapse_file, 'w') as outfile:
		json.dump(synapse, outfile, indent = 4, sort_keys = True)
	print("saved synapses to: ", synapse_file) 

X = np.array(training)
y = np.array(output)

start_time = time.time()
train(X, y, hidden_neurons = 20, alpha = 0.1, epochs=100000, dropout=False, dropout_rate=0.2)
elapsed_time = time.time() - start_time
print("processing time:", elapsed_time, "seconds")


# probability threshold
ERROR_THRESHOLD = 0.2
# load our calculated synapse values
synapse_file = 'synapses.json'

with open(synapse_file) as data_file:
	synapse = json.load(data_file)
	synapse_0 = np.asarray(synapse['synapse0'])
	synapse_1 = np.asarray(synapse['synapse1'])

# classify - classify the sentence into class
# sentence - to classify
#
def classify(sentence):
	
	results = think(sentence)
	results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
	results.sort(key = lambda x: x[1], reverse = True)
	return_results = [[classes[r[0]], r[1]] for r in results]
	print ("%s \n classification: %s" % (sentence, return_results))
	return return_results

classify("make me a sandwich")
classify("how are you today?")
classify("talk to you tomorrow")
classify("who are you")
classify("make me some food")
classify("how was your lunch today")
classify("good day")






























