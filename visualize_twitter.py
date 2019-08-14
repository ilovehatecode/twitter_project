from tweepy_streamer import *
import matplotlib.pyplot as plt

twitter_client = TwitterClient()
tweet_analyzer = TweetAnalyzer()

api = twitter_client.get_twitter_client_api()

tweets = api.user_timeline(screen_name="realDonaldTrump", count=1000)
print('Number of tweets: {}'.format(len(tweets)))
df = tweet_analyzer.tweets_to_data_frame(tweets)
print(df.head(10))

## Time series
time_likes= pd.Series(data=df['likes'].values, index=df['date'])
time_likes.plot(figsize=(16,4), label='likes', legend=True)


##plt.scatter(df['emotive_score'], df['likes_followers_ratio'], c=(1,0,0))
plt.show()

##Convert dataframe to2d numpy array
X = df['emotive_score'].to_numpy().reshape(-1,1)
Y = df['likes_followers_ratio'].to_numpy().reshape(-1,1)

##Split data into testing and training sets
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=42)


##Train Model
clf = LinearRegression()
clf = clf.fit(X,Y)
##R-squared 
print('Score: {}'.format(clf.score(X, Y)))

