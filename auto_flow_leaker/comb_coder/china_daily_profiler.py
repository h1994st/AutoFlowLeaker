#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-09 19:50:14
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


with open('../../data/china_daily_feeds.json') as fp:
    china_daily_feeds = json.load(fp)

try:
    db.connect()

    i = 0
    for section in china_daily_feeds:
        feed = feedparser.parse(china_daily_feeds[section])
        # lastest_datetime = CHINA_DAILY.select(
        #     peewee.fn.Max(
        #         CHINA_DAILY.DATE)).where(
        #             CHINA_DAILY.SECTION == section).scalar()
        # if lastest_datetime is not None:
        #     lastest_datetime = lastest_datetime.replace(tzinfo=pytz.utc)

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

            if not hasattr(news, 'published'):
                continue

            news_datetime = pytz.timezone('Asia/Shanghai').localize(
                datetime.datetime.strptime(
                    news.published, '%Y-%m-%d %H:%M:%S')).astimezone(
                        pytz.UTC)
            # if (lastest_datetime is not None and
            #         news_datetime <= lastest_datetime):
            #     print 'Exist!'
            #     continue

            try:
                CHINA_DAILY.create(
                    SECTION=section, SUB_SECTION=news.tags[0].term,
                    AUTHOR=news.authorname, TITLE=news.title,
                    DATE=news_datetime,
                    URL=news.link, URL_MD5=md5.new(news.link).hexdigest(),
                    PROFILE_DATE=datetime.datetime.now(pytz.utc),
                    SUMMARY=news.summary)
            except peewee.IntegrityError as e:
                print 'Exist: %r' % e, section, news.tags[0].term, news.link
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
