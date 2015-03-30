""" Exploring learning curves for classification of handwritten digits """

import matplotlib.pyplot as plt
import numpy
from sklearn.datasets import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

data = load_digits()
# print data.DESCR
num_trials = 50
train_percentages = range(5,95,5)
test_accuracies = numpy.zeros(len(train_percentages))
Train_accuracy = []

for i in range(num_trials):
	test_accuracies_onetrial = []
	for train_size in train_percentages:
		X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, train_size=train_size/100.)
		model = LogisticRegression(C=10**-10)
		model.fit(X_train, y_train)
		Train_accuracy.append(model.score(X_train,y_train))
		test_accuracies_onetrial.append(model.score(X_test,y_test))
	test_accuracies = [a+b for a,b in zip (test_accuracies, test_accuracies_onetrial)]
test_accuracies_average = [x / num_trials for x in test_accuracies]

fig = plt.figure()
plt.plot(train_percentages, test_accuracies)
plt.xlabel('Percentage of Data Used for Training')
plt.ylabel('Accuracy on Test Set')
plt.show()