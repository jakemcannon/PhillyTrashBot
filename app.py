import csv
import time
import tweepy
import urllib.parse
from datetime import datetime
from distance import return_nearest_location_coordinates
from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

FILE_NAME = 'last_seen_id.txt'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
api = tweepy.API(auth)

def retrieve_last_seen_id(file_name):
	f_read = open(file_name, 'r')
	last_seen_id = int(f_read.read().strip())
	f_read.close()
	return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
	f_write = open(file_name, 'w')
	f_write.write(str(last_seen_id))
	f_write.close()
	return

def reply_to_tweets():

	last_seen_id = retrieve_last_seen_id(FILE_NAME)

	# http://docs.tweepy.org/en/latest/api.html
	mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
	for mention in mentions:
		last_seen_id = mention.id
		store_last_seen_id(last_seen_id, FILE_NAME)
		if mention.coordinates is not None and '#nearme' in mention.full_text.lower():
			my_location = get_coordinates(mention)
			url = build_url(my_location)
			api.update_status('@' + mention.user.screen_name + ' Here is the nearest waste bin, created at : ' + str(mention.created_at) + " " + url, mention.id)
		else:
			api.update_status('@' + mention.user.screen_name + ' You did not provide any location data in your tweet. Please read the pinned tweet for instructions! ' + str(mention.created_at), mention.id)

def get_coordinates(mention):
	lat = mention.coordinates['coordinates'][1]
	lon = mention.coordinates['coordinates'][0]
	return lat, lon


def build_url(my_location):
	# destination, the google maps parameter, is the nearest waste bin
	destination = return_nearest_location_coordinates(my_location)
	url = "https://www.google.com/maps/dir/?api=1&"
	params = {'origin': str(my_location[0]) + ',' + str(my_location[1]), 'destination': str(destination[0]) + ',' + str(destination[1])}
	result = url + urllib.parse.urlencode(params) + '&travelmode=walking'
	return result

while True:
	reply_to_tweets()
	time.sleep(15)



