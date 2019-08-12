from tweepy_streamer import *
import matplotlib.pyplot as plt
twitter_client = TwitterClient()
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
tweet_analyzer = TweetAnalyzer()
import logging

api = twitter_client.get_twitter_client_api()

tweets = api.user_timeline(screen_name="senSanders", count=400)

df = tweet_analyzer.tweets_to_data_frame(tweets)
print(df.head(10))
## Time series
##time_likes= pd.Series(data=df['likes'].values, index=df['date'])
####time_likes.plot(figsize=(16,4), label='likes', legend=True)
##
##time_retweets= pd.Series(data=df['likes'].values, index=df['polarity'])
##time_retweets.plot(figsize=(16,4), label='polarity', legend=True)

plt.scatter(df['emotive_score'], df['retweets'], c=(1,0,0))
plt.show()

##Convert dataframe to2d numpy array
X = df['emotive_score'].to_numpy().reshape(-1,1)
Y = df['retweets'].to_numpy().reshape(-1,1)

##Split data into testing and training sets
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=42)


##Train Model
clf = LinearRegression()
clf = clf.fit(X,Y)
##R-squared 
print('Score: {}'.format(clf.score(X, Y)))

