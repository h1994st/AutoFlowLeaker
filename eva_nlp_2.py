#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-15 17:07:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import time

import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib

# with open('data/nlp/training/all_out_filter.csv', 'r') as fp:
#     fp.readline()
#     training_data = np.loadtxt(fp, delimiter=',', usecols=(0, 1, 2, 3, 4, 5))

# with open('data/nlp/training/brown_result_filter.csv', 'r') as fp:
#     fp.readline()
#     training_data = np.loadtxt(fp, delimiter=',', usecols=(0, 1, 2, 3, 4, 5))

with open('data/nlp/training/wiki_result_filter.csv', 'r') as fp:
    fp.readline()
    training_data = np.loadtxt(fp, delimiter=',', usecols=(0, 1, 2, 3, 4, 5))

with open('data/nlp/testing/testing-news-digest-0-result_filter.csv', 'r') as fp:
    fp.readline()
    testing_data = np.loadtxt(fp, delimiter=',', usecols=(0, 1, 2, 3, 4, 5))

with open('data/nlp/testing/testing_non_nl_filter.csv', 'r') as fp:
    fp.readline()
    outlier_data = np.loadtxt(fp, delimiter=',', usecols=(0, 1, 2, 3, 4, 5))

# nu = 0.1
# gamma = 1e-5
# kernel = 'rbf'
# clf = OneClassSVM(nu=nu, gamma=gamma, kernel=kernel, verbose=True)
# print 'Training...'
# clf.fit(training_data[:150000])
# print 'Save model'
# joblib.dump(
#     clf, 'data/nlp/one-class-svm-%s-%f-%f-%d.pkl' % (
#         kernel, nu, gamma, int(time.time())))
# # print 'Training on testing data...'
# # clf.fit(testing_data)
# # print 'Save model'
# # joblib.dump(
# #     clf, 'data/nlp/one-class-svm-%f-%f-%d.pkl' % (nu, gamma, int(time.time())))

clf = joblib.load('data/nlp/one-class-svm-rbf-0.100000-0.000010-1484900502.pkl')

print 'Testing...'
print 'Predict training data...'
pred_train = clf.predict(training_data[:150000])
n_error_train = pred_train[pred_train == -1].size
print 'error train: %f' % (float(n_error_train) / len(pred_train))
print 'Predict training data...'
pred_train = clf.predict(training_data[150000:])
n_error_train = pred_train[pred_train == -1].size
print 'error train: %f' % (float(n_error_train) / len(pred_train))

print 'Predict testing data...'
pred_test = clf.predict(testing_data)
n_error_test = pred_test[pred_test == -1].size
print 'error test: %f' % (float(n_error_test) / len(pred_test))

print 'Predict outlier data...'
pred_outlier = clf.predict(outlier_data)
n_error_outlier = pred_outlier[pred_outlier == 1].size
print 'error outlier: %f' % (float(n_error_outlier) / len(pred_outlier))


# def score_func3(estimator, X):
#     pred = estimator.predict(X)
#     return float(pred[pred == 1].size) / len(pred)


# grid = GridSearchCV(OneClassSVM(), {
#     'gamma': [1e-1, 1e-3, 1e-5, 1e-7],
#     'nu': [0.1]
# }, cv=4, scoring=score_func3, verbose=100, n_jobs=4)
# grid.fit(training_data[:150000])

# print grid.best_params_, grid.best_score_
# print grid.cv_results_
# print '>>>>>>>>>>>>>'


# def score_func2(estimator, X):
#     pred = estimator.predict(testing_data)
#     return float(pred[pred == 1].size) / len(pred)


# grid = GridSearchCV(OneClassSVM(), {
#     'gamma': [1e-1, 1e-3, 1e-5, 1e-7],
#     'nu': [0.1]
# }, cv=4, scoring=score_func2, verbose=100, n_jobs=4)
# grid.fit(training_data[:150000])

# print grid.best_params_, grid.best_score_
# print grid.cv_results_
# print '>>>>>>>>>>>>>'


# def score_func(estimator, X):
#     pred = estimator.predict(outlier_data)
#     return float(pred[pred == -1].size) / len(pred)


# grid = GridSearchCV(OneClassSVM(), {
#     'gamma': [1e-1, 1e-3, 1e-5, 1e-7],
#     'nu': [0.1]
# }, cv=4, scoring=score_func, verbose=100, n_jobs=4)
# grid.fit(training_data[:150000])

# print grid.best_params_, grid.best_score_
# print grid.cv_results_
