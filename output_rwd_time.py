#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-22 23:44:29
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import json

import numpy as np


destDir = os.path.join(
    os.path.expanduser('~'),
    'Documents/Private/Learning/Security/SVN_Root/h1994st')


def is_error(x):
    assert isinstance(x, (tuple, list)), x

    return -1 in x


def cal_rwd(path):
    ret = None
    with open(path, 'r') as fp:
        data = json.load(fp)
        data = filter(lambda x: -1 not in x, data)
        data = np.array(data)

        ret = (np.mean(data, axis=0), np.std(data, axis=0))

    return ret


def main():
    # data/bak/
    print 'China:'

    # Ghost R
    # Ghost W
    # Ghost D
    print 'Ghost', cal_rwd('data/bak/ghost_rwd_time.txt')

    # Github R
    # Github W
    # Github C
    print 'Github', cal_rwd('data/bak/github_rwc_time.txt')

    # Yinxiang R
    # Yinxiang W
    # Yinxiang D
    print 'Yinxiang', cal_rwd('data/bak/yinxiang_rwd_time.txt')

    # data/
    print 'Hong Kong:'

    # Evernote R
    # Evernote W
    # Evernote D
    print 'Evernote', cal_rwd('data/evernote_rwd_time.txt')

    # Ghost R
    # Ghost W
    # Ghost D
    print 'Ghost', cal_rwd('data/ghost_rwd_time.txt')

    # Github R
    # Github W
    # Github D
    print 'Github', cal_rwd('data/github_rwc_time_2.txt')

    # Wordpress R
    # Wordpress W
    # Wordpress D
    print 'Wordpress', cal_rwd('data/wordpress_rwd_time.txt')

    # Yinxiang R
    # Yinxiang W
    # Yinxiang D
    print 'Yinxiang', cal_rwd('data/yinxiang_rwd_time.txt')


if __name__ == '__main__':
    main()