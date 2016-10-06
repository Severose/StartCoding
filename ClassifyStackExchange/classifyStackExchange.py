import string
import re

# Constants
punctuation = string.punctuation
digits = string.digits
topics = {'gis':0, 'security':1, 'photo':2, 'mathematica':3, 'unix':4, 'wordpress':5, 'scifi':6, 'electronics':7, 'android':8, 'apple':9}

def readdata( dataset,train ):
	# Remove "title" words from each dataset
	if train :
		string = dataset.find("topic")
		dataset = dataset[:string] + " " + dataset[string+5:]
	string = dataset.find("question")
	dataset = dataset[:string] + " " + dataset[string+8:]
	string = dataset.find("excerpt")
	dataset = dataset[:string] + " " + dataset[string+7:]

	# Remove string formatting characters
	while dataset.find("\\n") >= 0:
		string = dataset.find("\\n")
		dataset = dataset[:string] + " " + dataset[string+2:]
	while dataset.find("\\r") >= 0:
		string = dataset.find("\\r")
		dataset = dataset[:string] + " " + dataset[string+2:]
	while dataset.find("\\x") >= 0:
		string = dataset.find("\\x")
		dataset = dataset[:string] + " " + dataset[string+2:]

	# Special treatment for special characters (instances of this/that and contractions)
	while dataset.find("/") >= 0:
		string = dataset.find("/")
		dataset = dataset[:string] + " " + dataset[string+1:]
	while dataset.find("\'") >= 0:
		string = dataset.find("\'")
		dataset = dataset[:string] + " " + dataset[string+1:]

	# Remove all but alphabet characters and separate the words
	regex = re.compile('[^a-zA-Z]')
	dataset = regex.sub(' ', dataset)
	dataset = ''.join([char.lower() for char in dataset if not char in (punctuation or digits)]).split()

	# For training data
	if train:
		# Get the current training set's topic ID and remove the topic word from the list
		topic = topics[dataset[0]]
		dataset = dataset[1:]

		# Populate classify matrix with training data
		for word in dataset:
			if (len(word) > 3) and (word in classify[topic]):
				classify[topic][word] = classify[topic][word] + 1
			elif len(word) > 3:
				classify[topic][word] = 1
				unique[topic] = unique[topic] + 1
			total[topic] = total[topic] + 1

	# For input data
	else:
		for word in dataset:
			for i in range(10):
				if (len(word) > 3) and (word in prob[i]):
					probabilities[i] = probabilities[i] + prob[i][word]
		print max(probabilities)
		print probabilities

# Open training file
filein = open('training.json', 'r')
first = True
train = True
trainingData = []
classify = []
total = []
unique = []
prob = []


# Initialize the classify matrix
for i in range(10):
	classify.append({})
	total.append(0)
	unique.append(0)
	prob.append({})

# Read training data from file
for dataset in filein:
	# Read the amount of training data in the file (first line)
	if first:
		trainingCount = dataset
		first = False

	else :
		readdata(dataset,train)

# We have the "trained" matrix
#TODO: Implement "learning" function
#print(classify[0])
for i in range(10):
	for key, value in classify[i].iteritems():
		prob[i][key] = (classify[i][key] + 1.0)/(total[i] + unique[i])

#(<Specific Word Count> + 1) / ( <Total Words in Topic> + <Unique Words in Topic> )
filein.close()

first = True
train = False
guess = ""
probabilities = []

# Initialize the matrices
for i in range(10):
	probabilities.append(0)
	total.append(0)
	unique.append(0)
	prob.append({})

inputCount = int(raw_input())

# Read input data from file
for i in range(inputCount) :
	dataset = raw_input()
	readdata(dataset, train)