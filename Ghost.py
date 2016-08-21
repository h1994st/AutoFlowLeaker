#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-21 00:16:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
from urllib import urlencode

import httplib2

import Config


class Ghost(object):
    """
    Login page: https://covertsan.ghost.io/ghost/signin/
    Login POST url: https://covertsan.ghost.io/ghost/api/v0.1/authentication/token
    Default email: covert.san@gmail.com
    """
    def __init__(self):
        super(Ghost, self).__init__()

        # Login
        self._login()

    @property
    def token_type(self):
        return self._token_type

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def posts(self):
        return self.get_posts(fields='id,title')

    def _login(self):
        '''
        POST https://covertsan.ghost.io/ghost/api/v0.1/authentication/token

        Request Body:
        grant_type: password
        username: covert.san@gmail.com
        password: PolyUSecurity
        client_id: ghost-admin
        client_secret: 961ba3266a2a

        Response Body:
        access_token
        refresh_token
        expires_in
        token_type
        '''
        h = httplib2.Http()

        post_data = {
            'grant_type': 'password',
            'username': Config.Ghost('email'),
            'password': Config.Ghost('password'),
            'client_id': Config.Ghost('client_id'),
            'client_secret': Config.Ghost('client_secret')
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }

        (res_headers, content) = h.request(
            Config.Ghost('token_url'),
            method='POST',
            headers=headers,
            body=urlencode(post_data))

        res = json.loads(content)

        self._token_type = res['token_type']
        self._access_token = res['access_token']
        self._refresh_token = res['refresh_token']

    def _get_new_token(self):
        '''
        POST https://covertsan.ghost.io/ghost/api/v0.1/authentication/token

        Request Body:
        grant_type: refresh_token
        refresh_token: ...
        client_id: ghost-admin
        client_secret: 961ba3266a2a

        Response Body:
        access_token
        expires_in
        token_type
        '''
        h = httplib2.Http()

        post_data = {
            'client_id': Config.Ghost('client_id'),
            'client_secret': Config.Ghost('client_secret'),
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }

        (res_headers, content) = h.request(
            Config.Ghost('token_url'),
            method='POST',
            headers=headers,
            body=urlencode(post_data))

        res = json.loads(content)

        self._token_type = res['token_type']
        self._access_token = res['access_token']

    # Write
    def create_post(self, title, body, status='published'):
        '''
        POST https://covertsan.ghost.io/ghost/api/v0.1/posts/

        title: string
        body: markdown syntax
        status: 'published' (default) or 'draft'

        Request Header:
        Authorization: ...
        Content-Type: application/json

        Request Body:
        {
            "posts": [
                {
                    "author": 1,
                    "title": <title>,
                    "markdown": <body>
                }
            ]
        }

        Response Body:
        If success, the body shows a json string descripting a post object
        '''
        assert isinstance(title, (str, unicode)), title
        assert isinstance(body, (str, unicode)), body
        assert status is not None and isinstance(status, (str, unicode)), status
        assert status in ['published', 'draft'], status

        h = httplib2.Http()

        post_data = {
            'posts': [{
                'author': 1,
                'title': title,
                'markdown': body,
                'status': status
            }]
        }
        headers = {
            'Content-type': 'application/json',
            'Authorization': '%s %s' % (self.token_type, self.access_token)
        }

        (res_headers, content) = h.request(
            'https://covertsan.ghost.io/ghost/api/v0.1/posts/',
            method='POST',
            headers=headers,
            body=json.dumps(post_data))

        if res_headers.status / 100 != 2:
            print (res_headers, content)
            return None

        res = json.loads(content)

        return res['posts'][0]

    def get_posts(self, limit='all', page=1, status='all', fields=None):
        '''
        GET https://covertsan.ghost.io/ghost/api/v0.1/posts/
        '''
        assert isinstance(limit, (int, str, unicode)), limit
        assert (isinstance(limit, int) and limit >= 0) or limit == 'all', limit
        assert isinstance(page, int) and page >= 1, page
        assert (status is not None and
                isinstance(status, (str, unicode))), status
        assert status in ['published', 'draft', 'all'], status
        assert fields is None or isinstance(fields, (str, unicode)), fields

        h = httplib2.Http()

        headers = {
            'Authorization': '%s %s' % (self.token_type, self.access_token)
        }
        parameters = {
            'limit': limit,
            'page': page,
            'status': status
        }

        if fields is not None:
            parameters['fields'] = fields

        (res_headers, content) = h.request(
            'https://covertsan.ghost.io/ghost/api/v0.1/posts/?%s' % urlencode(
                parameters),
            headers=headers)

        if res_headers.status / 100 != 2:
            print (res_headers, content)
            return None

        res = json.loads(content)

        return res['posts']

    # Read
    def get_post(self, id):
        '''
        GET https://covertsan.ghost.io/ghost/api/v0.1/posts/:id/?status=all
        '''
        assert isinstance(id, int) and id >= 1, id

        h = httplib2.Http()

        headers = {
            'Authorization': '%s %s' % (self.token_type, self.access_token)
        }
        parameters = {
            'status': 'all'
        }

        (res_headers, content) = h.request(
            'https://covertsan.ghost.io/ghost/api/v0.1/posts/%d?%s' % (
                id, urlencode(parameters)),
            headers=headers)

        if res_headers.status / 100 != 2:
            print (res_headers, content)
            return None

        res = json.loads(content)

        return res['posts'][0]

    # Delete
    def delete_post(self, id):
        '''
        DELETE https://covertsan.ghost.io/ghost/api/v0.1/posts/:id
        '''
        assert isinstance(id, int) and id >= 1, id

        h = httplib2.Http()

        headers = {
            'Authorization': '%s %s' % (self.token_type, self.access_token)
        }

        (res_headers, content) = h.request(
            'https://covertsan.ghost.io/ghost/api/v0.1/posts/%d' % id,
            method='DELETE',
            headers=headers)

        if res_headers.status / 100 != 2:
            print (res_headers, content)
