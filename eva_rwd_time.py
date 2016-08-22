#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 14:47:17
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

from Email import Email
from Ghost import Ghost
from Github import Github
from Yinxiang import Yinxiang


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
    g = Ghost()
    print 'Ghost'

    # Write
    print 'Write'
    begin = time.time()
    post = g.create_post('from py %s' % time.time(), data)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    g.get_post(post['id'])
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    g.delete_post(post['id'])
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_github(data):
    g = Github()
    print 'Github'

    # Write
    print 'Write'
    begin = time.time()
    issue = g.create_issue('from py %s' % time.time(), data)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    g.get_issue(issue.number)
    end = time.time()
    read = end - begin

    # Close
    print 'Close'
    begin = time.time()
    g.close_issue(issue.number)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def test_yinxiang(data):
    y = Yinxiang()
    print 'Yinxiang'

    # Write
    print 'Write'
    begin = time.time()
    note = y.create_note('from py %s' % time.time(), data)
    end = time.time()
    write = end - begin

    # Read
    print 'Read'
    begin = time.time()
    y.get_note(note.guid)
    end = time.time()
    read = end - begin

    # Delete
    print 'Delete'
    begin = time.time()
    y.delete_note(note)
    end = time.time()
    delete = end - begin

    return (read, write, delete)


def main():
    # emails = []
    ghosts = []
    githubs = []
    yinxiangs = []

    with open('data/eva_time_data_2.in', 'r') as fp:
        data = fp.read().strip()

        for i in xrange(1000):
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
            except:
                temp = (-1, -1, -1)
            finally:
                ghosts.append(temp)
                print 'Ghost:', temp

            try:
                temp = test_github(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            except:
                temp = (-1, -1, -1)
            finally:
                githubs.append(temp)
                print 'Github:', temp

            try:
                temp = test_yinxiang(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            except:
                temp = (-1, -1, -1)
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


if __name__ == '__main__':
    main()