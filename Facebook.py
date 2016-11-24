#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 22:33:56
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import warnings
from pprint import pprint

import facebook

import Config

warnings.filterwarnings('ignore', category=DeprecationWarning)


class Facebook(object):
    '''
    Default user: covert.san@gmail.com
    '''

    def __init__(self):
        self._facebook_graph = facebook.GraphAPI(Config.Facebook('token'))

    @property
    def posts(self):
        return self.get_posts()

    def create_post(self, message):
        assert len(message) <= 63206, \
            'message cnnot be longer than 63206 characters'
        try:
            res = self._facebook_graph.put_object(
                'me', 'feed', message=message)
        except facebook.GraphAPIError as e:
            print 'Something went wrong:', e.type, e.message
            raise e
        else:
            return res['id']  # id of new post

    def get_post(self, id):
        try:
            res = self._facebook_graph.get_object(id)
        except facebook.GraphAPIError as e:
            print 'Something went wrong:', e.type, e.message
            raise e
        else:
            return res

    def get_posts(self):
        try:
            posts = self._facebook_graph.get_connections('me', 'posts')
        except facebook.GraphAPIError as e:
            print 'Something went wrong:', e.type, e.message
            raise e
        else:
            return posts['data']  # list of posts

    def delete_post(self, id):
        try:
            self._facebook_graph.delete_object(id)
        except facebook.GraphAPIError as e:
            print 'Something went wrong:', e.type, e.message
            raise e


def test_fb_message_max():
    fb = Facebook()

    message = '1' * 63206

    # Read all
    pprint(fb.posts)

    try:
        # Write
        post_id = fb.create_post(message)
    except Exception as e:
        print e
    else:
        # Read all
        pprint(fb.posts)

        # Delete
        fb.delete_post(post_id)

        # Read all
        pprint(fb.posts)


def main():
    fb = Facebook()

    # Read all
    pprint(fb.posts)

    # Write
    post_id = fb.create_post('from python auto flow')

    # Read all
    pprint(fb.posts)

    # Delete
    fb.delete_post(post_id)

    # Read all
    pprint(fb.posts)


if __name__ == '__main__':
    test_fb_message_max()
