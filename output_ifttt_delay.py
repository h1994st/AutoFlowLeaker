#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-26 12:55:22
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json


def main():
    # Evernote -> Github via IFTTT
    print 'Evernote -> Github via IFTTT'
    with open('data/rtt/evernote_to_github_IFTTT.json') as fp:
        data = json.load(fp)
        delays1 = [x[1] - x[0] for x in data]

    with open('data/rtt/evernote_IFTTT_github_1474663935.json') as fp:
        data = json.load(fp)
        delays2 = [x[1] - x[0] for x in data]

    with open('data/rtt/evernote_IFTTT_github_1474714363.json') as fp:
        data = json.load(fp)
        delays3 = [x[1] - x[0] for x in data]

    print delays1 + delays2 + delays3


if __name__ == '__main__':
    main()
