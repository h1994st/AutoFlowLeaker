#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-11 22:25:15
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

# from Email import Email
from Github import Github
from Twitter import Twitter
from Wordpress import Wordpress
from auto_flow_leaker import AutoFlowSocket

# Group 1
# Email (covert_zhang@163.com) -> Evernote (ctom357)
# Wordpress (covertsan.wordpress.com) <- Email (covert_tom@163.com)
auto_flow_socket = AutoFlowSocket(
    Github(),
    Wordpress())
# Group 2
# Github () -> Evernote (ctom357)
# Wordpress (covertsan.wordpress.com) <- Github (webmaster)
print 'Run'
print auto_flow_socket

print 'Clear all'
auto_flow_socket.clean()
t = Twitter()
print '-----------'

while True:
    results = auto_flow_socket.receive()

    if len(results) > 0:
        query = results[0].content[3:-5]
        print 'Receive:', query

        results = t._api.GetSearch(
            raw_query='q={0}%20&result_type=recent&count=10'.format(query))
        print dir(results[0])

        res = [{
            'content': status.text,
            'authors': status.user.screen_name,
            'time': status.created_at
        } for status in results]

        print 'Send response'
        auto_flow_socket.send(json.dumps(res), title='Twitter Digest')

        print 'Clear receiver'
        auto_flow_socket.clean_receiver()
    else:
        # print 'Nothing, sleep 1 seconds'
        time.sleep(1)
