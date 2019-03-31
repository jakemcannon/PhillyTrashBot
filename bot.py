import tweepy
import time

from secret import *

print('this is my twitter bot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
#this 'api' object is basically what talks to Twitter, read data, write data
api = tweepy.API(auth)

#what is mentions, a list, object
'''
It returns the below type(), a class
<class 'tweepy.models.ResultSet'>
It is subclass of a Python list, so it is a list like object
https://github.com/tweepy/tweepy/blob/master/tweepy/models.py#L10
Therefore mentions[0] will get you the first tweet
'''
# mentions = api.mentions_timeline()

FILE_NAME = 'last_seen_id.txt'

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
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#nearme' in mention.full_text.lower():
            print('found #nearme', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    '#nearme back to you!', mention.id)

def get_coordinates():
	mentions = api.mentions_timeline(tweet_mode='extended')
	for mention in mentions:
		if mention.coordinates is not None and '#nearme' in mention.full_text.lower():
			print(str(mention.id) + " - " + mention.full_text)
			lat = mention.coordinates['coordinates'][1]
			lon = mention.coordinates['coordinates'][0]
			coords = (lat, lon)
			print("[" + str(lat) + ", " + str(lon) + "]")
	return lat, lon

coordinates = (get_coordinates())

print("This is the coords tuple")
print(coordinates)

while True:
    # reply_to_tweets()
    get_coordinates()
    time.sleep(15)




# for mention in mentions:
# 	# print(str(mention.id) + ' - ' +  mention.text)
# 	if '#nearme' in mention.text.lower():
# 		print('found our keyword! ' + mention.text)
for mention in mentions:
	# print(str(mention.id) + ' - ' +  mention.text)
	if '#nearme' in mention.text.lower():
		print('found our keyword!' + mention.text)
#test
#test t

