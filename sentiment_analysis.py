from tweepy_streamer import *

def evaluateSentiment(twitter_user, num_of_tweets):
    """
        Returns the user's tweets' mean polarity, mean subjectivity, mean emotive score  (absolute value of polarity) and number of tweets
        Parameters:
        twitter_user (str) : Twitter username (i.e. "senSanders")
        num_of_tweets (int) : the number of tweets to return

        Returns:
        
    """
    twitter_client = TwitterClient(twitter_user=twitter_user)
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name=twitter_user, count=num_of_tweets)
##    tweets = twitter_client.get_user_timeline_tweets(num_of_tweets)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    return (dict({'user': twitter_user, 'num_of_tweets': len(tweets), 'mean_polarity': np.mean(df['polarity']), 'mean_subjectivity': np.mean(df['subjectivity']), 'mean_emotive_score' : np.mean(df['emotive_score']), 'mean_sentiment': np.mean(df['sentiment'])}))

    
num_of_tweets = 200
print(evaluateSentiment('realDonaldTrump', num_of_tweets))
print(evaluateSentiment('senSanders', num_of_tweets))
print(evaluateSentiment('JoeBiden', num_of_tweets))
print(evaluateSentiment('SpeakerRyan', num_of_tweets))
print(evaluateSentiment('BarackObama', num_of_tweets))
print(evaluateSentiment('AndrewYang', num_of_tweets))




