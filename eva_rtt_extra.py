#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-19 20:56:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import sys
import json
import pytz
import time
import datetime
import argparse

import Notification
from Dropbox import Dropbox
from Twitter import Twitter
from Wordpress import Wordpress


def dropbox_to_twitter(auto_service_name, roungs):
    pass


def twitter_to_dropbox(auto_service_name, rounds):
    if auto_service_name == 'Flow':
        twitter_tags = '#Flow #covert_san #Dropbox'
    else:
        twitter_tags = '#%s' % auto_service_name
    name = 'Twitter ({tags}) -> Dropbox (/{auto})'.format(
        tags=twitter_tags, auto=auto_service_name)
    Notification.get_device('Ines').push_note(
        'eva_rtt: %s' % (auto_service_name), name)
    print name

    # Init
    ret = []
    twitter = Twitter()  # Trigger
    dropbox = Dropbox(folder='/%s' % auto_service_name)  # Action
    print 'Trigger:', twitter
    print 'Action:', dropbox

    trigger_name = type(twitter).__name__
    action_name = type(dropbox).__name__

    # Preparation
    print 'Clearing...'
    # Clear trigger channel
    # print 'Clearing trigger channel...'
    # twitter.delete_all()
    # print 'Done!'

    # Clear action channel
    print 'Clearing action channel...'
    dropbox.delete_all()
    print 'Done!'
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        try:
            timestamp_pair = [-1, -1]
            title = '{tags} Round {round} {timestamp}'.format(
                    tags=twitter_tags,
                    round=i, timestamp=time.time())
            # attach timestamp: send time |\

            # Publish a post on trigger channel
            print 'Publishing a new post on %s...' % trigger_name
            print '  Title:', title
            trigger_post = twitter.send(content=title)
            print 'Done!'

            # real creation time
            timestamp_pair[0] = (
                trigger_post.create_time - datetime.datetime(
                    1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

            # Check action
            # 1. Get posts
            posts = dropbox.receive_all()

            # 2. Check
            while len(posts) == 0:
                # no posts
                print 'Sleep 30 seconds'
                time.sleep(30)

                # Get posts
                posts = dropbox.receive_all()
            else:
                # new post
                assert len(posts) == 1, 'More than one post on action channel'

                print 'Get a new post'
                post = posts[0]

                # ISO 8601 datetime string to datetime object, then to unix epoch
                # with time zone
                timestamp = (
                    post.create_time - datetime.datetime(
                        1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

                timestamp_pair[1] = timestamp

                print timestamp_pair[1] - timestamp_pair[0], timestamp_pair
                Notification.get_device('Ines').push_note(
                    'eva_rtt: %s' % (auto_service_name),
                    'Round %d: %f (%s)' % (
                        i, timestamp_pair[1] - timestamp_pair[0],
                        timestamp_pair))
                ret.append(timestamp_pair)

                # Delete this post on action channel
                print 'Deleting this post on action channel...'
                dropbox.delete(post)
                print 'Done!'
        except Exception as e:
            print 'Error:', e
            Notification.get_device('Ines').push_note(
                'eva_rtt: %s' % (auto_service_name), 'Error: %s' % e)

            print 'Clearing all contents before...'
            # Clear trigger channel
            # print 'Clearing trigger channel...'
            # twitter.delete_all()
            # print 'Done!'

            # Clear action channel
            print 'Clearing action channel...'
            dropbox.delete_all()
            print 'Done!'
            print 'Done!'
        except KeyboardInterrupt:
            print 'KeyboardInterrupt'
            Notification.get_device('Ines').push_note(
                'eva_rtt: %s' % (auto_service_name),
                'KeyboardInterrupt, end with "i=%d"' % i)
            break
        else:
            pass
        finally:
            print 'Sleep 3 seconds'
            time.sleep(3)

    # End
    print 'End.'

    # Clear
    print 'Clearing...'
    # Clear trigger channel
    # print 'Clearing trigger channel...'
    # twitter.delete_all()
    # print 'Done!'

    # Clear action channel
    print 'Clearing action channel...'
    dropbox.delete_all()
    print 'Done!'
    print 'Done!'

    Notification.get_device('Ines').push_note(
        'eva_rtt: %s' % (auto_service_name), 'End!')

    return ret


def dropbox_to_wordpress(auto_service_name, rounds):
    name = 'Dropbox (/{auto}) -> Wordpress (#{auto} "Dropbox")'.format(
        auto=auto_service_name)
    Notification.get_device('Ines').push_note(
        'eva_rtt: %s' % (auto_service_name), name)
    print name

    # Init
    ret = []
    dropbox = Dropbox(folder='/%s' % auto_service_name)  # Trigger
    wordpress = Wordpress()  # Action
    print 'Trigger:', dropbox
    print 'Action:', wordpress

    trigger_name = type(dropbox).__name__
    action_name = type(wordpress).__name__

    # Preparation
    print 'Clearing...'
    # Clear trigger channel
    print 'Clearing trigger channel...'
    dropbox.delete_all()
    print 'Done!'

    # Clear action channel
    print 'Clearing action channel...'
    if auto_service_name != 'Flow':
        wordpress.delete_all(category=trigger_name, tag=auto_service_name)
    else:
        wordpress.delete_all(tag=auto_service_name)
    print 'Done!'
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        try:
            timestamp_pair = [-1, -1]
            title = '{trigger}_{auto}_{action}: ' \
                'Round {round} {timestamp}'.format(
                    trigger=trigger_name,
                    auto=auto_service_name,
                    action=action_name,
                    round=i, timestamp=time.time())
            # attach timestamp: send time |\

            # Publish a post on trigger channel
            print 'Publishing a new post on %s...' % trigger_name
            print '  Title:', title
            trigger_post = dropbox.send('body', title=title)
            print 'Done!'

            # real creation time
            timestamp_pair[0] = (
                trigger_post.create_time - datetime.datetime(
                    1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

            # Check action
            # 1. Get posts
            if auto_service_name != 'Flow':
                posts = wordpress.receive_all(
                    category=trigger_name, tag=auto_service_name)
            else:
                # Flow
                posts = wordpress.receive_all(tag=auto_service_name)

            # 2. Check
            while len(posts) == 0:
                # no posts
                print 'Sleep 30 seconds'
                time.sleep(30)

                # Get posts
                if auto_service_name != 'Flow':
                    posts = wordpress.receive_all(
                        category=trigger_name, tag=auto_service_name)
                else:
                    # Flow
                    posts = wordpress.receive_all(tag=auto_service_name)
            else:
                # new post
                assert len(posts) == 1, 'More than one post on action channel'

                print 'Get a new post'
                post = posts[0]

                # ISO 8601 datetime string to datetime object, then to unix epoch
                # with time zone
                timestamp = (
                    post.create_time - datetime.datetime(
                        1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

                timestamp_pair[1] = timestamp

                print timestamp_pair[1] - timestamp_pair[0], timestamp_pair
                Notification.get_device('Ines').push_note(
                    'eva_rtt: %s' % (auto_service_name),
                    'Round %d: %f (%s)' % (
                        i, timestamp_pair[1] - timestamp_pair[0],
                        timestamp_pair))
                ret.append(timestamp_pair)

                # Delete this post on action channel
                print 'Deleting this post on action channel...'
                wordpress.delete(post)
                print 'Done!'
        except Exception as e:
            print 'Error:', e
            Notification.get_device('Ines').push_note(
                'eva_rtt: %s' % (auto_service_name), 'Error: %s' % e)

            print 'Clearing all contents before...'
            # Clear trigger channel
            # print 'Clearing trigger channel...'
            # dropbox.delete_all()
            # print 'Done!'

            # Clear action channel
            print 'Clearing action channel...'
            if auto_service_name != 'Flow':
                wordpress.delete_all(
                    category=trigger_name, tag=auto_service_name)
            else:
                wordpress.delete_all(tag=auto_service_name)
            print 'Done!'
            print 'Done!'
        except KeyboardInterrupt:
            print 'KeyboardInterrupt'
            Notification.get_device('Ines').push_note(
                'eva_rtt: %s' % (auto_service_name),
                'KeyboardInterrupt, end with "i=%d"' % i)
            break
        else:
            pass
        finally:
            print 'Sleep 3 seconds'
            time.sleep(3)

    # End
    print 'End.'

    # Clear
    print 'Clearing...'
    # Clear trigger channel
    print 'Clearing trigger channel...'
    dropbox.delete_all()
    print 'Done!'

    # Clear action channel
    print 'Clearing action channel...'
    if auto_service_name != 'Flow':
        wordpress.delete_all(category=trigger_name, tag=auto_service_name)
    else:
        wordpress.delete_all(tag=auto_service_name)
    print 'Done!'
    print 'Done!'

    Notification.get_device('Ines').push_note(
        'eva_rtt: %s' % (auto_service_name), 'End!')

    return ret


def wordpress_to_dropbox(auto_service_name, rounds):
    name = 'Wordpress (#{auto} "Dropbox") -> Dropbox (/{auto})'.format(
        auto=auto_service_name)
    Notification.get_device('Ines').push_note(
        'eva_rtt: %s' % (auto_service_name), name)
    print name

    # Init
    ret = []
    wordpress = Wordpress()  # Trigger
    dropbox = Dropbox(folder='/%s' % auto_service_name)  # Action
    print 'Trigger:', wordpress
    print 'Action:', dropbox

    trigger_name = type(wordpress).__name__
    action_name = type(dropbox).__name__

    # Preparation
    print 'Clearing...'
    # Clear trigger channel
    # print 'Clearing trigger channel...'
    # wordpress.delete_all(category=action_name, tag=auto_service_name)
    # print 'Done!'

    # Clear action channel
    print 'Clearing action channel...'
    dropbox.delete_all()
    print 'Done!'
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        try:
            timestamp_pair = [-1, -1]
            title = '{trigger}_{auto}_{action}: Round {round} {timestamp}'.format(
                trigger=trigger_name,
                auto=auto_service_name,
                action=action_name,
                round=i, timestamp=time.time())  # attach timestamp: send time

            # Publish a post on trigger channel
            print 'Publishing a new post on %s...' % trigger_name
            print '  Title:', title
            trigger_post = wordpress.send(
                'body', title=title,
                categories=action_name, tags=auto_service_name)
            print 'Done!'

            # real creation time
            timestamp_pair[0] = (
                trigger_post.create_time - datetime.datetime(
                    1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

            # Check action
            # 1. Get posts
            posts = dropbox.receive_all()

            # 2. Check
            while len(posts) == 0:
                # no posts
                print 'Sleep 30 seconds'
                time.sleep(30)

                # Get posts
                posts = dropbox.receive_all()
            else:
                # new post
                assert len(posts) == 1, 'More than one post on action channel'

                print 'Get a new post'
                post = posts[0]

                # ISO 8601 datetime string to datetime object, then to unix epoch
                # with time zone
                timestamp = (
                    post.create_time - datetime.datetime(
                        1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

                timestamp_pair[1] = timestamp

                print timestamp_pair[1] - timestamp_pair[0], timestamp_pair
                Notification.get_device('Ines').push_note(
                    'eva_rtt: %s' % (auto_service_name),
                    'Round %d: %f (%s)' % (
                        i, timestamp_pair[1] - timestamp_pair[0],
                        timestamp_pair))
                ret.append(timestamp_pair)

                # Delete this post on action channel
                print 'Deleting this post on action channel...'
                dropbox.delete(post)
                print 'Done!'
        except Exception as e:
            print 'Error:', e
            Notification.get_device('Ines').push_note(
                'eva_rtt: %s' % (auto_service_name), 'Error: %s' % e)

            print 'Clearing all contents before...'
            # Clear trigger channel
            # print 'Clearing trigger channel...'
            # wordpress.delete_all(category=action_name, tag=auto_service_name)
            # print 'Done!'

            # Clear action channel
            print 'Clearing action channel...'
            dropbox.delete_all()
            print 'Done!'
            print 'Done!'
        except KeyboardInterrupt:
            print 'KeyboardInterrupt'
            Notification.get_device('Ines').push_note(
                'eva_rtt: %s' % (auto_service_name),
                'KeyboardInterrupt, end with "i=%d"' % i)
            break
        else:
            pass
        finally:
            print 'Sleep 3 seconds'
            time.sleep(3)

    # End
    print 'End.'

    # Clear
    print 'Clearing...'
    # Clear trigger channel
    print 'Clearing trigger channel...'
    wordpress.delete_all(category=action_name, tag=auto_service_name)
    print 'Done!'

    # Clear action channel
    print 'Clearing action channel...'
    dropbox.delete_all()
    print 'Done!'
    print 'Done!'

    Notification.get_device('Ines').push_note(
        'eva_rtt: %s' % (auto_service_name), 'End!')

    return ret


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Experiment: measure performance of automation services')

    supported_channels = ['dropbox', 'wordpress', 'twitter']

    # Version
    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0')
    # Options
    parser.add_argument(
        '-t', '--trigger',
        choices=supported_channels,
        help='trigger channel',
        required=True)
    parser.add_argument(
        '-a', '--action',
        choices=supported_channels,
        help='action channel',
        required=True)
    # Rounds
    parser.add_argument(
        '-r', '--round',
        type=int,
        help='the number of rounds',
        required=True)
    # Automation service name
    parser.add_argument(
        '-A', '--auto',
        choices=['IFTTT', 'Zapier', 'Flow', 'Apiant'],
        help='the name of automation service',
        required=True)

    (args, _) = parser.parse_known_args()
    print 'Starting program...'

    import __main__ as main

    trigger = args.trigger
    action = args.action
    rounds = args.round
    auto = args.auto

    func_name = '%s_to_%s' % (trigger, action)
    func = getattr(main, func_name, None)
    if func is None:
        print 'No such method:', func_name
        sys.exit(-1)

    ret = None
    try:
        ret = func(auto, rounds)
    except Exception as e:
        print unicode(e)

    if ret is not None:
        # Saving results
        print 'Saving results...'
        filename = '%s_%s_%s_%d.json' % (
            trigger, auto, action, int(time.time()))
        with open('data/rtt/%s' % filename, 'w') as fp:
            print '  Dump results to file:', filename
            json.dump(ret, fp)
        print 'Done!'
