import tweepy
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

from config import CONFIG

CONSUMER_KEY = CONFIG['CONSUMER_KEY']
CONSUMER_SECRET = CONFIG['CONSUMER_SECRET']
ACCESS_TOKEN = CONFIG['ACCESS_TOKEN']
ACCESS_SECRET = CONFIG['ACCESS_SECRET']

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


class MyListener(StreamListener):
    def on_data(self, data):
        # print(data)
        try:
            with open('tweets.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#BadDecisionsIHaveMade'])
# twitter_stream.filter(track=['#StrangeThingsToArgueAbout'])
