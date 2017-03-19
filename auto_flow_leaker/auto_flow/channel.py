#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-03 15:24:09
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from .post import Post


class Channel(object):
    '''
    Base object of Channel service
    '''
    def __init__(self):
        super(Channel, self).__init__()

    def __repr__(self):
        return (
            '{type}({description})'
        ).format(
            type=type(self).__name__,
            description=self.description()
        )

    def description(self):
        raise NotImplementedError(
            'Class %s doesn\'t implement description()' % (
                self.__class__.__name__))

    def send(self, *args, **kwargs):
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

        assert isinstance(
            items[0], Post), 'Wrong implementation of receive_all()'

        return items[0]

    def receive_all(self):
        '''Retrieve all the items on the channel

        Messages should be sorted in reverse chronological order.'''
        raise NotImplementedError(
            'Class %s doesn\'t implement receive_all()' % (
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
