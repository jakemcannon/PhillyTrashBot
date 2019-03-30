import tweepy

CONSUMER_KEY = 'X'
CONSUMER_SECRET = 'X'
ACCESS_KEY = 'X'
ACCESS_SECRET = 'X'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

#this 'api object' is basically what talks to Twitter, read data, write data
api = tweepy.API(auth)

print("This is my bot")


mentions = api.mentions_timeline()

for mention in mentions:
	# print(str(mention.id) + ' - ' +  mention.text)
	if '#nearme' in mention.text.lower():
		print('found our keyword!' + mention.text)
#test
#test t
