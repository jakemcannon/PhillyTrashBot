import csv
import time
import tweepy
from datetime import datetime
from distance import return_nearest_location
from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

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

def reply_to_tweets(path):
	last_seen_id = retrieve_last_seen_id(FILE_NAME)
	mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

	for mention in reversed(mentions):
		print(str(mention.id) + ' -' + mention.full_text, flush=True)
		last_seen_id = mention.id
		if '#nearme' in mention.full_text.lower():
			print('found #nearme!', flush=True)
			print('responding back...', flush=True)
			api.update_status('@' + mention.user.screen_name + 'test' + '#nearme back to you! The nearest location is: ' + path, mention.id)


#currently returns the coordinates but in reverse
def get_coordinates():
	mentions = api.mentions_timeline(tweet_mode='extended')
	for mention in mentions:
		if mention.coordinates is not None and '#nearme' in mention.full_text.lower():
			lat = mention.coordinates['coordinates'][1]
			lon = mention.coordinates['coordinates'][0]
			coords = (lat, lon)
	return lat, lon

my_location = get_coordinates()
# print(coords[0])

destination = return_nearest_location(my_location)
path = "https://www.google.com/maps/dir/?api=1&origin=" + str(my_location).replace(" ", "")[1:-1] + "&destination=" + str(destination).replace("'", "").replace(" ", "")[1:-1]
print(path)


while True:
	reply_to_tweets(path)
	time.sleep(15)




