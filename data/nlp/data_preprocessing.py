#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-18 15:36:52
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os


base_dir = '/Users/tomhu/Desktop/Experiment/covert channle/CovertLeaker/data/nlp/'
training_dir = os.path.join(base_dir, 'training')
training_file = os.path.join(training_dir, 'all_out.csv')
testing_dir = os.path.join(base_dir, 'testing')


def normalize_filter(line):
    num_nn, num_vb, num_adj, num_adv, total, score, classes = line.split(
        ',')

    if line.find('NaN') != -1:
        print 'Remove: ', line.strip()
        return ''

    total = int(total)

    if total <= 3:
        print 'Remove: ', line.strip()
        return ''

    num_nn = float(num_nn) / total
    num_vb = float(num_vb) / total
    num_adj = float(num_adj) / total
    num_adv = float(num_adv) / total

    return '%f,%f,%f,%f,%d,%s,%s' % (
        num_nn, num_vb, num_adj, num_adv, total, score, classes)


def process_file(input_file):
    with open(input_file, 'r') as in_fp:
        root, ext = os.path.splitext(os.path.abspath(in_fp.name))
        with open('%s_filter%s' % (root, ext), 'w') as out_fp:
            print 'Input:', in_fp.name
            print 'Output:', out_fp.name
            out_fp.write(in_fp.readline())  # header
            for line in in_fp:
                out_fp.write(normalize_filter(line))


# process_file(training_file)
process_file(os.path.join(testing_dir, 'testing-news-digest-0-result.csv'))
process_file(os.path.join(testing_dir, 'testing-news-digest-1-result.csv'))
# process_file(os.path.join(testing_dir, 'testing2.csv'))
# process_file(os.path.join(testing_dir, 'testing3.csv'))
# process_file(os.path.join(testing_dir, 'testing_non_nl.csv'))
# process_file(os.path.join(training_dir, 'wiki_result.csv'))
