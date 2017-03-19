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

Global = partial(_config.get, 'Global')

Dropbox = partial(_config.get, 'Dropbox')
Email = partial(_config.get, 'Email')
Evernote = partial(_config.get, 'Evernote')
Facebook = partial(_config.get, 'Facebook')
Ghost = partial(_config.get, 'Ghost')
Github = partial(_config.get, 'Github')
Gmail = partial(_config.get, 'Gmail')
# https://developers.google.com/api-client-library/python/apis/drive/v2
GoogleDrive = partial(_config.get, 'Google Drive')
Medium = partial(_config.get, 'Medium')
Twitter = partial(_config.get, 'Twitter')
Weibo = partial(_config.get, 'Weibo')
Wordpress = partial(_config.get, 'Wordpress')
Yinxiang = partial(_config.get, 'Yinxiang')

# TODO: messagebird, reddit, foursquare, onenote, pinterest

IFTTT = partial(_config.get, 'IFTTT')
Zapier = partial(_config.get, 'Zapier')

Pool = partial(_config.get, 'Pool')

Pushbullet = partial(_config.get, 'Pushbullet')


del partial
