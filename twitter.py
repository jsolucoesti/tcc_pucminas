from ast import keyword
from distutils.command.clean import clean
from itertools import count
from datetime import datetime
from xml.etree.ElementInclude import include
from textblob import TextBlob
import tweepy
import re
import pandas as pd
import matplotlib.pyplot as plt

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAK2KRAEAAAAAW%2BsH09xL6PpxZ%2FalypgTqWxwhcg%3DybBZb0IYIHGmdZOlNQQ4w0dyskNaS2vtF57l7cH11ZJiuy8uuG"


keyword = ("'Bitcoin'")
count = 500
start_date = datetime(2022,1,1,0,0,0).date()

class TweetSearch():

    def __init__(self, bearer_token) -> None:
        '''
        Conecting to twitter with tweepy
        '''
        auth = tweepy.OAuth2BearerHandler(bearer_token)
        self.connected_token = tweepy.API(auth, wait_on_rate_limit=True, retry_count=5, retry_delay=10)
    
    def __clean_tweet(self, tweets_text):
        '''
        Tweet cleaning
        '''
        clean_text = re.sub(r'RT+', '', tweets_text)
        clean_text = re.sub(r'@\S+', '', clean_text)
        clean_text = re.sub(r'https?\S+', '', clean_text)
        clean_text = clean_text.replace("\n"," ")

        return clean_text

    def search_by_keyword(self, keyword, count=5000, result_type='mixed', lang='en', tweet_mode='extended', start_date=datetime.now):
        '''
        Search for the twitters that has commented the keyword subject
        '''
        tweets_founded = tweepy.Cursor(self.connected_token.search_tweets, 
                        q=keyword, tweet_mode=tweet_mode,
                        count=count, result_type=result_type,
                        lang=lang,
                        include_entities=True).items(count)

        return tweets_founded

    def prepare_tweets_list(self, tweets_founded):
        '''
        Transforming the data to DataFrame
        '''

        tweets_data_list = []
        for tweet in tweets_founded:
            if not 'retweeted_status' in dir(tweet):
                tweet_text = self.__clean_tweet(tweet.full_text)
                tweets_data = {
                    'len': len(tweet_text),
                    'ID' : tweet.id,
                    'User' :tweet.user.screen_name,
                    'UserName' : tweet.user.name,
                    'UserLocation' : tweet.user.location,
                    'TweetText' : tweet_text,
                    'Language' : tweet.user.lang,
                    'Date' : tweet.created_at,
                    'Source': tweet.source,
                    'Likes' : tweet.favorite_count,
                    'Retweets' : tweet.retweet_count,
                    'Coordinates' : tweet.coordinates,
                    'Place' : tweet.place
                }

                tweets_data_list.append(tweets_data)

        return tweets_data_list

    def sentiment_polarity(self, tweets_text_list):
        tweets_sentiments_list = []

        for tweet in tweets_text_list:
            polarity = TextBlob(tweet).sentiment.polarity
            if polarity > 0:
                tweets_sentiments_list.append('Positive')
            elif polarity < 0:
                tweets_sentiments_list.append('Negative')
            else:
                tweets_sentiments_list.append('Neutral')
        
        return tweets_sentiments_list

# Testing class
analyzer = TweetSearch(BEARER_TOKEN)

tweets_iter = analyzer.search_by_keyword(keyword, count, start_date)
tweets_list = analyzer.prepare_tweets_list(tweets_iter)

# Analizer result with DataFrame
tweets_df = pd.DataFrame(tweets_list)
print(tweets_df.head())

# Print result
tweets_df['Sentiment'] = analyzer.sentiment_polarity(tweets_df['TweetText'])
sentiment_percentage = tweets_df.groupby('Sentiment')['ID'].count().apply(lambda x:100*x/count)
sentiment_percentage.plot(kind='bar')
plt.show()
plt.savefig('sentiments_tweets.png', bbox_inches='tight', pad_inches=0.5)