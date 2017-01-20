from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import math
import random


# fix random seed for reproducibility
# seed = 7
# np.random.seed(seed)


def loadData(filename, split):
    train_in = []
    train_out = []
    test_in = []
    test_out = []

    dataSet = np.loadtxt(filename, delimiter=",")

    # split into input (X) and output (Y),
    for i in range(len(dataSet)):
        if random.random() < split:
            train_in.append(dataSet[i, 0:8])
            train_out.append(dataSet[i, 8])
        else:
            test_in.append(dataSet[i, 0:8])
            test_out.append(dataSet[i, 8])

    print "train in: " + str(len(train_in)) + "  train_out : " + str(len(train_out))
    print "test in: " + str(len(test_in)) + "  test_out : " + str(len(test_out))
    # convert list to np.array, for the sake of processing
    return np.array(train_in), np.array(train_out), np.array(test_in), np.array(test_out)


def get_model(inputs, outputs, test_in, test_out):
    # model is defined as layer of sequence, so create a Sequential model and add on layer at a time.
    # fully connected layers are defined using the Dense class
    # first layers has 12 neurons, 8 are inputs; and second layers has 8 neurons, last layer has one as output.
    model = Sequential()
    model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
    model.add(Dense(8, init='uniform', activation='relu'))
    model.add(Dense(1, init='uniform', activation='sigmoid'))

    # compile the model
    # 'adam' is an efficient gradient descent algorithm to optimize
    model.compile(loss = 'binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit model
    # iterate 150 times, and 10 dataset as a group.
    # input and output should be type of np.array, can't be list, as it is array[array[], array[], array[]....]
    model.fit(inputs, outputs, nb_epoch=150, batch_size=10) # happens on CPU/GPU

    # evaluate the model
    scores = model.evaluate(inputs, outputs)

    # make a prediction
    predictions = model.predict(test_in)
    predictions = [round(ele) for ele in predictions] # after round, it's type of float

    # calculate accuracy
    correct = 0
    for i in range(len(test_out)):
        # print "predic: " + str(predictions[i]) + "  real: " + str(outputs[i])
        if (predictions[i]==test_out[i]):
            correct += 1
    accuracy = correct/float(len(test_out)) * 100.0 # remember to make len() to float, otherwise the result is 0.
    print "\n"+"accuracy", accuracy


def main():
    train_in, train_out, test_in, test_out = loadData("res\pima-indians-diabetes.csv", 0.80)
    get_model(train_in, train_out, test_in, test_out)


main()
