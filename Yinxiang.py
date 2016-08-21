#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 18:20:19
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

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
