#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 23:45:03
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

# Automation flows:
# Ghost (matches "Wordpress") -> Wordpress (#Inside): Zapier
# Ghost (matches "Evernote") -> Evernote (#Inside)
# Ghost (matches "Yinxiang") -> Yinxiang (notebook "Outside" #Ghost)
# Github (assigned to self) -> Wordpress (#Inside): Zapier
# Github (new closed issue) -> Evernote (notebook "Inside")
# Yinxiang (notebook "Wordpress") -> Wordpress ("Yinxiang" with #Inside)
# Yinxiang (notebook "Github") -> Github (create issue in "covertsan/Yinxiang")
#
# Evernote (notebook "Github") -> Github: Zapier
# Wordpress (#Github) -> Github: Zapier
# Wordpress (#Yinxiang) -> Yinxiang (notebook "Outside")

import json
import pytz
import time
import datetime
import argparse
import dateutil.parser

from Ghost import Ghost
from Github import Github
from Wordpress import Wordpress
from Yinxiang import Yinxiang

N = 30
CHANNELS = ['evernote', 'ghost', 'github', 'wordpress', 'yinxiang']


def yinxiang_to_wordpress(rounds):
    '''
    Trigger Channel: Yinxiang Biji
    Action Channel: Wordpress

    Description: Yinxiang (notebook "Wordpress") -> Wordpress (#Yinxiang)
    '''
    print 'Yinxiang (notebook "Wordpress") -> Wordpress (#Yinxiang)'

    # Init
    yinxiang = Yinxiang()  # Trigger
    wordpress = Wordpress()  # Action

    # Preparation
    # Get notebook
    notebook = yinxiang.get_notebook(name='Wordpress')  # Write

    # Clear action channel
    print 'Deleting all posts on Wordpress...'
    wordpress.delete_all_posts()
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        timestamp_pair = [time.time(), -1]
        title = 'Evaluate Delay %d %f' % (i, timestamp_pair[0])

        # Create note in notebook 'Github'
        print 'Creating a new note in notebook "Wordpress"...'
        yinxiang.create_note(title, 'body', notebook=notebook)
        print 'Done!'

        # Check
        # 1. Get posts
        posts = wordpress.get_posts(
            fields='ID,date,title', category='Yinxiang', tag='Inside')

        # 2. Check
        while len(posts) == 0:
            # no posts
            print 'Sleep 30 seconds'
            time.sleep(30)

            # Get posts
            posts = wordpress.get_posts(
                fields='ID,date,title', category='Yinxiang', tag='Inside')
        else:
            # new post
            assert len(posts) == 1, posts

            print 'A new post is published on Wordpress'
            post = posts[0]

            # ISO 8601 datetime string to datetime object, then to unix epoch
            timestamp = (
                dateutil.parser.parse(post['date']) - datetime.datetime(
                    1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

            timestamp_pair[1] = timestamp

            print timestamp_pair[1] - timestamp_pair[0], timestamp_pair

            # Close post
            print 'Deleting this post...'
            wordpress.delete_post(post['ID'])
            print 'Done!'
    else:
        # End
        print 'End.'

        # Clear
        print 'Clearing...'
        # Clear trigger channel
        print 'Deleting all notes in notebook "Wordpress"...'
        yinxiang.delete_notes(notebook=notebook)
        print 'Done!'

        # Clear action channel
        print 'Deleting all posts on Wordpress...'
        wordpress.delete_all_posts()
        print 'Done!'
        print 'Done!'


def ghost_to_yinxiang(rounds):
    '''
    Trigger Channel: Ghost
    Action Channel: Yinxiang

    Description: Ghost (matches "Yinxiang") -> Yinxiang (notebook "Outside" #Ghost)
    '''
    print 'Ghost (matches "Yinxiang") -> Yinxiang (notebook "Outside" #Ghost)'

    # Init
    ghost = Ghost()  # Trigger
    yinxiang = Yinxiang()  # Action

    # Preparation
    # Get notebook
    notebook = yinxiang.get_notebook(name='Outside')  # Write

    # Clear action channel
    print 'Deleting all notes in notebook "Outside"...'
    yinxiang.delete_notes(notebook=notebook)
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        timestamp_pair = [time.time(), -1]
        title = 'To Yinxiang: Evaluate Delay %d %f' % (i, timestamp_pair[0])

        # Create note in notebook 'Github'
        print 'Publishing a new post on Ghost...'
        ghost.create_post(title, 'body')
        print 'Done!'

        # Check
        # 1. Get notes
        notes = yinxiang.get_notes(notebook=notebook)

        # 2. Check
        while len(notes) == 0:
            # no notes
            print 'Sleep 30 seconds'
            time.sleep(30)

            # Get posts
            notes = yinxiang.get_notes(notebook=notebook)
        else:
            # new note
            assert len(notes) == 1, notes

            print 'A new note is created in notebook "Outside"'
            note = notes[0]

            timestamp_pair[1] = note.created / 1000

            print timestamp_pair[1] - timestamp_pair[0], timestamp_pair

            # Delete this note
            print 'Deleting this note...'
            yinxiang.delete_note(note=note)
            print 'Done!'
    else:
        # End
        print 'End.'

        # Clear
        print 'Clearing...'
        # Clear trigger channel
        print 'Deleting all posts on Ghost...'
        ghost.delete_all_posts()
        print 'Done!'

        # Clear action channel
        print 'Deleting all notes in notebook "Outside"...'
        yinxiang.delete_notes(notebook=notebook)
        print 'Done!'
        print 'Done!'


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
    # print 'Deleting all notes in notebook "Github"...'
    # yinxiang.delete_notes(notebook=notebook)
    # print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        timestamp_pair = [time.time(), -1]
        title = 'Evaluate Delay %d %f' % (i, timestamp_pair[0])

        # Create note in notebook 'Github'
        print 'Creating a new note in notebook "Github"...'
        yinxiang.create_note(title, 'body', notebook=notebook)
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
        # print 'Deleting all notes in notebook "Github"...'
        # yinxiang.delete_notes(notebook=notebook)
        # print 'Done!'
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

        timestamp_pair = [time.time(), -1]
        title = 'Evaluate Delay %d %f' % (i, timestamp_pair[0])

        # Create note in notebook 'Github'
        print 'Creating a new note in notebook "Github"...'
        yinxiang.create_note(title, 'body', notebook=notebook)
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
        choices=['yinxiang', 'ghost'],
        help='trigger channel',
        required=True)
    parser.add_argument(
        '-a', '--action',
        choices=['wordpress', 'yinxiang'],
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

    if trigger == 'yinxiang' and action == 'wordpress':
        yinxiang_to_wordpress(rounds)
    elif trigger == 'ghost' and action == 'yinxiang':
        ghost_to_yinxiang(round)
    else:
        print 'Automation flow (%s -> %s) does not exist.' % (trigger, action)
