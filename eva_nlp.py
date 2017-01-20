#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-13 17:50:09
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import re
import subprocess

import peewee

from auto_flow_leaker.comb_coder.public_pool import SINA_EN
from auto_flow_leaker.comb_coder.public_pool import CHINA_DAILY


def parse(sentence, classes):
    command = 'java -Xmx512M -jar StanfordParserDemo.jar "%s" "%s"' % (
        sentence, classes)
    try:
        result = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE).stdout.read()
    except Exception:
        print '>>>> Run Time Error (%s) When parsing:', sentence
    return result


def generate_random_post(num):
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
    ).order_by(peewee.fn.Rand()).limit(num)
    qr = query.execute()

    return qr


def generate_random_post2(num):
    query = CHINA_DAILY.select(
        CHINA_DAILY.TITLE,
        CHINA_DAILY.SUMMARY,
        CHINA_DAILY.URL).where(
            CHINA_DAILY.SUMMARY != '').order_by(peewee.fn.Rand()).limit(num)
    qr = query.execute()

    return qr


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def main(num_news_digest, num_testing_file):
    with open('data/nlp/testing/testing%d.csv' % num_testing_file, 'w') as fp:
        print fp.name

        for i in xrange(num_news_digest):
            print i
            # generate news
            qr = generate_random_post(10)
            for result in qr:
                # fp.write(result.TITLE.encode('utf8'))
                # fp.write('\n')
                # fp.write(result.SUMMARY.encode('utf8'))
                # fp.write('\n')
                fp.write(parse(result.TITLE, 'news %d' % i))
                fp.write(parse(result.SUMMARY, 'news %d' % i))

    print 'Done!'


def main2(num_news_digest, num_testing_file):
    with open('data/nlp/testing/testing-news-digest-%d.csv' % num_testing_file, 'w') as fp:
        print fp.name

        for i in xrange(num_news_digest):
            print i
            # generate news
            qr = generate_random_post2(10)
            for result in qr:
                # fp.write(result.TITLE.encode('utf8'))
                # fp.write('\n')
                # fp.write(result.SUMMARY.encode('utf8'))
                # fp.write('\n')
                line = cleanhtml(result.SUMMARY.encode('utf8'))
                if line[-1] != '.':
                    line += '.'
                fp.write(line)
                fp.write('\n')
                fp.flush()


if __name__ == '__main__':
    for i in xrange(10):
        main2(1000, i)
