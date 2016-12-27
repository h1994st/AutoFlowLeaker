#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-30 00:25:44
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import time

import requests
from lxml import html

import Config


class IFTTT(object):
    '''
    Default user: covertsan (covert.san@gmail.com)
    '''
    def __init__(self,
                 username=Config.IFTTT('email1'),
                 password=Config.IFTTT('password')):
        super(IFTTT, self).__init__()

        self.username = username
        self._is_login = False
        self._session_requests = requests.session()

        self._login(username, password)

    @property
    def is_login(self):
        return self._is_login

    def _login(self, username, password):
        # Get authenticity token
        login_page_url = 'https://ifttt.com/login'
        result = self._session_requests.get(login_page_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(
            set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

        payload = {
            'utf8': '✓',
            'user[username]': username,
            'user[password]': password,
            'commit': 'Sign in',
            'authenticity_token': authenticity_token,
            'return_to': ''
        }

        # Log in
        login_url = 'https://ifttt.com/session'
        result = self._session_requests.post(
            login_url,
            data=payload,
            headers=dict(referer=login_url)
        )
        if result.status_code != 200:
            print 'Login failed!'
            return
        self._is_login = True

        url = 'https://ifttt.com/my_applets'
        result = self._session_requests.get(
            url,
            data=payload,
            headers=dict(referer=url)
        )
        tree = html.fromstring(result.content)
        bucket_elems = tree.cssselect(
            'li.my-web-applet-card.enabled_for_user.web-applet-card')

        # Get ids (applet-*)
        self.applet_ids = [elem.get('id')[7:] for elem in bucket_elems]

    def force_check(self, applet_id):
        if not self.is_login:
            raise Exception('Not login')

        # Get CSRF token
        applet_page_url = 'https://ifttt.com/applets/%s' % applet_id
        result = self._session_requests.get(applet_page_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(
            set(tree.xpath("//meta[@name='csrf-token']/@content")))[0]

        check_url = 'https://ifttt.com/services/feed/applets/%s/check' % (
            applet_id)
        result = self._session_requests.post(
            check_url,
            headers={
                'referer': applet_page_url,
                'X-CSRF-Token': authenticity_token
            })
        print result.status_code

    def force_check_all(self):
        if not self.is_login:
            raise Exception('Not login')
        for applet_id in self.applet_ids:
            self.force_check(applet_id)


if __name__ == '__main__':
    ifttt = IFTTT()

    print ifttt.applet_ids

    i = 0
    while True:
        i += 1
        ifttt.force_check('xxx')
        print '%d: Sleep 2 seconds' % i
        time.sleep(2)
