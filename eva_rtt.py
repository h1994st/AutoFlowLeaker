#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 23:45:03
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

# Automation flows:
# Ghost (matches "Wordpress") -> Wordpress (#Inside): Zapier
# Ghost (matches "Evernote") -> Evernote (#Inside)
# Github (assigned to self) -> Wordpress (#Inside): Zapier
# Github (new closed issue) -> Evernote (notebook "Inside")
# Yinxiang (notebook "Wordpress") -> Wordpress (#Inside)
# Yinxiang (notebook "Github") -> Github (create issue in "covertsan/Yinxiang")
#
# Evernote (notebook "Github") -> Github: Zapier
# Wordpress (#Github) -> Github: Zapier
# Wordpress (#Yinxiang) -> Yinxiang (notebook "Outside")

import json
import time
import datetime
import argparse

from Github import Github
from Wordpress import Wordpress
from Yinxiang import Yinxiang

N = 30
CHANNELS = ['evernote', 'ghost', 'github', 'wordpress', 'yinxiang']


def yinxiang_to_github(rounds):
    print 'Yinxiang (notebook "Github") -> Github (create issue in "covertsan/Yinxiang")'

    # Init
    yinxiang = Yinxiang()  # Trigger
    github = Github()  # Action

    # Get notebook
    notebook = yinxiang.get_notebook(name='Github')  # Write

    # Change repository
    github.change_repo(name='Yinxiang')  # Read, Close

    # Clear
    print 'Deleting all notes in notebook "Github"...'
    yinxiang.delete_notes(notebook=notebook)
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        timestamp_pair = (time.time(), -1)
        title = 'Evaluate Delay %d %f' % (i, timestamp_pair[0])

        # Create note in notebook 'Github'
        print 'Creating a new note in notebook "Github"...'
        yinxiang.create_note(title, '', notebook=notebook)
        print 'Done!'

        # Check
        # 1. Get issues
        issues = github.issues

        # 2. Check
        while len(issues) == 0:
            # no issues
            print 'Sleep 30 seconds'
            time.sleep(30)

            # Get issues
            issues = github.issues
        else:
            # new issue
            assert len(issues) == 1, issues

            print 'A new issue is posted in Github repository "covertsan/Yinxiang"'
            issue = issues[0]

            timestamp = (
                issue['date'] - datetime.datetime(
                    1970, 1, 1)).total_seconds()

            timestamp_pair[1] = timestamp

            print timestamp_pair[1] - timestamp_pair[0], timestamp_pair

            # Close issue
            print 'Closing this issue...'
            github.close_issue(number=issue['number'])
            print 'Done!'
    else:
        # End
        print 'End.'

        # Clear
        print 'Clearing...'
        print 'Deleting all notes in notebook "Github"...'
        yinxiang.delete_notes(notebook=notebook)
        print 'Done!'
        print 'Deleting all issues in repository "covertsan/Yinxiang"'
        github.delete_all_issues()
        print 'Done!'
        print 'Done!'


def wordpress_to_yinxiang(rounds):
    print 'Wordpress (#Yinxiang) -> Yinxiang (notebook "Outside")'

    # Init
    wordpress = Wordpress()  # Trigger
    yinxiang = Yinxiang()  # Action

    # Get notebook
    notebook = yinxiang.get_notebook(name='Outside')  # Write

    # Clear
    print 'Deleting all posts on Wordpress...'
    wordpress.delete_all_posts()
    print 'Done!'
    print 'Deleting all notes in notebook "Outside"...'
    yinxiang.delete_notes(notebook=notebook)
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        timestamp_pair = (time.time(), -1)
        title = 'Evaluate Delay %d %f' % (i, timestamp_pair[0])

        # Create note in notebook 'Github'
        print 'Creating a new note in notebook "Github"...'
        yinxiang.create_note(title, '', notebook=notebook)
        print 'Done!'

        # Check
        # 1. Get posts
        posts = wordpress.get_posts(fields='')

        # 2. Check
        while len(posts) == 0:
            # no issues
            print 'Sleep 30 seconds'
            time.sleep(30)

            # Get posts
            posts = wordpress.get_posts(fields='')
        else:
            # new issue
            assert len(posts) == 1, posts

            print 'A new post is published on Wordpress'

            timestamp = -1

            timestamp_pair[1] = timestamp

            print timestamp_pair[1] - timestamp_pair[0], timestamp_pair
    else:
        # End
        print 'End.'

        # Clear
        print 'Clearing...'
        print 'Deleting all posts on Wordpress...'
        wordpress.delete_all_posts()
        print 'Done!'
        print 'Deleting all notes in notebook "Outside"...'
        yinxiang.delete_notes(notebook=notebook)
        print 'Done!'
        print 'Done!'


def evaluate_rtt(trigger, action, rounds):
    yinxiang = Yinxiang()
    wordpress = Wordpress()

    # Get notebook
    notebook = yinxiang.get_notebook(name='Outside')

    # Clear
    yinxiang.delete_notes()
    wordpress.delete_all_posts()

    for i in xrange(rounds):
        title = 'Evaluate Delay %d' % i
        timestamp = time.time()  # Unix Epoch Timestamp
        note = yinxiang.create_note(title, str(timestamp))
        note.guid  # GUID of created note


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Experiment: measure performance of automation services')

    # Version
    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0')
    # Options
    parser.add_argument(
        '-t', '--trigger',
        choices=CHANNELS,
        help='trigger channel',
        required=True)
    parser.add_argument(
        '-a', '--action',
        choices=CHANNELS,
        help='action channel',
        required=True)
    # Rounds
    parser.add_argument(
        '-r', '--round',
        type=int,
        help='the number of rounds',
        required=True)

    (args, _) = parser.parse_known_args()
    print 'Starting program...'

    trigger = args.trigger
    action = args.action
    rounds = args.round

    yinxiang_to_github(rounds)
