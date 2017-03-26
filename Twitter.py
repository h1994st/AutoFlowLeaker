#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-22 16:11:02
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import pytz
import time
import dateutil.parser
from pprint import pprint

import twitter

import Config
from auto_flow_leaker.auto_flow.post import Post
from auto_flow_leaker.auto_flow.channel import Channel


class Twitter(Channel):
    '''
    Default user: covert.san@gmail.com
    '''

    def __init__(self):
        super(Twitter, self).__init__()
        self._api = twitter.Api(
            consumer_key=Config.Twitter('consumer_key'),
            consumer_secret=Config.Twitter('consumer_secret'),
            access_token_key=Config.Twitter('access_token_key'),
            access_token_secret=Config.Twitter('access_token_secret'))

    def description(self):
        return 'consumer_key={!r}, consumer_secret={!r}, ' \
            'access_token_key={!r}, access_token_secret={!r}'.format(
                Config.Twitter('consumer_key'),
                Config.Twitter('consumer_secret'),
                Config.Twitter('access_token_key'),
                Config.Twitter('access_token_secret'))

    def send(self, content=None):
        '''
        Default title: unix epoch
        '''
        try:
            tweet = self.create_tweet(content or '%.6f' % time.time())
        except Exception:
            return None
        else:
            return Post(
                id=tweet.id,
                title=None,  # No title
                create_time=dateutil.parser.parse(
                    tweet.created_at).replace(tzinfo=pytz.utc))

    def receive_all(self):
        def converter(tweet):
            return Post(
                id=tweet.id,
                title=None,
                content=tweet.text,
                create_time=dateutil.parser.parse(
                    tweet.created_at).replace(tzinfo=pytz.utc))

        return map(converter, self.get_tweets())

    def delete(self, item):
        self.delete_tweet(item.id)

    def delete_all(self):
        self.delete_all_tweets()

    @property
    def tweets(self):
        return self.get_tweets()

    def create_tweet(self, content):
        '''
        Create a new tweet
        '''
        if len(content) <= 140:
            ret = self._api.PostUpdate(content, trim_user=True)
        else:
            ret = self._api.PostUpdates(content, trim_user=True)

        return ret

    def get_tweet(self, id):
        '''
        Get a tweet
        '''
        return self._api.GetStatus(
            id, trim_user=True,
            include_my_retweet=False, include_entities=False)

    def get_tweets(self):
        '''
        Get all the tweets
        '''
        statuses = self._api.GetUserTimeline(
            trim_user=True, exclude_replies=True)
        return statuses

    def delete_tweet(self, id):
        '''
        Delete a tweet
        '''
        return self._api.DestroyStatus(id, trim_user=True)

    def delete_all_tweets(self):
        '''
        Delete all the tweets
        '''
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


def test_long_tweet():
    tw = Twitter()

    # Read all
    pprint(tw.tweets)

    try:
        # Write
        print 'Input file: ./data/eva_time_data_3.in'
        with open('data/eva_time_data_3.in', 'r') as fp:
            data = fp.read().strip()
            tw.create_tweet(data)
    except Exception as e:
        print e
    else:
        # Read all
        pprint(tw.tweets)


def test_twitter_channel():
    tw = Twitter()
    print tw

    # Read all
    pprint(tw.receive_all())

    tweet = tw.send('test text')
    print tweet

    # Read all
    pprint(tw.receive_all())

    # Delete all
    tw.delete_all()

    # Read all
    pprint(tw.receive_all())


if __name__ == '__main__':
    test_tw_delete()
