#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 19:15:29
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

from Ghost import Ghost
from Github import Github

# Ghost (?) -> Wordpress (covertsan.wordpress.com)
# Github (covertsan) <- Evernote (ctom357)
sender = Ghost()
receiver = Github()
print 'Run'

print 'Clear all'
sender.delete_all_posts()
receiver.clean()
print '-----------'

query = 'basketball'

results = []

# while True:
for i in xrange(10):
    print 'Round', i
    # Send
    sender.create_issue(str(time.time()), query)
    print 'Send:', query
    start = time.time()

    res = receiver.issues

    while len(res) == 0:
        # print 'Nothing, sleep 5 seconds'
        print 'Sleep 5 seconds'
        time.sleep(5)
        res = receiver.issues

    end = time.time()

    print 'Time:', end - start
    results.append(end - start)

    receiver.clean()

filename = 'twitter_%d.json' % (int(time.time()))
with open('data/%s' % filename) as fp:
    json.dump(results, fp)
