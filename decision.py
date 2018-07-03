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


import matplotlib.pyplot as plt
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

# plotNode - annotate the node with text passed in
# text - text to annotate
# center - center of node
# parent - parent of node
# nodetype - nodetype
#
def plotNode(text, center, parent, nodetype):
    'plot the edge and vertices'
    createPlot.ax1.annotate(text, xy=parent,  xycoords='axes fraction', xytext=center, textcoords='axes fraction', va="center", ha="center", bbox=nodetype, arrowprops=arrow_args )

# plotMidText - plot mid text with axis
# center - center of node
# parent - parent of node
# text - node text
#
def plotMidText(center, parent, text):
    'add mid text'
    
    # 中间位置坐标
    xMid = (parent[0]-center[0])/2.0 + center[0]
    yMid = (parent[1]-center[1])/2.0 + center[1]
    
    createPlot.ax1.text(xMid, yMid, text, va="center", ha="center", rotation=30)

# plotTree - plot the tree recursively
# myTree - my decision tree
# text - text to annotate 
#
def plotTree(myTree, parent, text):
    'plot decision tree'
    
    # get num of leaves
    count = numLeaves(myTree)
    firstStr = myTree.keys()[0]
    center = (plotTree.x + (1.0 + float(count))/2.0/plotTree.width, plotTree.y)
    
    # 绘制当前节点到子树节点(含子树节点)的信息
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    
    # 获取子树信息
    secondDict = myTree[firstStr]
    # 开始绘制子树，纵坐标-1。        
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
      
    for key in secondDict.keys():
        # plot subtree recursion
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        # plot leave node directly
        else:
            plotTree.x = plotTree.x + 1.0/plotTree.width
            plotNode(secondDict[key], (plotTree.x, plotTree.y), center, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
     
    # finish plot subtree, increment y axis
    plotTree.y = plotTree.y + 1.0/plotTree.depth

# createPlot - show the decision tree
# myTree: my decision tree
# 
def createPlot(myTree):
    'show decision tree'
    # configure plot
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    
    plotTree.width = float(numLeaves(myTree))
    plotTree.depth = float(getDepth(myTree))
    
    # get the axis
    plotTree.x = -0.5/plotTree.width; 
    plotTree.y = 1.0;
    
    # plot decision tree
    plotTree(myTree, (0.5,1.0), '')
    plt.show()

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


