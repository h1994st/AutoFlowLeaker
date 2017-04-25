#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-11 22:25:15
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

from Twitter import Twitter
from Evernote import Evernote
from Wordpress import Wordpress

# Evernote (ctom357) -> Github (covertsan)
# Wordpress (covertsan.wordpress.com) <- Ghost ()
sender = Evernote()
receiver = Wordpress()
print 'Run'

print 'Clear all'
sender.delete_all_posts()
receiver.clean()

t = Twitter()
print '-----------'


while True:
    results = receiver.receive_all(fields='ID,date,title')

    if len(results) > 0:
        query = results[0].content
        print 'Receive:', query

        results = t._api.GetSearch(
            raw_query='q={0}%20&result_type=recent&count=10'.format(query))
        print dir(results[0])

        res = [{
            'content': status.text,
            'authors': status.user.screen_name,
            'time': status.created_at
        } for status in results]

        print res

        print 'Send response'
        sender.send(
            json.dumps(res), title='Twitter Digest %d' % int(time.time()))

        print 'Clear receiver'
        receiver.delete_all()
    else:
        # print 'Nothing, sleep 1 seconds'
        time.sleep(1)
