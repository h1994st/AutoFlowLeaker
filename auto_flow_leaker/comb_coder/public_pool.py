#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-12 16:05:44
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : $Id$

import peewee

db = peewee.MySQLDatabase(
    'AUTO_PUBLIC_POOL', user='root', passwd='hsthst')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class CHINA_DAILY(BaseModel):
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


class SINA_EN(BaseModel):
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


def main():
    print CHINA_DAILY.select(
        peewee.fn.Count(
            peewee.fn.Distinct(
                CHINA_DAILY.SECTION))).scalar()
    print CHINA_DAILY.select(
        CHINA_DAILY.SECTION,
        peewee.fn.Count(
            peewee.fn.Distinct(
                CHINA_DAILY.SUB_SECTION))).group_by(CHINA_DAILY.SECTION)


if __name__ == '__main__':
    main()
