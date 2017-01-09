#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-09 02:54:54
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import md5
import json
import pytz
import datetime

import peewee
import feedparser

db = peewee.MySQLDatabase('AUTO_PUBLIC_POOL', user='root', passwd='hsthst')


class Profiler(object):
    '''
    Collect news on structural websites

    Website - Column - Page - URL
    '''
    def __init__(self):
        super(Profiler, self).__init__()


class CNNProfiler(Profiler):
    '''
    CNN Profiler
    '''
    def __init__(self):
        super(CNNProfiler, self).__init__()


class CHINA_DAILY(peewee.Model):
        ID = peewee.IntegerField()
        SECTION = peewee.CharField()
        SUB_SECTION = peewee.CharField()
        AUTHOR = peewee.CharField()
        TITLE = peewee.CharField()
        DATE = peewee.DateTimeField()
        URL = peewee.CharField()
        PROFILE_DATE = peewee.DateTimeField()
        URL_MD5 = peewee.CharField()
        SUMMARY = peewee.CharField()

        class Meta:
            database = db


class ChinaDailyProfiler(Profiler):
    '''
    China Daily Profiler

    Feeds: data/china_daily_feeds.json
    '''
    def __init__(self):
        super(ChinaDailyProfiler, self).__init__()

    def profile(self):
        with open("data/china_daily_feeds.json") as fp:
            china_daily_feeds = json.load(fp)

        try:
            i = 0
            for section in china_daily_feeds:
                feed = feedparser.parse(china_daily_feeds[section])

                for news in feed.entries:
                    # # section
                    # print section
                    # # sub section
                    # print news.tags[0].term
                    # # author
                    # print news.authorname
                    # # date
                    # print news.published, news.published_parsed
                    # # url
                    # print news.link
                    # print md5.new(news.link).hexdigest()
                    # # summary
                    # print news.summary
                    # print ''

                    if not hasattr(news, 'authorname'):
                        news.authorname = ''

                    try:
                        CHINA_DAILY.create(
                            SECTION=section, SUB_SECTION=news.tags[0].term,
                            AUTHOR=news.authorname, TITLE=news.title,
                            DATE=pytz.timezone('Asia/Shanghai').localize(
                                datetime.datetime.strptime(
                                    news.published,
                                    '%Y-%m-%d %H:%M:%S')).astimezone(
                                        pytz.UTC),
                            URL=news.link,
                            URL_MD5=md5.new(news.link).hexdigest(),
                            PROFILE_DATE=datetime.datetime.now(pytz.utc),
                            SUMMARY=news.summary)
                    except peewee.IntegrityError as e:
                        print 'Error: %r' % e
                        print section, news.tags[0].term, news.link
                        continue
                    except AttributeError as e:
                        print 'Error: %r' % e
                        print section, news.tags[0].term, news.link
                        continue
                    else:
                        i += 1
                        print i
                    finally:
                        pass
                print ''
        except Exception as e:
            print 'Error: %r' % e
        finally:
            db.close()


def main():
    pass


if __name__ == '__main__':
    main()
