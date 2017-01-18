import csv
import random
import math
import operator



""" getCSVData() read a csv file, and tranfer the data into a string list,
divide data into trainSet and testSet, with ratio assigned"""
def getCSVData(filename, ratio, trainSet = [], testSet = []):
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile) # type: csv.reader #
        dataSet = list(lines) # dataSet is list, ele in dataSet is str
        for i in range(len(dataSet) - 1):
            for j in range(len(dataSet[0]) - 1):
                dataSet[i][j] = float(dataSet[i][j]) # transfer first 4 ele from str to float
                # separate data into training and testing in ratio split
                if random.random() < ratio:  #random.random() generates num in range [0.0, 1.0)
                    trainSet.append(dataSet[i])
                else :
                    testSet.append(dataSet[i])


"""euclideanDistance() takes 2 elements and calculate the euclidean distance between them.
    len limits the calculation bits"""
def euclideanDistance(x, y, len):
    distance = 0
    for i in range(len):
        distance += math.pow(x[i] - y[i], 2)
    # print "distance:  ", math.sqrt(distance)
    return math.sqrt(distance)


"""findNeighbors() find the nearest k neighbors based on the euclidean neighbors"""
def findNeighbors(trainSet, testData, k):
    distances = []
    for i in range(len(trainSet) - 1):
        distance = euclideanDistance(testData, trainSet[i], len(testData) - 1)
        distances.append((trainSet[i], distance)) # (ele1, ele2) is type of tuple
    distances.sort(key=operator.itemgetter(1)) # compare with distance
    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0]) # neighbors is type of list
    return neighbors


def predict(neighbors):
    votes = {}  # use a dictionary to store the votes
    for i in range(len(neighbors)):
        label = neighbors[i][-1]
        if label in votes:
            votes[label] += 1
        else:
            votes[label] = 1 # init
    # dictionary is not iterable, compare the second items, not the key, sort in decrease direction
    sortedVotes = sorted(votes.iteritems(), key=operator.itemgetter(1), reverse=True) # sortedVotes is type of list
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    length = len(testSet)
    print "predict numbers: ", length
    count = 0
    incorr = 0
    for i in range(length):
        if testSet[i][-1] == predictions[i]: # should use '==' instead of 'is'
            count += 1
        else:
            print "predict: " + repr(testSet[i][-1]) + ",  actual: " + repr(predictions[i])
            incorr += 1
    print "predict correctly: ", count
    print "predict wrong: ", incorr
    accuracy = (count/float(length)) * 100.0
    print "accuracy: ", accuracy
    return accuracy


def knn_test(trainSet, testSet):
    predictions = []
    k = 3
    for i in range(len(testSet)):
        res = predict(findNeighbors(trainSet, testSet[i], k))
        predictions.append(res)
    return getAccuracy(testSet, predictions)


def main():
    trainSet = []
    testSet = []
    # get training and testing data
    getCSVData('res\iris.data', 0.67, trainSet, testSet)
    knn_test(trainSet, testSet)


main()