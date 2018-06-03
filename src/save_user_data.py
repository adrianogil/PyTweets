#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv, os
import sqlite3

import twitter_secret, importutils

import followers

importutils.addpath(__file__, 'entity')
from entity.account import Account
from entity.entityfactory import EntityFactory

importutils.addpath(__file__, 'dao')
from dao.accountdao import AccountDAO

# Open Connection
okane_directory = os.environ['PYTWITTER_DIR'] + '../db/'
conn = sqlite3.connect(okane_directory + 'pytwitter.sqlite');

# Creating cursor
cursor = conn.cursor()

entity_factory = EntityFactory()

accountDAO = AccountDAO(conn, cursor, entity_factory)
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

def save_user_data_into_db(user):
    account = Account(user.screen_name)
    account.bio = user.description
    account.name = user.name
    account.followers = user.followers_count
    account.following = user.friends_count
    account.iam_following = user.following
    account.total_tweets = user.statuses_count

    accountDAO.save(account)

def save_followers_from(twitter_handle):
    max_users = 4000
    following = followers.get_user_followings(api, twitter_handle, max_users)
    for user in following:
        save_user_data_into_db(user)
        user_following = followers.get_user_followings(api, user.screen_name, max_users)
        for u in user_following:
            save_user_data_into_db(u)

def save_user_data(twitter_handle):

    user = api.get_user(twitter_handle)
    save_user_data_into_db(user)
    

if __name__ == '__main__':
    #pass in the username of the account you want to download
    save_followers_from("sandmangil")