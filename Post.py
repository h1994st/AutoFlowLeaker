#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-03 16:49:39
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import pytz
import datetime


class Post(object):
    '''Post object'''
    def __init__(self,
                 content=None, title=None,
                 create_time=None, id=None):
        super(Post, self).__init__()

        self._content_value = None
        self._title_value = None
        self._create_time_value = None
        self._id_value = None

        self.content = content
        self.title = title
        self.create_time = create_time or datetime.datetime.now(pytz.utc)
        self.id = id

    @property
    def id(self):
        '''
        A unique identifier for the post.

        :rtype: str
        '''
        if self._id_value is not None:
            return self._id_value
        else:
            raise AttributeError('missing required field \'id\'')

    @id.setter
    def id(self, val):
        self._id_value = val

    @id.deleter
    def id(self):
        self._id_value = None

    @property
    def content(self):
        '''
        Readable contents of the post.

        :rtype: str
        '''
        return self._content_value

    @content.setter
    def content(self, val):
        self._content_value = val

    @content.deleter
    def content(self):
        self._content_value = None

    @property
    def create_time(self):
        '''
        Create timestamp of the post.

        :rtype: datetime.datetime
        '''
        if self._create_time_value is not None:
            return self._create_time_value
        else:
            raise AttributeError('missing required field \'create_time\'')

    @create_time.setter
    def create_time(self, val):
        if not isinstance(val, datetime.datetime):
            raise AttributeError(
                'attribute \'create_time\' type should be  \'datetime.datetime\'')
        if val.tzinfo != pytz.UTC:
            raise AttributeError(
                'attribute \'create_time\' time zone should be \'UTC\'')
        self._create_time_value = val

    @create_time.deleter
    def create_time(self):
        self._create_time_value = None

    @property
    def title(self):
        '''
        Possible post title or filename.

        :rtype: str
        '''
        if self._title_value is not None:
            return self._title_value
        else:
            raise AttributeError('missing required field \'title\'')

    @title.setter
    def title(self, val):
        self._title_value = val

    @title.deleter
    def title(self):
        self._title_value = None

    def __repr__(self):
        if self.content is None:
            return 'PostMeta(id={!r}, title={!r}, create_time={!r})'.format(
                self.id, self.title, self.create_time)
        return 'Post(id={!r}, title={!r}, create_time={!r}, content=\'{!s}...\')'.format(
            self.id, self.title, self.create_time, self.content[:16])
