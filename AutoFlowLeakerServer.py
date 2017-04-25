#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-11 22:25:15
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

from Email import Email
from Twitter import Twitter
from Wordpress import Wordpress
from auto_flow_leaker import AutoFlowSocket

# Email (covert_zhang@163.com) -> Evernote (ctom357)
# Wordpress (covertsan.wordpress.com) <- Email (covert_tom@163.com)
auto_flow_socket = AutoFlowSocket(
    Email(email='covert_zhang@163.com'),
    Wordpress())
print 'Run'
print auto_flow_socket

auto_flow_socket.clean()
t = Twitter()

while True:
    results = auto_flow_socket.receive()

    if len(results) > 0:
        print 'Receive:'
        query = results[0].content[3:-5]
        print query
        results = t._api.GetSearch(
            raw_query='q={0}%20&result_type=recent&count=10'.format(query))
        print dir(results[0])

        res = [{
            'content': status.text,
            'authors': '',
            'time': ''
        } for status in results]

        auto_flow_socket.clean_receiver()
        auto_flow_socket.send(json.dumps(res), title='Twitter Digest')
    else:
        # print 'Nothing, sleep 1 seconds'
        time.sleep(1)
