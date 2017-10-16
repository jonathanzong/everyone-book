#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "q6O6czkdYd7K4e47jg7Tpd3Ln"
consumer_secret = "EQhwowi3LB4Mjr5zr7TwWiOiXO6KeK5IqnIDD3z14fR5mE4zgk"
access_key = "871867165837856770-iM1bIwadNRN4DIUWiGnux9yN7dL1bQk"
access_secret = "2iv2dRii8s1XpIHK7e9ogqm2U5gBMxjh9q76Qr9lUXN3T"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode="extended")

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, tweet_mode="extended")

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.retweeted_status.user.screen_name ,tweet.retweeted_status.full_text.encode("utf-8")] for tweet in alltweets if tweet.retweeted_status]

	#write the csv
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(outtweets)

	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("everyonebot")
