from tweepy_streamer import *
from sklearn.linear_model import LinearRegression

##Get Data
twitter_client = TwitterClient()
tweet_analyzer = TweetAnalyzer()

api = twitter_client.get_twitter_client_api()

tweets = api.user_timeline(screen_name="hellomikewalker", count=200)
print('Number of tweets: {}'.format(len(tweets)))
## Preprocess Data - Convert  to 2d numpy array

df = tweet_analyzer.tweets_to_data_frame(tweets)

X = df['emotive_score'].to_numpy().reshape(-1,1)
Y = df['likes'].to_numpy().reshape(-1,1)

##Train 
clf = LinearRegression()
clf = clf.fit(X,Y)

##R-squared 
print('Coefficient of Determination: {}'.format(clf.score(X, Y)))
