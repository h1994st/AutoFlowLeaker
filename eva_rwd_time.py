#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 14:47:17
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import sys
import json
import time

from Email import Email
from Ghost import Ghost
from Github import Github
from Yinxiang import Yinxiang

from Evernote import Evernote
from Wordpress import Wordpress


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
        g.close_issue(issue.number)
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


if __name__ == '__main__':
    def usage():
        print 'Usage: python %s [china|hk|all] <rounds>' % sys.argv[0]

    if len(sys.argv) != 3:
        usage()
        sys.exit(-1)

    if sys.argv[1] not in ['china', 'hk', 'all']:
        usage()
        sys.exit(-1)

    opt = sys.argv[1]
    rounds = int(sys.argv[2])
    print opt

    if opt == 'china':
        mainland(rounds)
    elif opt == 'hk':
        hongkong(rounds)
    else:
        mainland(rounds)
        hongkong(rounds)
