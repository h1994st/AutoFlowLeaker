#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-15 17:07:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.model_selection import GridSearchCV

with open('data/nlp/training/all_out.csv', 'r') as fp:
    fp.readline()
    training_data = np.loadtxt(fp, delimiter=',', usecols=(0, 1, 2, 3, 4, 5))

# with open('data/nlp/testing/testing0_no_nan.csv', 'r') as fp:
#     fp.readline()
#     testing_date = np.loadtxt(fp, delimiter=',', usecols=(0, 1, 2, 3, 4, 5))

# clf = OneClassSVM(verbose=True)
# print 'Training...'
# clf.fit(training_data[:10000])
# print 'Testing...'
# pred = clf.predict(testing_date)
# print len(pred)
# n_error = pred[pred == -1].size
# print pred[pred == 1].size, n_error, float(pred[pred == 1].size) / 1000


def score_func(estimator, X):
    pred = estimator.predict(X)
    return float(pred[pred == 1].size) / X.size


grid = GridSearchCV(OneClassSVM(), {
    'gamma': [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7],
    'nu': [0.5, 0.6, 0.7, 0.8, 0.9, 1]
}, cv=4, scoring=score_func, verbose=100, n_jobs=4)
grid.fit(training_data[:10000])

print grid.best_params_, grid.best_score_
print grid.cv_results_
