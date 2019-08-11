from tweepy_streamer import *

twitter_client = TwitterClient()

tweet_analyzer = TweetAnalyzer()
api = twitter_client.get_twitter_client_api()

tweets = api.user_timeline(screen_name="senSanders", count=400)

df = tweet_analyzer.tweets_to_data_frame(tweets)

## Time series
time_likes= pd.Series(data=df['likes'].values, index=df['date'])
time_likes.plot(figsize=(16,4), label='likes', legend=True)

time_retweets= pd.Series(data=df['retweets'].values, index=df['date'])
time_retweets.plot(figsize=(16,4), label='retweets', legend=True)
plt.show()
