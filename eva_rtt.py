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
#
# Evernote (notebook "Github") -> Github: Zapier
# Wordpress (#Github) -> Github: Zapier
# Wordpress (#Yinxiang) -> Yinxiang (notebook "Outside")

import json
import time
import argparse

import Config
from Ghost import Ghost
from Github import Github
from Wordpress import Wordpress

N = 30


def github_to_wordpress(n):
    results = []

    github = Github()
    wordpress = Wordpress()

    issues = github.issues
    posts = wordpress.posts

    if len(issues) != 0:
        print 'Clear Github issues'
        github.delete_all_issues()

    if len(posts) != 0:
        print 'Clear Wordpress posts'
        wordpress.delete_all_posts()

    for i in xrange(n):
        title = 'Github to Wordpress %d' % i

        # New issue
        print 'Create a new issue on Github'
        issue = github.create_issue(
            title, body=title, assignee=Config.Github('username'))

        # Wait for trigger
        created_at = issue.created_at  # Timestamp

        while True:
            w_posts = wordpress.get_posts(fields='ID,title,date')
            if len(w_posts) == 0:
                print 'Sleep 5 seconds'
                time.sleep(5)
                continue

            w_post = w_posts[0]

            if w_post['title'].lower() == title.lower():
                break

        w_created_at = w_post['date']

        # Done!
        print 'Done!'

        # Save results
        print 'Save results'
        print (created_at, w_created_at)
        results.append((created_at, w_created_at))

        # Clear
        print 'Delete posts'
        github.close_issue(issue.number)
        wordpress.delete_post(w_post['ID'])

    print 'Save results...'
    with open('data/github_to_wordpress_rtt_time.json', 'w') as fp:
        print 'Github to Wordpress...'
        json.dump(results, fp)
    print 'Done!'


def ghost_to_wordpress(n):
    results = []

    ghost = Ghost()
    wordpress = Wordpress()

    # 0. Clear Ghost & Wordpress
    print 'Clear Ghost posts'
    ghost.delete_all_posts()

    print 'Clear Wordpress posts'
    wordpress.delete_all_posts()

    # 1. Generate content:
    #    title
    #    timestamp
    #    content

    for i in xrange(n):
        title = 'Ghost2222222WordPress %d' % i

        # New post
        print 'Create a new post on Ghost Blog'
        post = ghost.create_post(title, title)

        # Wait for trigger
        created_at = post['created_at']  # Timestamp

        while True:
            w_posts = wordpress.get_posts(fields='ID,title,date')
            if len(w_posts) == 0:
                print 'Sleep 5 seconds'
                time.sleep(5)
                continue

            w_post = w_posts[0]

            if w_post['title'].lower() == title.lower():
                break

        w_created_at = w_post['date']

        # Done!
        print 'Done!'

        # Save results
        print 'Save results'
        print (created_at, w_created_at)
        results.append((created_at, w_created_at))

        # Clear
        print 'Delete posts'
        ghost.delete_post(post['id'])
        wordpress.delete_post(w_post['ID'])

    print 'Save results...'
    with open('data/ghost_to_wordpress_rtt_time.json', 'w') as fp:
        print 'Ghost to Wordpress...'
        json.dump(results, fp)
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
        '-c', '--channel',
        choices=['ghost_to_wordpress', 'github_to_wordpress'],
        help='channel',
        required=True)
    # Rounds
    parser.add_argument(
        '-r', '--round',
        type=int,
        help='the number of rounds',
        required=True)

    (args, _) = parser.parse_known_args()
    print 'Starting program...'

    channel = args.channel
    rounds = args.round
    print channel, rounds

    if channel == 'ghost_to_wordpress':
        ghost_to_wordpress(rounds)
    elif channel == 'github_to_wordpress':
        github_to_wordpress(rounds)
