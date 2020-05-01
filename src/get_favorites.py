#!/usr/bin/env python
# encoding: utf-8

# https://github.com/tweepy/tweepy
import tweepy
import csv
import sys
import twitter_secret

# Twitter API credentials (Get from https://apps.twitter.com)
consumer_key = twitter_secret.consumer_key
consumer_secret = twitter_secret.consumer_secret
access_key = twitter_secret.access_key
access_secret = twitter_secret.access_secret


def get_all_tweets(screen_name, target_file="%NAME%_favorite_tweets.csv"):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    # Authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Initialize a list to hold all the tweepy Tweets
    alltweets = []

    # Make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.favorites(screen_name, count=200)

    # Save most recent tweets
    alltweets.extend(new_tweets)

    # Save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # Keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.favorites(screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # Transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    # Write the csv
    target_file = target_file.replace("%NAME%", screen_name)

    with open(target_file, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        get_all_tweets("sandmangil", target_file)
    else:
        get_all_tweets("sandmangil")
