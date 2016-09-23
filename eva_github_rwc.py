#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-23 17:26:00
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

from Github import Github


def test_github(data):
    try:
        g = Github()
        print 'Github'

        # Write
        print 'Write'
        begin = time.time()
        issue = g.create_issue('from py %s' % time.time(), data)
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        g.get_issue(issue.number)
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Close
    print 'Close'
    begin = time.time()
    try:
        g.close_issue(issue=issue)
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def main(rounds):
    githubs = []

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        data = fp.read().strip()

        for i in xrange(rounds):
            print 'Round %d' % i

            try:
                temp = test_github(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                githubs.append(temp)
                print 'Github:', temp

    # Save
    print 'Save results...'

    with open('data/github_rwc_time.txt', 'w') as fp:
        print 'Github...'
        json.dump(githubs, fp)
    print 'Done!'


if __name__ == '__main__':
    main()
