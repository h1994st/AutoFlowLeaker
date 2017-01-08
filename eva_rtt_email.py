#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-08 23:41:03
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import pytz
import time
import datetime
import argparse
import dateutil.parser

from Email import Email
from Wordpress import Wordpress


def email_to_wordpress(rounds):
    '''
    Trigger Channel: Ghost
    Action Channel: Wordpress

    Description:
    Ghost (matches "Ghost to Wordpress") -> Wordpress ("Ghost" #Inside): IFTTT
    '''
    print 'Email -> Wordpress: IFTTT'

    # Init
    ret = []
    email = Email()  # Trigger
    wordpress = Wordpress()  # Action

    # Preparation
    # Clear action channel
    print 'Deleting all posts on Wordpress...'
    wordpress.delete_all_posts()
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        try:
            timestamp_pair = [-1, -1]
            title = 'Email to Wordpress: Evaluate Delay %d %f' % (
                i, time.time())  # attach timestamp: send time

            # Create note in notebook 'Github'
            print 'Sending a new post via Email...'
            email.send_email(title, 'body')
            print 'Done!'

            # Change to sent box
            email.imap_client.select(email.imap_client.get_sent_folder())
            email_post = email.receive()
            # Change back
            email.imap_client.select('inbox')

            # ISO 8601 datetime string to datetime object, then to unix epoch
            # time zone: UTC
            # real creation time
            timestamp_pair[0] = (
                email_post.create_time - datetime.datetime(
                    1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

            # Check action
            # 1. Get posts
            posts = wordpress.get_posts(fields='ID,date,title')

            # 2. Check
            while len(posts) == 0:
                # no posts
                print 'Sleep 2 seconds'
                time.sleep(30)

                # Get posts
                posts = wordpress.get_posts(fields='ID,date,title')
            else:
                # new post
                assert len(posts) == 1, posts

                print 'A new post is published on Wordpress'
                post = posts[0]

                # ISO 8601 datetime string to datetime object, then to unix epoch
                # with time zone
                timestamp = (
                    dateutil.parser.parse(post['date']) - datetime.datetime(
                        1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

                timestamp_pair[1] = timestamp

                print timestamp_pair[1] - timestamp_pair[0], timestamp_pair
                ret.append(timestamp_pair)

                # Close post
                print 'Deleting this post...'
                wordpress.delete_post(post['ID'])
                print 'Done!'
        except Exception:
            pass
        else:
            pass
        finally:
            pass

    # End
    print 'End.'

    # Clear
    print 'Clearing...'
    # Clear trigger channel
    print 'Deleting all posts on Email %r...' % email
    # Change to sent box
    email.imap_client.select(email.imap_client.get_sent_folder())
    email_post = email.delete_all_emails()
    print 'Done!'

    # Clear action channel
    print 'Deleting all posts on Wordpress...'
    wordpress.delete_all_posts()
    print 'Done!'
    print 'Done!'

    return ret


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Experiment: measure performance of automation services' +
                    'when using Email as trigger channel service')

    # Version
    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0')
    # Rounds
    parser.add_argument(
        '-r', '--round',
        type=int,
        help='the number of rounds',
        required=True)
    # Automation service name
    parser.add_argument(
        '--auto',
        choices=['IFTTT', 'Zapier'],
        help='the name of automation service',
        required='True')

    (args, _) = parser.parse_known_args()
    print 'Starting program...'

    rounds = args.round
    auto = args.auto

    ret = None
    if auto == 'Zapier':
        ret = email_to_wordpress_zapier(rounds)
    elif auto == 'IFTTT':
        ret = email_to_wordpress(rounds)
    else:
        print 'Automation flow (email -(%s)> wordpress) does not exist.' % auto

    if ret is not None:
        # Saving results
        print 'Saving results...'
        filename = 'email_%s_wordpress_%d.json' % (
            auto, int(time.time()))
        with open('data/rtt/%s' % filename, 'w') as fp:
            json.dump(ret, fp)
        print 'Done!'
