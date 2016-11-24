#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-22 16:11:02
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from pprint import pprint

import twitter

import Config


class Twitter(object):
    '''
    Default user: covert.san@gmail.com
    '''

    def __init__(self):
        self._api = twitter.Api(
            consumer_key=Config.Twitter('consumer_key'),
            consumer_secret=Config.Twitter('consumer_secret'),
            access_token_key=Config.Twitter('access_token_key'),
            access_token_secret=Config.Twitter('access_token_secret'))

    @property
    def tweets(self):
        return self.get_tweets()

    def create_tweet(self, content):
        if len(content) <= 140:
            ret = self._api.PostUpdate(content, trim_user=True)
        else:
            ret = self._api.PostUpdates(content, trim_user=True)

        return ret

    def get_tweet(self, id):
        return self._api.GetStatus(
            id, trim_user=True,
            include_my_retweet=False, include_entities=False)

    def get_tweets(self):
        statuses = self._api.GetUserTimeline(
            trim_user=True, exclude_replies=True)
        return statuses

    def delete_tweet(self, id):
        return self._api.DestroyStatus(id, trim_user=True)

    def delete_all_tweets(self):
        for tweet in self.tweets:
            print 'Delete %d' % tweet.id
            self.delete_tweet(tweet.id)


def test_tw_write():
    tw = Twitter()

    # Read all
    pprint(tw.tweets)

    # Write
    tw.create_tweet('from python auto flow2')

    # Read all
    pprint(tw.tweets)


def test_tw_delete():
    tw = Twitter()

    # Delete all
    tw.delete_all_tweets()


def main():
    tw = Twitter()

    # Read all
    pprint(tw.tweets)

    # Write
    tweet = tw.create_tweet('from python auto flow2')

    # Read all
    pprint(tw.tweets)

    # Delete
    tw.delete_tweet(tweet.id)

    # Read all
    pprint(tw.tweets)


if __name__ == '__main__':
    test_tw_delete()