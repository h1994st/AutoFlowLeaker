#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 14:51:36
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from functools import partial

_config = __import__('ConfigParser').SafeConfigParser(allow_no_value=True)

_config.read('default.conf')


get = _config.get
getboolean = _config.getboolean
getint = _config.getint
getfloat = _config.getfloat

Github = partial(_config.get, 'Github')
Yinxiang = partial(_config.get, 'Yinxiang')
Email = partial(_config.get, 'Email')
Ghost = partial(_config.get, 'Ghost')
Facebook = partial(_config.get, 'Facebook')
Wordpress = partial(_config.get, 'Wordpress')
Evernote = partial(_config.get, 'Evernote')
Twitter = partial(_config.get, 'Twitter')
Gmail = partial(_config.get, 'Gmail')
IFTTT = partial(_config.get, 'IFTTT')

del partial
