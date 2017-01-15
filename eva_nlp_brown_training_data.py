#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-15 02:04:57
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import math

base_dir = '/Users/tomhu/Desktop/Experiment/covert channle/NLP/'
brown_dir = os.path.join(base_dir, 'brownSent')
brown_word_count_dir = os.path.join(brown_dir, 'brownWordCount')
brown_score_dir = os.path.join(brown_dir, 'brownSentScoreV2')

output_dir = '/Users/tomhu/Desktop/Experiment/covert channle/NLP/output'
brown_out_file = os.path.join(output_dir, 'brown_out.csv')

csv_header = 'NN,VB,ADJ,ADV,Total,Score,Class\n'

# Brown
with open(brown_out_file, 'w') as out_fp:
    out_fp.write(csv_header)
    for sentence_hash in os.listdir(brown_score_dir):
        if sentence_hash == '.DS_Store':
            continue

        score_file = os.path.join(brown_score_dir, sentence_hash)
        if not os.path.exists(score_file):
            continue

        with open(score_file, 'r') as fp:
            score = float(fp.read().strip())
        if math.isnan(score):
            print sentence_hash, 'score: NaN'
            continue

        # e.g.
        # NN   :6
        # VB   :3
        # ADJ  :1
        # ADV  :0
        # TOTAL:16
        count_file = os.path.join(brown_word_count_dir, sentence_hash)
        if not os.path.exists(count_file):
            continue

        with open(count_file, 'r') as fp:
            lines = fp.readlines()
            num_nn = int(lines[0][6:])
            num_vb = int(lines[1][6:])
            num_adj = int(lines[2][6:])
            num_adv = int(lines[3][6:])
            num_total = int(lines[4][6:])

        # Write
        line = '%d,%d,%d,%d,%d,%f,%s\n' % (
            num_nn, num_vb, num_adj, num_adv, num_total, score, 'normal')

        print sentence_hash, line.strip()
        out_fp.write(line)
