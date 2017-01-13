#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-13 17:50:09
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import peewee

from auto_flow_leaker.comb_coder.public_pool import SINA_EN
from auto_flow_leaker.comb_coder.public_pool import CHINA_DAILY


def generate_random_post():
    query = (
        SINA_EN.select(
            SINA_EN.TITLE,
            SINA_EN.SUMMARY,
            SINA_EN.URL).where(
                SINA_EN.SUMMARY != '') |
        CHINA_DAILY.select(
            CHINA_DAILY.TITLE,
            CHINA_DAILY.SUMMARY,
            CHINA_DAILY.URL).where(
                CHINA_DAILY.SUMMARY != '')
    ).order_by(peewee.fn.Rand()).limit(10)
    qr = query.execute()

    return qr


def main(rounds):
    for i in xrange(rounds):
        qr = generate_random_post()
        with open('data/nlp/testing/news%d.txt' % i, 'w') as fp:
            print fp.name
            for result in qr:
                fp.write(result.TITLE.encode('utf8'))
                fp.write('\n')
                fp.write(result.SUMMARY.encode('utf8'))
                fp.write('\n')

    print 'Done!'


if __name__ == '__main__':
    main(10)
