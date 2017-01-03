#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-03 15:24:09
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0


class Channel(object):
    '''Base object of Channel service'''
    def __init__(self):
        super(Channel, self).__init__()

    def send(self, content, title=None):
        '''Post a new item to the channel'''
        raise NotImplementedError(
            'Class %s doesn\'t implement send()' % (
                self.__class__.__name__))

    def receive(self):
        '''Retrieve the latest item from the channel

        Return: {
            'title': ...,
            'content': ...,
            'create_time': ... <unix epoch>,
            'item_id': ...
        }'''
        items = self.receive_all()

        if len(items) == 0:
            return None

        return items[0]

    def receive_all(self):
        '''Retrieve all the items on the channel

        Messages should be sorted in reverse chronological order.'''
        raise NotImplementedError(
            'Class %s doesn\'t implement retrieve_all()' % (
                self.__class__.__name__))

    def delete(self, item):
        '''Delete the designated item on the channel'''
        raise NotImplementedError(
            'Class %s doesn\'t implement delete()' % (
                self.__class__.__name__))

    def delete_all(self):
        '''Delete all the items on the channel'''
        raise NotImplementedError(
            'Class %s doesn\'t implement delete_all()' % (
                self.__class__.__name__))
