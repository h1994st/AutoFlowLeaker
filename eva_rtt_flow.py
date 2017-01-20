#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 23:45:03
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import pytz
import time
import datetime
import argparse
import dateutil.parser

from Ghost import Ghost
from Wordpress import Wordpress


def ghost_to_wordpress(rounds):
    '''
    Trigger Channel: Ghost
    Action Channel: Wordpress

    Description:
    Ghost -> Wordpress (#Inside): Flow
    '''
    print 'Ghost -> Wordpress (#Inside): Flow'

    # Init
    ret = []
    ghost = Ghost()  # Trigger
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
            title = 'Ghost to Wordpress: Evaluate Delay %d %f' % (
                i, time.time())  # attach timestamp: send time

            # Create note in notebook 'Github'
            print 'Publishing a new post on Ghost...'
            ghost_post = ghost.create_post(title, 'body')
            print 'Done!'

            # ISO 8601 datetime string to datetime object, then to unix epoch
            # time zone: UTC
            # real creation time
            timestamp_pair[0] = (
                dateutil.parser.parse(
                    ghost_post['created_at']) - datetime.datetime(
                    1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

            # Check action
            # 1. Get posts
            posts = wordpress.get_posts(
                fields='ID,date,title', tag='Inside')

            # 2. Check
            while len(posts) == 0:
                # no posts
                print 'Sleep 30 seconds'
                time.sleep(30)

                # Get posts
                posts = wordpress.get_posts(
                    fields='ID,date,title', tag='Inside')
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
            # Refresh token
            print 'Refreshing token...'
            ghost._get_new_token()
            print 'Done!'

    # End
    print 'End.'

    # Clear
    print 'Clearing...'
    # Clear trigger channel
    print 'Deleting all posts on Ghost...'
    ghost.delete_all_posts()
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
        description='Experiment: measure performance of automation services')

    # Version
    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0')
    # Rounds
    parser.add_argument(
        '-r', '--round',
        type=int,
        help='the number of rounds',
        required=True)

    (args, _) = parser.parse_known_args()
    print 'Starting program...'

    rounds = args.round
    ret = ghost_to_wordpress(rounds)

    if ret is not None:
        # Saving results
        print 'Saving results...'
        filename = 'ghost_flow_wordpress_%d.json' % (int(time.time()))
        with open('data/rtt/%s' % filename, 'w') as fp:
            json.dump(ret, fp)
        print 'Done!'
