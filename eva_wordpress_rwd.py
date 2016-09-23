#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-23 19:10:52
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

from Wordpress import Wordpress


def test_wordoress(data):
    try:
        w = Wordpress()
        print 'Wordpress'

        # Write
        print 'Write'
        begin = time.time()
        post = w.create_post(
            'from py %s' % time.time(), data, fields='ID,title')
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        w.get_post(post['ID'], fields='ID,title')
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        w.delete_post(post['ID'], fields='ID,title')
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def main(rounds):
    wordpresses = []

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        data = fp.read().strip()

        for i in xrange(rounds):
            print 'Round %d' % i

            try:
                temp = test_wordoress(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                wordpresses.append(temp)
                print 'Wordpress:', temp

    # Save
    print 'Save results...'
    with open('data/wordpress_rwd_time_2.txt', 'w') as fp:
        print 'Wordpress...'
        json.dump(wordpresses, fp)
    print 'Done!'


if __name__ == '__main__':
    main(1000)
