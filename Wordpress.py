#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-21 00:16:38
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
from urllib import urlencode

import httplib2

import Config

TIMEOUT = int(Config.Global('timeout'))


class Wordpress(object):
    """
    Default user: covertsan (covert.san@gmail.com)
    """
    def __init__(self):
        super(Wordpress, self).__init__()

    def _api_url(self, path):
        API_BASE_URL = 'https://public-api.wordpress.com/rest/v1.1'
        return API_BASE_URL + path

    @property
    def posts(self):
        return self.get_posts(fields='ID,title')

    # Write
    def create_post(self, title, body, fields=None):
        '''
        POST /sites/$site/posts/new
        '''
        assert isinstance(title, (str, unicode)), title
        assert isinstance(body, (str, unicode)), body
        assert fields is None or isinstance(fields, (str, unicode)), fields

        h = httplib2.Http(timeout=TIMEOUT)

        post_data = {
            'title': title,
            'content': body
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': '%s %s' % (
                Config.Wordpress('token_type'),
                Config.Wordpress('access_token'))
        }
        parameters = dict()

        if fields is not None:
            parameters['fields'] = fields

        (res_headers, content) = h.request(
            self._api_url('/sites/%s/posts/new/?%s' % (
                Config.Wordpress('site'), urlencode(parameters))),
            method='POST',
            headers=headers,
            body=urlencode(post_data))

        if res_headers.status / 100 != 2:
            raise Exception((res_headers, content))

        res = json.loads(content)

        return res

    def get_posts(self, number=100, fields=None, status='publish'):
        '''
        GET /sites/:site/posts/
        '''
        assert (number is not None and
                isinstance(number, int) and
                number <= 100 and number >= 1), number
        assert fields is None or isinstance(fields, (str, unicode)), fields
        assert (status is not None and
                isinstance(status, (str, unicode))), status
        assert status in [
            'publish', 'private', 'draft',
            'pending', 'future', 'trash',
            'any'], status

        h = httplib2.Http(timeout=TIMEOUT)

        headers = {
            'Authorization': '%s %s' % (
                Config.Wordpress('token_type'),
                Config.Wordpress('access_token'))
        }
        parameters = {
            'number': number,
            'status': status
        }

        if fields is not None:
            parameters['fields'] = fields

        (res_headers, content) = h.request(
            self._api_url('/sites/%s/posts/?%s' % (
                Config.Wordpress('site'), urlencode(parameters))),
            method='GET',
            headers=headers)

        if res_headers.status / 100 != 2:
            raise Exception((res_headers, content))

        res = json.loads(content)

        return res['posts']

    # Read
    def get_post(self, id, fields=None):
        '''
        GET /sites/:site/posts/:post_ID
        '''
        assert isinstance(id, int) and id >= 1, id
        assert fields is None or isinstance(fields, (str, unicode)), fields

        h = httplib2.Http(timeout=TIMEOUT)

        headers = {
            'Authorization': '%s %s' % (
                Config.Wordpress('token_type'),
                Config.Wordpress('access_token'))
        }
        parameters = dict()

        if fields is not None:
            parameters['fields'] = fields

        (res_headers, content) = h.request(
            self._api_url('/sites/%s/posts/%d/?%s' % (
                Config.Wordpress('site'), id, urlencode(parameters))),
            method='GET',
            headers=headers)

        if res_headers.status / 100 != 2:
            raise Exception((res_headers, content))

        res = json.loads(content)

        return res

    # Delete
    def delete_post(self, id, fields=None):
        '''
        POST /sites/:site/posts/:post_ID/delete
        '''
        assert isinstance(id, int) and id >= 1, id
        assert fields is None or isinstance(fields, (str, unicode)), fields

        h = httplib2.Http(timeout=TIMEOUT)

        headers = {
            'Authorization': '%s %s' % (
                Config.Wordpress('token_type'),
                Config.Wordpress('access_token'))
        }
        parameters = dict()

        if fields is not None:
            parameters['fields'] = fields

        (res_headers, content) = h.request(
            self._api_url('/sites/%s/posts/%d/delete/?%s' % (
                Config.Wordpress('site'), id, urlencode(parameters))),
            method='POST',
            headers=headers)

        if res_headers.status / 100 != 2:
            raise Exception((res_headers, content))

        res = json.loads(content)

        return res

    def delete_all_posts(self):
        '''
        Delete all the posts
        '''
        posts = self.get_posts(fields='ID,status', status='publish')
        while len(posts) > 0:
            for post in posts:
                print 'Delete %d (%s)' % (post['ID'], post['status'])
                self.delete_post(post['ID'])
            posts = self.get_posts(fields='ID,status', status='publish')

        posts = self.get_posts(fields='ID,status', status='trash')
        while len(posts) > 0:
            for post in posts:
                print 'Delete %d (%s)' % (post['ID'], post['status'])
                self.delete_post(post['ID'])
            posts = self.get_posts(fields='ID,status', status='trash')

        print 'Done!'
