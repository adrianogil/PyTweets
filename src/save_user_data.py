#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv, os
import sqlite3

import twitter_secret, importutils

importutils.addpath(__file__, 'entity')
from entity.account import Account

importutils.addpath(__file__, 'dao')
from dao.accountdao import AccountDAO

# Open Connection
okane_directory = os.environ['PYTWITTER_DIR'] + '../db/'
conn = sqlite3.connect(okane_directory + 'pytwitter.sqlite');

# Creating cursor
cursor = conn.cursor()

accountDAO = AccountDAO(conn, cursor, None)
accountDAO.createTables()

# Twitter API credentials (Get from https://apps.twitter.com)
consumer_key = twitter_secret.consumer_key
consumer_secret = twitter_secret.consumer_secret
access_key = twitter_secret.access_key
access_secret = twitter_secret.access_secret

# authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
# Twitter only allows access to a users most recent 3240 tweets with this method
api = tweepy.API(auth)

def save_user_data(twitter_handle):

    user = api.get_user(twitter_handle)

    account = Account(twitter_handle)
    account.bio = user.description
    account.name = user.name
    account.followers = user.followers_count
    account.following = user.friends_count
    account.iam_following = user.following
    account.total_tweets = user.statuses_count

    accountDAO.save(account)

if __name__ == '__main__':
    #pass in the username of the account you want to download
    save_user_data("sandmangil")