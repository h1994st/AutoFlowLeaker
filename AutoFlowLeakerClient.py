#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 19:15:29
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

from Email import Email
from Evernote import Evernote
from auto_flow_leaker import AutoFlowSocket

# Group 1
# Email (covert_tom@163.com) -> Wordpress (covertsan.wordpress.com)
# Evernote (ctom357) <- Email (covert_zhang@163.com)
auto_flow_socket = AutoFlowSocket(
    Email(),
    Evernote())
# Group 2
# -> Wordpress (covertsan.wordpress.com)
# Evernote (ctom357) <-
print 'Run'
print auto_flow_socket

print 'Clear all'
auto_flow_socket.clean()
print '-----------'

query = 'basketball'

results = []

# while True:
for i in xrange(10):
    print 'Round', i
    # Send
    auto_flow_socket.send(query)
    print 'Send:', query
    start = time.time()

    res = auto_flow_socket.receive()

    while len(res) == 0:
        # print 'Nothing, sleep 5 seconds'
        print 'Sleep 5 seconds'
        time.sleep(5)
        res = auto_flow_socket.receive()

    end = time.time()

    print 'Time:', end - start
    results.append(end - start)

    auto_flow_socket.clean_receiver()

filename = 'twitter_%d.json' % (int(time.time()))
with open('data/%s' % filename) as fp:
    json.dump(results, fp)
