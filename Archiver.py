#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-27 14:31:50
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import libarchive.public
import libarchive.constants

for entry in libarchive.public.create_file(
        'test.7z',
        libarchive.constants.ARCHIVE_FORMAT_7ZIP,
        ['data/eva_time_data_1.in', 'data/eva_time_data_2.in', 'data/eva_time_data_3.in']):
    print entry
