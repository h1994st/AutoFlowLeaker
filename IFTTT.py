#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-30 00:25:44
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import httplib2


class IFTTT(object):
    '''
    Default user: covertsan (covert.san@gmail.com)
    '''
    def __init__(self):
        super(IFTTT, self).__init__()

    def force_run(self, recipe_id):
        h = httplib2.Http()
