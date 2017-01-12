#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-12 02:12:14
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import json
import time

from Email import Email


def test_email_write(data):
    e = Email()
    print 'Email', e

    # Write
    print 'Write'
    begin = time.time()
    try:
        e.send_email(
            subject='from py %s hehehehe' % time.time(),
            text_body=data)
    except Exception:
        return -1
    end = time.time()
    write = end - begin
    return write


def test_email_read():
    e = Email()
    print 'Email', e

    # Read
    print 'Read'
    begin = time.time()
    try:
        email = e.receive()
    except Exception:
        return -1
    end = time.time()
    read = end - begin
    return read, email


def test_email_delete(uid):
    e = Email()
    print 'Email', e

    # Delete
    print 'Delete'
    begin = time.time()
    try:
        e.delete_email(uid)
    except Exception:
        return -1
    end = time.time()
    delete = end - begin
    return delete


def test_email(data):
    e = Email()
    e.delete_all_emails()
    read, write, delete = -1, -1, -1

    # Write
    write = test_email_write(data)

    if write != -1:
        # Read
        read, email = test_email_read()

        # Delete
        delete = test_email_delete(email.id)

    return (read, write, delete)


def main(rounds):
    emails = []

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        data = fp.read().strip()

        for i in xrange(rounds):
            print 'Round %d' % i
            try:
                temp = test_email(data)
            except KeyboardInterrupt:
                temp = (-1, -1, -1)
                break
            except:
                temp = (-1, -1, -1)
            finally:
                emails.append(temp)
                print 'Email:', temp

    # Save
    print 'Save results...'
    with open('email_r_time.txt', 'w') as fp:
        print 'Email...'
        json.dump(emails, fp)

    print 'Done!'


if __name__ == '__main__':
    main(1000)
