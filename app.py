import csv
import time
import tweepy
import urllib.parse
from datetime import datetime
from distance import return_nearest_location
from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

FILE_NAME = 'last_seen_id.txt'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
api = tweepy.API(auth)

mentions = api.mentions_timeline()

for mention in mentions:
	# print(str(mention.id) + ' - ' +  mention.text)
	if '#nearme' in mention.text.lower():
		print('found our keyword!' + mention.text)

# get last seen id for store id func
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
	mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

	for mention in reversed(mentions):
		print(str(mention.id) + ' -' + mention.full_text, flush=True)
		last_seen_id = mention.id
		store_last_seen_id(last_seen_id, FILE_NAME)
		if mention.coordinates is not None and '#nearme' in mention.full_text.lower():
			my_location = get_coordinates(mention)
			url = create_url(my_location)
			print('found #nearme!', flush=True)
			print('responding back...', flush=True)
			print(mention.coordinates)
			print(mention.created_at)
			api.update_status('@' + mention.user.screen_name + ' Here is the nearest waste bin is:' + url + mention.created_at, mention.id)
		else:
			api.update_status('@' + mention.user.screen_name + ' You did not provide any location data in your tweet. Please read the pinned tweet for instructions!', mention.id)


#currently returns the coordinates but in reverse
def get_coordinates(mention):
	lat = mention.coordinates['coordinates'][1]
	lon = mention.coordinates['coordinates'][0]
	coords = (lat, lon)
	return lat, lon

def create_url(my_location):
	destination = return_nearest_location(my_location)
	url = "https://www.google.com/maps/dir/?api=1&"
	params = {'origin': str(my_location[0]) + ',' + str(my_location[1]), 'destination': str(destination[0]) + ',' + str(destination[1])}
	result = url + urllib.parse.urlencode(params) + '&travelmode=walking'
	return result


while True:
	reply_to_tweets()
	time.sleep(15)


