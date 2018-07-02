# Decision Tree
# created by Jul 2

# entropy - use dataSet to calculate shannon Entropy
# math formula H = sum(-(p*(log2(p))))
# dataSet - data
#
def entropy(dataSet):
	'calculate Shannon Entropy'
	# num of entries
	numEntries = len(dataSet)
	# num of label
	numLabel = {}

	for featVec in dataSet:
		# add to label set
		current = featVec[-1]
		if current not in numLabel.keys(): numLabel[current] = 0
		numLabel[current] += 1

	# return shannonEntropy
	from math import log
	shannonEnt = 0.0
	for key in numLabel:
		prob = float(numLabel[key])/numEntries
		shannonEnt -= prob * log(prob, 2)

	return shannonEnt

# splitDataSet - extract your featurized vector and append to result
# dataSet - training dataSet
# axis - num of featurizer columns
# value - split value
#
def splitDataSet(dataSet, axis, value):
	'split dataSet'
	result = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			result.append(reducedFeatVec)

	return result

# optimize - choose a best feature to split and return the feature
# dataSet - data
#
def optimize(dataSet):
	'choose the best split'
	numFeatures = len(dataSet[0]) - 1
	# entropy of original dataSet
	baseEntropy = entropy(dataSet)
	bestInfoGain = 0.0
	#best entropy's feature
	bestFeature = -1

	for i in range(numFeatures):
		# get all feature for example
		featList = [example[i] for example in dataSet]
		# unique our feature
		uniqueVals = set(featList)
		
		# calculate new best entropy 
		newEntropy = 0.0
		for value in uniqueVals:
			# extract feature vector
			subDataSet = splitDataSet(dataSet, i , value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob * entropy(subDataSet)

		# store best entropy feature
		infoGain = baseEntropy - newEntropy
		if (infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i

		return bestFeature

# priority - choose a best label by priority vote
# classList - list of labels
def priority(classList):
	'get best label by priority vote'
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys(): classCount[vote] = 0
		classCount[vote] += 1
		sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)

	return sortedClassCount[0][0]

# createTree - create the decision tree with recurison
# dataSet - data
# labels - labels
#
def createTree(dataSet, labels):
	'create decision tree'

	# get classList
	classList = [example[-1] for example in dataSet]

	# if all classifers are the same, return the tree
	if classList.count(classList[0]) == len(classList):
		return classList[0]

	# if all feature ares classified
	if len(dataSet[0]) == 1:
		# return as a single class
		return priority(classList)

	# choose best Feature and label
	bestFeat = optimize(dataSet)
	bestFeatLabel = labels[bestFeat]

	myTree = {bestFeatLabel:{}}
	# delete elements that are classified
	del(labels[bestFeat])

	# get best feature value and store the unique
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)

	for value in uniqueVals:
		# store all labels and pass to next recursion
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)

	return myTree

# numLeaves - cacluate the num of leaves in the tree with recursion
# myTree - my decision tree
#
def numLeaves(myTree):
	'calculate the number of leaves'
	count = 0
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]

	for key in secondDict.keys():
		# recursively return the num of leaves
		if type(secondDict[key]).__name__=='dict':
			count += numLeaves(secondDict[key])
		else: 
			count += 1
	return count

# getDepth - calculate the depth of decision tree
# myTree - my decision tree
#
def getDepth(myTree):
	'calculate the depth of decision tree'
	maxDepth = 0
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]

	for key in secondDict.keys():
		if type(secondDict[key]).__name__=='dict':
			thisDepth = 1 + getDepth(secondDict[key])
		else:
			thisDepth = 1

		if thisDepth > maxDepth: maxDepth = thisDepth

	return maxDepth




# createDataSet - create a test dataSet
def createDataSet():
	'create testing dataSet'

	dataSet = [[1, 1, 'yes'],
			   [1, 1, 'yes'],
			   [1, 0, 'no'],
			   [0, 1, 'no'],
			   [0, 1, 'no']]
	labels = ['computer science', 'machine learning']

	return dataSet, labels

# test - test shannon entropy with test dataSet
def test():
	'test'
	myDataSet, labels = createDataSet()
	print (optimize(myDataSet))
	print (entropy(myDataSet))
	myTree = createTree(myDataSet, labels)
	print (myTree)
	print (numLeaves(myTree))
	print (getDepth(myTree))

# main
if __name__ == "__main__":
	test()


