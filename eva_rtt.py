#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 23:45:03
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

# Automation flows:
# Ghost (matches "Wordpress") -> Wordpress ("Ghost" #Inside): Zapier
# Ghost (matches "Evernote") -> Evernote (#Inside)
# Ghost (matches "Yinxiang") -> Yinxiang (notebook "Outside" #Ghost)
# Github (assigned to self) -> Wordpress (#Inside): Zapier
# Github (new closed issue) -> Evernote (notebook "Inside")
# Yinxiang (notebook "Wordpress") -> Wordpress ("Yinxiang" with #Inside)
# Yinxiang (notebook "Github") -> Github (create issue in "covertsan/Yinxiang")
#
# Evernote (notebook "Github") -> Github (create issue in "covertsan/Evernote"): Zapier
# Wordpress (#Github) -> Github: Zapier
# Wordpress (#Yinxiang) -> Yinxiang (notebook "Outside")

import json
import pytz
import time
import datetime
import argparse
import dateutil.parser

from Evernote import Evernote
from Ghost import Ghost
from Github import Github
from Wordpress import Wordpress
from Yinxiang import Yinxiang


def ghost_to_wordpress(rounds):
    '''
    Trigger Channel: Ghost
    Action Channel: Wordpress

    Description:
    Ghost (matches "Wordpress") -> Wordpress ("Ghost" #Inside): Zapier
    '''
    print 'Ghost (matches "Wordpress") -> Wordpress ("Ghost" #Inside): Zapier'

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
                # with time zone
                timestamp = (
                    dateutil.parser.parse(post['date']) - datetime.datetime(
                        1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

                timestamp_pair[1] = timestamp

                print timestamp_pair[1] - timestamp_pair[0], timestamp_pair
                ret.append(timestamp_pair[1] - timestamp_pair[0])

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
    print 'Deleting all posts on Ghost...'
    ghost.delete_all_posts()
    print 'Done!'

    # Clear action channel
    print 'Deleting all posts on Wordpress...'
    wordpress.delete_all_posts()
    print 'Done!'
    print 'Done!'

    return ret


def evernote_to_github(rounds):
    '''
    Trigger Channel: Evernote
    Action Channel: Github

    Description: Evernote (notebook "Github") -> Github (create issue in "covertsan/Evernote"): Zapier
    '''
    print 'Evernote (notebook "Github") -> Github (create issue in "covertsan/Evernote"): Zapier'

    # Init
    ret = []
    evernote = Evernote()  # Trigger
    github = Github()  # Action

    # Preparation
    # Get notebook
    notebook = evernote.get_notebook(name='Github')  # Write

    # Change repository
    github.change_repo(name='Evernote')  # Read, Close

    # Clear action channel
    print 'Closing all issues in repository "covertsan/Evernote"...'
    github.delete_all_issues()
    print 'Done!'

    # Loop
    for i in xrange(rounds):
        print 'Round %d' % i

        try:
            timestamp_pair = [-1, -1]
            title = 'Evaluate Delay %d %f' % (i, time.time())

            # Create note in notebook 'Github'
            print 'Creating a new note in notebook "Github"...'
            evernote_note = evernote.create_note(
                title, 'body', notebook=notebook)
            print 'Done!'

            # Time stamp, unit: ms
            timestamp_pair[0] = evernote_note.created / 1000

            # Check action channel
            # 1. Get issues
            issues = github.issues

            # 2. Check
            while len(issues) == 0:
                # no posts
                print 'Sleep 30 seconds'
                time.sleep(30)

                # Get issues
                issues = github.issues
            else:
                # new post
                assert len(issues) == 1, issues

                print 'A new issue is posted in Github repository "covertsan/Evernote"'
                issue = issues[0]

                # ISO 8601 datetime string to datetime object, then to unix epoch
                # with time zone
                timestamp = (
                    dateutil.parser.parse(
                        issue['created_at']) - datetime.datetime(
                            1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

                timestamp_pair[1] = timestamp

                print timestamp_pair[1] - timestamp_pair[0], timestamp_pair
                ret.append(timestamp_pair[1] - timestamp_pair[0])

                # Close issue
                print 'Closing this issue...'
                github.close_issue(number=issue['number'])
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
    print 'Deleting all notes in notebook "Github"...'
    evernote.delete_notes(notebook=notebook)
    print 'Done!'

    # Clear action channel
    print 'Closing all issues in repository "covertsan/Evernote"...'
    github.delete_all_issues()
    print 'Done!'
    print 'Done!'

    return ret


def yinxiang_to_wordpress(rounds):
    '''
    Trigger Channel: Yinxiang Biji
    Action Channel: Wordpress

    Description: Yinxiang (notebook "Wordpress") -> Wordpress (#Yinxiang)
    '''
    print 'Yinxiang (notebook "Wordpress") -> Wordpress (#Yinxiang)'

    # Init
    ret = []
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

        try:
            timestamp_pair = [time.time(), -1]
            title = 'Evaluate Delay %d %f' % (i, timestamp_pair[0])

            # Create note in notebook 'Github'
            print 'Creating a new note in notebook "Wordpress"...'
            yinxiang_note = yinxiang.create_note(
                title, 'body', notebook=notebook)
            print 'Done!'

            # Time stamp, unit: ms
            timestamp_pair[0] = yinxiang_note.created / 1000

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
                ret.append(timestamp_pair[1] - timestamp_pair[0])

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
    print 'Deleting all notes in notebook "Wordpress"...'
    yinxiang.delete_notes(notebook=notebook)
    print 'Done!'

    # Clear action channel
    print 'Deleting all posts on Wordpress...'
    wordpress.delete_all_posts()
    print 'Done!'
    print 'Done!'

    return ret


def ghost_to_yinxiang(rounds):
    '''
    Trigger Channel: Ghost
    Action Channel: Yinxiang

    Description: Ghost (matches "Yinxiang") -> Yinxiang (notebook "Outside" #Ghost)
    '''
    print 'Ghost (matches "Yinxiang") -> Yinxiang (notebook "Outside" #Ghost)'

    # Init
    ret = []
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

        try:
            timestamp_pair = [-1, -1]
            title = 'Ghost to Yinxiang: Evaluate Delay %d %f' % (
                i, time.time())

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
                ret.append(timestamp_pair[1] - timestamp_pair[0])

                # Delete this note
                print 'Deleting this note...'
                yinxiang.delete_note(note=note)
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
    print 'Deleting all posts on Ghost...'
    ghost.delete_all_posts()
    print 'Done!'

    # Clear action channel
    print 'Deleting all notes in notebook "Outside"...'
    yinxiang.delete_notes(notebook=notebook)
    print 'Done!'
    print 'Done!'

    return ret


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

        try:
            timestamp_pair = [-1, -1]
            title = 'Yinxiang to Github: Evaluate Delay %d %f' % (
                i, time.time())

            # Create note in notebook 'Github'
            print 'Creating a new note in notebook "Github"...'
            yinxiang_note = yinxiang.create_note(
                title, 'body', notebook=notebook)
            print 'Done!'

            # Time stamp, unit: ms
            timestamp_pair[0] = yinxiang_note.created / 1000

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

                # ISO 8601 datetime string to datetime object, then to unix epoch
                # with time zone
                timestamp = (
                    dateutil.parser.parse(
                        issue['created_at']) - datetime.datetime(
                            1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()

                timestamp_pair[1] = timestamp

                print timestamp_pair[1] - timestamp_pair[0], timestamp_pair

                # Close issue
                print 'Closing this issue...'
                github.close_issue(number=issue['number'])
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
    # print 'Deleting all notes in notebook "Github"...'
    # yinxiang.delete_notes(notebook=notebook)
    # print 'Done!'
    print 'Deleting all issues in repository "covertsan/Yinxiang"...'
    github.delete_all_issues()
    print 'Done!'
    print 'Done!'


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
        choices=['evernote', 'ghost'],
        help='trigger channel',
        required=True)
    parser.add_argument(
        '-a', '--action',
        choices=['wordpress', 'github'],
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
        '--auto',
        choices=['IFTTT', 'Zapier'],
        help='the name of automation service',
        required='True')

    (args, _) = parser.parse_known_args()
    print 'Starting program...'

    trigger = args.trigger
    action = args.action
    rounds = args.round
    auto = args.auto

    ret = None
    if trigger == 'evernote' and action == 'github':
        ret = evernote_to_github(rounds)
    elif trigger == 'ghost' and action == 'wordpress':
        ret = ghost_to_wordpress(rounds)
    else:
        print 'Automation flow (%s -> %s) does not exist.' % (trigger, action)

    if ret is not None:
        # Saving results
        print 'Saving results...'
        filename = '%s_to_%s_%s.json' % (trigger, action, auto)
        with open('data/rtt/%s' % filename, 'w') as fp:
            json.dump(ret, fp)
        print 'Done!'
