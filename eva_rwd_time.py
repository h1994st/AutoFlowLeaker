#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 14:47:17
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time
import argparse

from Email import Email
from Ghost import Ghost
from Github import Github
from Yinxiang import Yinxiang

from Evernote import Evernote
from Wordpress import Wordpress

from Dropbox import Dropbox
from Facebook import Facebook
from Twitter import Twitter


def test_email(data):
    e = Email()
    print 'Email'

    # Write
    print 'Write'
    begin = time.time()
    e.send_email(subject='from py %s hehehehe' % time.time(),
                 text_body=data)
    end = time.time()
    write = end - begin

    # Read: -1
    # Delete: -1

    return (-1, write, -1)


def test_ghost(data):
    try:
        g = Ghost()
        print 'Ghost'

        # Write
        print 'Write'
        begin = time.time()
        post = g.create_post('from py %s' % time.time(), data)
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        g.get_post(post['id'])
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        g.delete_post(post['id'])
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_github(data):
    try:
        g = Github()
        print 'Github'

        # Write
        print 'Write'
        begin = time.time()
        issue = g.create_issue('from py %s' % time.time(), data)
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        g.get_issue(issue.number)
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Close
    print 'Close'
    begin = time.time()
    try:
        g.close_issue(issue=issue)
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_yinxiang(data):
    try:
        y = Yinxiang()
        print 'Yinxiang'

        # Write
        print 'Write'
        begin = time.time()
        note = y.create_note('from py %s' % time.time(), data)
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        y.get_note(note.guid)
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        y.delete_note(note)
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_wordoress(data):
    try:
        w = Wordpress()
        print 'Wordpress'

        # Write
        print 'Write'
        begin = time.time()
        post = w.create_post('from py %s' % time.time(), data)
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        w.get_post(post['ID'])
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        w.delete_post(post['ID'])
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_evernote(data):
    try:
        e = Evernote()
        print 'Evernote'

        # Write
        print 'Write'
        begin = time.time()
        note = e.create_note('from py %s' % time.time(), data)
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        e.get_note(note.guid)
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        e.delete_note(note)
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_facebook(data):
    fb = Facebook()
    print 'Facebook'

    # Write
    print 'Write'
    begin = time.time()
    try:
        post_id = fb.create_post(data)
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        fb.get_post(post_id)
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        fb.delete_post(post_id)
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_twitter(data):
    _data = data[:140]

    tw = Twitter()
    print 'Twitter'

    # Write
    print 'Write'
    begin = time.time()
    try:
        tweet = tw.create_tweet(_data)
    except Exception as e:
        print e
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        tw.get_tweet(tweet.id)
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        tw.delete_tweet(tweet.id)
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_dropbox(data):
    dbx = Dropbox()
    print 'Dropbox'

    # Write
    print 'Write'
    begin = time.time()
    try:
        md = dbx.create_file(data)
    except Exception:
        return (-1, -1, -1)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    try:
        dbx.get_file(md.name)
    except Exception:
        return (-1, write, -1)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        dbx.delete_file(md.name)
    except Exception:
        return (read, write, -1)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def mainland(rounds):
    # emails = []
    ghosts = []
    githubs = []
    yinxiangs = []

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        data = fp.read().strip()

        for i in xrange(rounds):
            print 'Round %d' % i
            # try:
            #     temp = test_email(data)
            # except KeyboardInterrupt:
            #     temp = (-1, -1, -1)
            #     break
            # except:
            #     temp = (-1, -1, -1)
            # finally:
            #     emails.append(temp)
            #     print 'Email:', temp

            try:
                temp = test_ghost(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                ghosts.append(temp)
                print 'Ghost:', temp

            try:
                temp = test_github(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                githubs.append(temp)
                print 'Github:', temp

            try:
                temp = test_yinxiang(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                yinxiangs.append(temp)
                print 'Yinxiang:', temp

    # Save
    print 'Save results...'
    # with open('email_r_time.txt', 'w') as fp:
    #     print 'Email...'
    #     json.dump(emails, fp)

    with open('data/ghost_rwd_time.txt', 'w') as fp:
        print 'Ghost...'
        json.dump(ghosts, fp)

    with open('data/github_rwc_time.txt', 'w') as fp:
        print 'Github...'
        json.dump(githubs, fp)

    with open('data/yinxiang_rwd_time.txt', 'w') as fp:
        print 'Yinxiang...'
        json.dump(yinxiangs, fp)
    print 'Done!'


def hongkong(rounds):
    wordpresses = []
    evernotes = []

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        data = fp.read().strip()

        for i in xrange(rounds):
            print 'Round %d' % i

            try:
                temp = test_wordoress(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                wordpresses.append(temp)
                print 'Wordpress:', temp

            try:
                temp = test_evernote(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                evernotes.append(temp)
                print 'Evernote:', temp

    # Save
    print 'Save results...'
    with open('data/wordpress_rwd_time.txt', 'w') as fp:
        print 'Wordpress...'
        json.dump(wordpresses, fp)

    with open('data/evernote_rwd_time.txt', 'w') as fp:
        print 'Evernote...'
        json.dump(evernotes, fp)
    print 'Done!'


def others(rounds):
    facebooks = []
    twitters = []
    dropboxs = []

    # Clean
    # Facebook().delete_all_posts()
    # Twitter().delete_all_tweets()
    # Dropbox().delete_all_files()

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        data = fp.read().strip()

        for i in xrange(rounds):
            print 'Round %d' % i

            try:
                temp = test_facebook(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                facebooks.append(temp)
                print 'Facebook:', temp

            try:
                temp = test_twitter(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                twitters.append(temp)
                print 'Twitter:', temp

            try:
                temp = test_dropbox(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            finally:
                dropboxs.append(temp)
                print 'Dropbox:', temp

    # Save
    print 'Save results...'
    with open('data/rwd/facebook_rwd_time.txt', 'w') as fp:
        print 'Facebook...'
        json.dump(facebooks, fp)

    with open('data/rwd/twitter_rwd_time.txt', 'w') as fp:
        print 'Twitter...'
        json.dump(twitters, fp)

    with open('data/rwd/dropbox_rwd_time.txt', 'w') as fp:
        print 'Dropbox...'
        json.dump(dropboxs, fp)
    print 'Done!'


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Experiment: measure R/W/D time for each channels')

    # Version
    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0')
    # Options
    parser.add_argument(
        '-t', '--region',
        choices=['china', 'hk', 'others', 'all'],
        help='region',
        required=True)
    # Rounds
    parser.add_argument(
        '-r', '--round',
        type=int,
        help='the number of rounds',
        required=True)

    (args, _) = parser.parse_known_args()
    print 'Starting program...'

    region = args.region
    rounds = args.round
    print region, rounds

    if region == 'china':
        mainland(rounds)
    elif region == 'hk':
        hongkong(rounds)
    elif region == 'others':
        others(rounds)
    else:
        mainland(rounds)
        hongkong(rounds)
        others(rounds)

    print 'Done!'
