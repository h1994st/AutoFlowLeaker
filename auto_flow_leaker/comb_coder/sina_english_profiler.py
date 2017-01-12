#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-09 22:08:21
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import re
import md5
import json
import pytz
import datetime
import HTMLParser
import dateutil.parser

import peewee
import requests
from lxml import html

from public_pool import SINA_EN

html_parser = HTMLParser.HTMLParser()


def parse_and_save_news_page(url):
    res = requests.get(url)
    tree = html.fromstring(res.text)
    news_wrap = tree.cssselect('div.wrap')[0]

    try:
        section_elem = news_wrap.cssselect(
            'div.subNav > div.subNav_left > div.tag > a')[0]
        sub_section_elem = news_wrap.cssselect(
            'div.subNav > div.subNav_left > div.tag_cont > a')[0]
    except IndexError:
        return None, None

    return html_parser.unescape(
        section_elem.text), html_parser.unescape(sub_section_elem.text)


pattern = re.compile(
    '<div class="r-info"><h4><a href="(?P<link>.*)" target="_blank">(?P<title>.*)</a></h4><p>(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} GMT) \&nbsp;(?P<author>.*) \&nbsp;(?P<subsection>.*)</p><p class="content">(?P<content>.*) <a href=".*" target="_blank">Full Story</a></p></div>')


with open('../../data/sina_english_structure_meta.json') as fp:
    sina_meta = json.load(fp)

try:
    i = 0
    for section in sina_meta:
        for sub_section in sina_meta[section]:
            res = requests.get(sina_meta[section][sub_section])
            tree = html.fromstring(res.text)
            script = tree.cssselect('script')[-3].text

            print sina_meta[section][sub_section]
            m = pattern.findall(script)

            # lastest_datetime = SINA_EN.select(
            #     peewee.fn.Max(
            #         SINA_EN.DATE)).where(
            #             SINA_EN.SUB_SECTION == sub_section).scalar()
            # if lastest_datetime is not None:
            #     lastest_datetime = lastest_datetime.replace(
            #         tzinfo=pytz.utc)

            for meta in m:
                # 0 link
                # 1 title
                # 2 date
                # 3 author or source
                # 4 subsection
                # 5 content
                # section_name, sub_section_name = parse_and_save_news_page(
                #     meta[0])

                # section_name = section_name or section
                # sub_section_name = sub_section_name or sub_section
                # if sub_section.istitle():
                #     sub_section_name = sub_section_name.title()

                # if sub_section.isupper():
                #     sub_section_name = sub_section_name.upper()

                # assert section_name == section, section_name
                # assert sub_section_name == sub_section, sub_section_name

                news_datetime = dateutil.parser.parse(meta[2])
                # if (lastest_datetime is not None and
                #         news_datetime <= lastest_datetime):
                #     print 'Exist!'
                #     continue

                try:
                    SINA_EN.create(
                        SECTION=section,
                        SUB_SECTION=sub_section,
                        AUTHOR=meta[3],
                        TITLE=html_parser.unescape(meta[1]),
                        DATE=news_datetime,
                        URL=meta[0], URL_MD5=md5.new(meta[0]).hexdigest(),
                        PROFILE_DATE=datetime.datetime.now(pytz.utc),
                        SUMMARY=meta[5])
                except peewee.IntegrityError as e:
                    print 'Exist: %r' % e, section, sub_section, meta[0]
                    continue
                except Exception as e:
                    print 'Error: %r' % e
                    print section, sub_section, meta[0]
                    raise e
                else:
                    i += 1
                    print i
                finally:
                    pass
except Exception as e:
    print 'Error: %r' % e
    raise e
finally:
    pass
