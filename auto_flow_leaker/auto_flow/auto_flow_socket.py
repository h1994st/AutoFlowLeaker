#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 19:15:53
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from channel import Channel


class AutoFlowSocket(object):
    '''
    '''
    def __init__(self, sender=None, receiver=None):
        assert (sender is None or isinstance(sender, Channel)), sender
        assert (receiver is None or isinstance(receiver, Channel)), receiver
        assert not (sender is None and receiver is None), (
            'must assign at least one sender or receiver')

        super(AutoFlowSocket, self).__init__()

        self.sender = sender
        self.receiver = receiver

    def __repr__(self):
        return (
            'AutoFlowSocket(sender={!r}, receiver={!r})'
        ).format(self.sender, self.receiver)

    def send(self, post_content):
        assert self.sender is not None, self.sender
        assert isinstance(self.sender, Channel), self.sender
        assert isinstance(post_content, str), post_content

        return self.sender.send(post_content)

    def receive(self):
        assert self.receiver is not None, self.receiver
        assert isinstance(self.receiver, Channel), self.receiver

        # non-block version
        return self.receiver.receive_all()
