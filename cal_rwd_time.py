#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-26 00:22:38
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json


def cal_rwd_time(data):
    def reduce_data(accum_value, x):
        # Read
        if x[0] >= 0:
            accum_value["read"] += x[0]
            accum_value["read_count"] += 1
            accum_value["read_min"] = min(accum_value["read_min"], x[0])
            accum_value["read_max"] = max(accum_value["read_max"], x[0])

        # Write
        if x[1] >= 0:
            accum_value["write"] += x[1]
            accum_value["write_count"] += 1
            accum_value["write_min"] = min(accum_value["write_min"], x[1])
            accum_value["write_max"] = max(accum_value["write_max"], x[1])

        # Delete
        if x[2] >= 0:
            accum_value["delete"] += x[2]
            accum_value["delete_count"] += 1
            accum_value["delete_min"] = min(accum_value["delete_min"], x[2])
            accum_value["delete_max"] = max(accum_value["delete_max"], x[2])

        accum_value["count"] = max(
            accum_value["read_count"],
            accum_value["write_count"],
            accum_value["delete_count"])

        return accum_value

    ret = {
        "read": 0,
        "write": 0,
        "delete": 0,
        "count": 0,
        "read_count": 0,
        "write_count": 0,
        "delete_count": 0,
        "read_min": 16,
        "write_min": 16,
        "delete_min": 16,
        "read_max": 0,
        "write_max": 0,
        "delete_max": 0
    }

    return reduce(reduce_data, data, ret)


def mainland():
    print '%10s  %8s, %8s, %8s' % ('Service', 'Read', 'Write', 'Delete')
    with open('data/bak/ghost_rwd_time.txt', 'r') as fp:
        data = json.load(fp)
        result = cal_rwd_time(data)
        read_average = result["read"] / result["read_count"]
        write_average = result["write"] / result["write_count"]
        delete_average = result["delete"] / result["delete_count"]
        print '%10s  %.6f, %.6f, %.6f' % (
            'Ghost', read_average, write_average, delete_average)

    with open('data/bak/github_rwc_time.txt', 'r') as fp:
        data = json.load(fp)
        result = cal_rwd_time(data)
        read_average = result["read"] / result["read_count"]
        write_average = result["write"] / result["write_count"]
        delete_average = result["delete"] / result["delete_count"]
        print '%10s  %.6f, %.6f, %.6f' % (
            'Github', read_average, write_average, delete_average)

    with open('data/bak/yinxiang_rwd_time.txt', 'r') as fp:
        data = json.load(fp)
        result = cal_rwd_time(data)
        read_average = result["read"] / result["read_count"]
        write_average = result["write"] / result["write_count"]
        delete_average = result["delete"] / result["delete_count"]
        print '%10s  %.6f, %.6f, %.6f' % (
            'Yinxiang', read_average, write_average, delete_average)


def hongkong():
    print '%10s  %8s, %8s, %8s' % ('Service', 'Read', 'Write', 'Delete')
    with open('data/ghost_rwd_time.txt', 'r') as fp:
        data = json.load(fp)
        result = cal_rwd_time(data)
        read_average = result["read"] / result["read_count"]
        write_average = result["write"] / result["write_count"]
        delete_average = result["delete"] / result["delete_count"]
        print '%10s  %.6f, %.6f, %.6f' % (
            'Ghost', read_average, write_average, delete_average)

    with open('data/github_rwc_time.txt', 'r') as fp:
        data = json.load(fp)
        result = cal_rwd_time(data)
        read_average = result["read"] / result["read_count"]
        write_average = result["write"] / result["write_count"]
        delete_average = result["delete"] / result["delete_count"]
        print '%10s  %.6f, %.6f, %.6f' % (
            'Github', read_average, write_average, delete_average)

    with open('data/yinxiang_rwd_time.txt', 'r') as fp:
        data = json.load(fp)
        result = cal_rwd_time(data)
        read_average = result["read"] / result["read_count"]
        write_average = result["write"] / result["write_count"]
        delete_average = result["delete"] / result["delete_count"]
        print '%10s  %.6f, %.6f, %.6f' % (
            'Yinxiang', read_average, write_average, delete_average)

    with open('data/wordpress_rwd_time.txt', 'r') as fp:
        data = json.load(fp)
        result = cal_rwd_time(data)
        read_average = result["read"] / result["read_count"]
        write_average = result["write"] / result["write_count"]
        delete_average = result["delete"] / result["delete_count"]
        print '%10s  %.6f, %.6f, %.6f' % (
            'Wordpress', read_average, write_average, delete_average)

    with open('data/evernote_rwd_time.txt', 'r') as fp:
        data = json.load(fp)
        result = cal_rwd_time(data)
        read_average = result["read"] / result["read_count"]
        write_average = result["write"] / result["write_count"]
        delete_average = result["delete"] / result["delete_count"]
        print '%10s  %.6f, %.6f, %.6f' % (
            'Evernote', read_average, write_average, delete_average)

if __name__ == '__main__':
    print 'China'
    mainland()

    print 'Hongkong'
    hongkong()
