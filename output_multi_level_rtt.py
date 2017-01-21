#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-24 23:27:20
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : $Id$

import json

import numpy as np


def main():
    print 'Series flow'
    # Ghost -> Wordpress via IFTTT, 2-level
    print 'Ghost -(IFTTT)-> Facebook -(IFTTT)-> Wordpress'
    with open('data/rtt/ghost_IFTTT_2_wordpress_1480433075.json') as fp:
        data = json.load(fp)
        delays = [x[1] - x[0] for x in data]
        action_performed_at = [x[1] for x in data]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Delay Avg.:', np.mean(delays),
        print 'Std.:', np.std(delays)
        print 'Interval Avg.:', np.mean(intervals),
        print 'Std.:', np.std(intervals)
    print ''

    # Evernote -> Github via IFTTT, 2-level
    print 'Evernote -(IFTTT)-> Facebook -(IFTTT)-> Github'
    with open('data/rtt/evernote_IFTTT_2_github_1480530846.json') as fp:
        data = json.load(fp)
        delays = [x[1] - x[0] for x in data]
        action_performed_at = [x[1] for x in data]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Delay Avg.:', np.mean(delays),
        print 'Std.:', np.std(delays)
        print 'Interval Avg.:', np.mean(intervals),
        print 'Std.:', np.std(intervals)
    print ''

    # Ghost -> Wordpress via IFTTT and Zapier, 2-level
    print 'Ghost -(Zapier)-> Facebook -(IFTTT)-> Wordpress'
    with open('data/rtt/ghost_Zapier_IFTTT_wordpress_1480445063.json') as fp:
        data = json.load(fp)
        delays = [x[1] - x[0] for x in data]
        action_performed_at = [x[1] for x in data]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Delay Avg.:', np.mean(delays),
        print 'Std.:', np.std(delays)
        print 'Interval Avg.:', np.mean(intervals),
        print 'Std.:', np.std(intervals)
    print ''

    # Evernote -> Github via IFTTT and Zapier, 2-level
    print 'Evernote -(Zapier)-> Facebook -(IFTTT)-> Github'
    with open('data/rtt/evernote_Zapier_IFTTT_github_1480607129.json') as fp:
        data = json.load(fp)
        delays = [x[1] - x[0] for x in data]
        action_performed_at = [x[1] for x in data]
        intervals = []
        for i in xrange(len(action_performed_at) - 1):
            intervals.append(
                action_performed_at[i + 1] - action_performed_at[i])

        print 'Delay Avg.:', np.mean(delays),
        print 'Std.:', np.std(delays)
        print 'Interval Avg.:', np.mean(intervals),
        print 'Std.:', np.std(intervals)
    print ''

    print 'Parallel flow'
    # Ghost -> Wordpress via IFTTT
    print 'Ghost ---(IFTTT)--> Wordpress'
    print '       |-(IFTTT)-|'
    with open('data/rtt/ghost_IFTTT_IFTTT_wordpress_1480810570_para.json') as fp:
        data = json.load(fp)
        delays = [max(x[2], x[3]) - min(x[0], x[1]) for x in data]
        action_performed_at_1 = [x[2] for x in data]
        action_performed_at_2 = [x[3] for x in data]
        intervals_1 = []
        intervals_2 = []
        for i in xrange(len(action_performed_at_1) - 1):
            intervals_1.append(
                action_performed_at_1[i + 1] - action_performed_at_1[i])
        for i in xrange(len(action_performed_at_2) - 1):
            intervals_2.append(
                action_performed_at_2[i + 1] - action_performed_at_2[i])

        two_action_time_offset = []
        assert len(action_performed_at_1) == len(action_performed_at_2)
        for i in xrange(len(action_performed_at_1)):
            two_action_time_offset.append(
                abs(action_performed_at_1[i] - action_performed_at_2[i]))

        print 'Delay Avg.:', np.mean(delays),
        print 'Std.:', np.std(delays)
        print 'Interval 1 Avg.:', np.mean(intervals_1),
        print 'Std.:', np.std(intervals_1)
        print 'Interval 2 Avg.:', np.mean(intervals_2),
        print 'Std.:', np.std(intervals_2)

        print 'Action Time Offset Avg.:', np.mean(two_action_time_offset),
        print 'Std.:', np.std(two_action_time_offset)
    print ''

    # Evernote -> Github via IFTTT
    print 'Evernote ---(IFTTT)--> Github'
    print '          |-(IFTTT)-|'
    with open('data/rtt/evernote_IFTTT_IFTTT_github_1480790584_para.json') as fp:
        data = json.load(fp)
        delays = [max(x[2], x[3]) - min(x[0], x[1]) for x in data]
        action_performed_at_1 = [x[2] for x in data]
        action_performed_at_2 = [x[3] for x in data]
        intervals_1 = []
        intervals_2 = []
        for i in xrange(len(action_performed_at_1) - 1):
            intervals_1.append(
                action_performed_at_1[i + 1] - action_performed_at_1[i])
        for i in xrange(len(action_performed_at_2) - 1):
            intervals_2.append(
                action_performed_at_2[i + 1] - action_performed_at_2[i])

        two_action_time_offset = []
        assert len(action_performed_at_1) == len(action_performed_at_2)
        for i in xrange(len(action_performed_at_1)):
            two_action_time_offset.append(
                abs(action_performed_at_1[i] - action_performed_at_2[i]))

        print 'Delay Avg.:', np.mean(delays),
        print 'Std.:', np.std(delays)
        print 'Interval 1 Avg.:', np.mean(intervals_1),
        print 'Std.:', np.std(intervals_1)
        print 'Interval 2 Avg.:', np.mean(intervals_2),
        print 'Std.:', np.std(intervals_2)

        print 'Action Time Offset Avg.:', np.mean(two_action_time_offset),
        print 'Std.:', np.std(two_action_time_offset)
    print ''

    # Ghost -> Wordpress via IFTTT and Zapier
    print 'Ghost ---(IFTTT)--> Wordpress'
    print '       |-(Zapier)-|'
    with open('data/rtt/ghost_IFTTT_ZAPIER_wordpress_1480843547_para.json') as fp:
        data = json.load(fp)
        delays = [max(x[2], x[3]) - min(x[0], x[1]) for x in data]
        action_performed_at_1 = [x[2] for x in data]
        action_performed_at_2 = [x[3] for x in data]
        intervals_1 = []
        intervals_2 = []
        for i in xrange(len(action_performed_at_1) - 1):
            intervals_1.append(
                action_performed_at_1[i + 1] - action_performed_at_1[i])
        for i in xrange(len(action_performed_at_2) - 1):
            intervals_2.append(
                action_performed_at_2[i + 1] - action_performed_at_2[i])

        two_action_time_offset = []
        assert len(action_performed_at_1) == len(action_performed_at_2)
        for i in xrange(len(action_performed_at_1)):
            two_action_time_offset.append(
                abs(action_performed_at_1[i] - action_performed_at_2[i]))

        print 'Delay Avg.:', np.mean(delays),
        print 'Std.:', np.std(delays)
        print 'Interval 1 Avg.:', np.mean(intervals_1),
        print 'Std.:', np.std(intervals_1)
        print 'Interval 2 Avg.:', np.mean(intervals_2),
        print 'Std.:', np.std(intervals_2)

        print 'Action Time Offset Avg.:', np.mean(two_action_time_offset),
        print 'Std.:', np.std(two_action_time_offset)
    print ''

    # Evernote -> Github via IFTTT and Zapier
    print 'Evernote ---(IFTTT)--> Github'
    print '          |-(Zapier)-|'
    with open('data/rtt/evernote_IFTTT_ZAPIER_github_1480877148_para.json') as fp:
        data = json.load(fp)
        delays = [max(x[2], x[3]) - min(x[0], x[1]) for x in data]
        action_performed_at_1 = [x[2] for x in data]
        action_performed_at_2 = [x[3] for x in data]
        intervals_1 = []
        intervals_2 = []
        for i in xrange(len(action_performed_at_1) - 1):
            intervals_1.append(
                action_performed_at_1[i + 1] - action_performed_at_1[i])
        for i in xrange(len(action_performed_at_2) - 1):
            intervals_2.append(
                action_performed_at_2[i + 1] - action_performed_at_2[i])

        two_action_time_offset = []
        assert len(action_performed_at_1) == len(action_performed_at_2)
        for i in xrange(len(action_performed_at_1)):
            two_action_time_offset.append(
                abs(action_performed_at_1[i] - action_performed_at_2[i]))

        print 'Delay Avg.:', np.mean(delays),
        print 'Std.:', np.std(delays)
        print 'Interval 1 Avg.:', np.mean(intervals_1),
        print 'Std.:', np.std(intervals_1)
        print 'Interval 2 Avg.:', np.mean(intervals_2),
        print 'Std.:', np.std(intervals_2)

        print 'Action Time Offset Avg.:', np.mean(two_action_time_offset),
        print 'Std.:', np.std(two_action_time_offset)
    print ''


if __name__ == '__main__':
    main()
