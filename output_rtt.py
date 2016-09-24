#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-24 11:19:09
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json

import numpy as np


def main():
    # Ghost -> Wordpress via IFTTT
    print 'Ghost -> Wordpress via IFTTT'
    with open('data/rtt/ghost_to_wordpress_IFTTT.json') as fp:
        data = json.load(fp)
        delays = [x[1] - x[0] for x in data]
        action_performed_at = [x[1] for x in data]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Delay Avg.:', np.mean(delays),
        print 'Delay Std.:', np.std(delays)
        print 'Interval Avg.:', np.mean(intervals),
        print 'Interval Std.:', np.std(intervals)
    print ''

    # Evernote -> Github via IFTTT
    print 'Evernote -> Github via IFTTT'
    with open('data/rtt/evernote_to_github_IFTTT.json') as fp:
        data = json.load(fp)
        delays = [x[1] - x[0] for x in data]
        action_performed_at = [x[1] for x in data]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Delay Avg.:', np.mean(delays),
        print 'Delay Std.:', np.std(delays)
        print 'Interval Avg.:', np.mean(intervals),
        print 'Interval Std.:', np.std(intervals)
    with open('data/rtt/evernote_IFTTT_github_1474663935.json') as fp:
        data = json.load(fp)
        delays = [x[1] - x[0] for x in data]
        action_performed_at = [x[1] for x in data]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Delay Avg.:', np.mean(delays),
        print 'Delay Std.:', np.std(delays)
        print 'Interval Avg.:', np.mean(intervals),
        print 'Interval Std.:', np.std(intervals)
    print ''

    # Ghost -> Wordpress via Zapier
    print 'Ghost -> Wordpress via Zapier'
    print ''

    # Evernote -> Github via Zapier
    print 'Evernote -> Github via Zapier'
    with open('data/rtt/evernote_to_github_Zapier.json') as fp:
        data = json.load(fp)
        delays = [x[1] - x[0] for x in data]
        action_performed_at = [x[1] for x in data]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Delay Avg.:', np.mean(delays),
        print 'Delay Std.:', np.std(delays)
        print 'Interval Avg.:', np.mean(intervals),
        print 'Interval Std.:', np.std(intervals)
    print ''


if __name__ == '__main__':
    main()
