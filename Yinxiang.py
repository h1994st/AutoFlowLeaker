#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 18:20:19
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from pprint import pprint

from Evernote import Evernote

import Config


class Yinxiang(Evernote):
    '''
    Default user: covert_tom (covert_tom@163.com)
    '''

    def __init__(self, **kwargs):
        kwargs.setdefault('service_host', Config.Yinxiang('host'))
        kwargs.setdefault('token', Config.Yinxiang('token'))

        super(Yinxiang, self).__init__(**kwargs)


def test_yinxiang():
    e = Yinxiang()

    # Read all
    pprint(e.receive_all())

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        content = fp.read()
        print e.send(content)

    # time.sleep(3)

    pprint(e.receive_all())

    # Delete all
    e.delete_all()

    # Read all
    pprint(e.receive_all())


if __name__ == '__main__':
    test_yinxiang()
