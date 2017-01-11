#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 19:15:29
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import time

from Email import Email
from Evernote import Evernote
from auto_flow_leaker import AutoFlowSocket

# Email (covert_tom@163.com) -> Wordpress (covertsan.wordpress.com)
# Evernote (ctom357) <- Email (covert_zhang@163.com)
auto_flow_socket = AutoFlowSocket(
    Email(),
    Evernote())
print 'Run'
print auto_flow_socket

auto_flow_socket.clean()

auto_flow_socket.send('swift')
print 'Send: Trump'

while True:
    results = auto_flow_socket.receive()

    if len(results) > 0:
        print 'Receive:'
        print results[0].content

        auto_flow_socket.clean_receiver()
    else:
        # print 'Nothing, sleep 3 seconds'
        time.sleep(3)
