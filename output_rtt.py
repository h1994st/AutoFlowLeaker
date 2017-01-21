#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-24 11:19:09
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json

import numpy as np


def main():
    # Email -> Wordpress via IFTTT
    print 'Email -> Wordpress via IFTTT'
    with open('data/rtt/email_IFTTT_wordpress_1483893177.json') as fp:
        data1 = json.load(fp)
    with open('data/rtt/email_IFTTT_wordpress_1483893361.json') as fp:
        data2 = json.load(fp)
    with open('data/rtt/email_IFTTT_wordpress_1483893700.json') as fp:
        data3 = json.load(fp)
        action_performed_at = [x[1] for x in data3]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Interval Avg.:', np.mean(intervals),
        print 'Interval Std.:', np.std(intervals)
    with open('data/rtt/email_IFTTT_wordpress_1483894138.json') as fp:
        data4 = json.load(fp)
        action_performed_at = [x[1] for x in data4]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Interval Avg.:', np.mean(intervals),
        print 'Interval Std.:', np.std(intervals)

    data = data1 + data2 + data3 + data4
    delays = [x[1] - x[0] for x in data]

    print 'Delay Avg.:', np.mean(delays),
    print 'Delay Std.:', np.std(delays)
    print ''

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

    # Ghost -> Wordpress via IFTTT with forcing check
    print 'Ghost -> Wordpress via IFTTT with forcing check'
    with open('data/rtt/ghost_IFTTT_wordpress_1482907187.json') as fp:
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
    with open('data/rtt/evernote_IFTTT_github_1474714363.json') as fp:
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
    with open('data/rtt/ghost_Zapier_wordpress_1474702567.json') as fp:
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
    with open('data/rtt/evernote_Zapier_github_1484952317.json') as fp:
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

    # Ghost -> Wordpress via Microsoft Flow
    print 'Ghost -> Wordpress via Flow'
    with open('data/rtt/ghost_Micro_wordpress_1480617920.json') as fp:
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
    with open('data/rtt/ghost_flow_wordpress_1484940083.json') as fp:
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

    # Ghost -> Wordpress via APIAnt
    print 'Ghost -> Wordpress via APIAnt'
    with open('data/rtt/ghost_APIant_wordpress_1480872682.json') as fp:
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
