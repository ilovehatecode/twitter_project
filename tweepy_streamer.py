from tweepy import API, Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import re
import numpy as np
import pandas as pd
import twitter_credentials
import matplotlib.pyplot as plt



class TwitterClient():
    """
       Class
    """
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client
    
    def get_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)

        return tweets

    def get_friend_list(self, num_friends,):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
                home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_user_timeline_tweets(self, num_tweets):
        user_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
                user_timeline_tweets.append(tweet)
        return user_timeline_tweets
        
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    """
        Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        ## This handles Twitter authentication and the connetion the Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        ##auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        ##auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
    
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    """
        This is basic listener class that prints received tweets to stdout.
    """
        
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
	
    def on_error(self, status):
         ## Return False when rate limit reached
         if status == 420:
             return False
         print(status)
		
		
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        sentiment_score = analysis.sentiment.polarity
        if sentiment_score > 0:
            return 1
        elif sentiment_score == 0:
            return 0
        else:
            return -1

    def get_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment_assessments

    def get_subjectivity_score(self, tweet):
        return self.get_sentiment( self.clean_tweet(tweet)).subjectivity

    def get_polarity_score(self, tweet):
        return self.get_sentiment( self.clean_tweet(tweet)).polarity

    def get_assessments(self, tweet):
        return self.get_sentiment(self.clean_tweet(tweet)).assessments




    def tweets_to_data_frame(self, tweets):
        """
           Create data frame of tweets with selected fields
           returns
           emotive score is the absolute value of polarity
           
        """
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['followers'] = np.array([tweet.user.followers_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['sentiment'] = np.array([self.analyze_sentiment(tweet) for tweet in df['tweets']])
        df['emotive_score'] = np.array([abs(self.get_polarity_score(tweet)) for tweet in df['tweets']])
        df['polarity'] = np.array([self.get_polarity_score(tweet) for tweet in df['tweets']])
        df['subjectivity'] = np.array([self.get_subjectivity_score(tweet) for tweet in df['tweets']])
        df['likes_followers_ratio'] = np.array([ float(tweet.favorite_count) / tweet.user.followers_count for tweet in tweets])
 ##       df['assessments'] = np.array([self.get_assessments(tweet) for tweet in df['tweets']])
        return df











	

