from ast import keyword
from distutils.command.clean import clean
from itertools import count
from datetime import datetime
from xml.etree.ElementInclude import include
from textblob import TextBlob
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import tweepy
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
import math
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TweetSearch():
  def __init__(self,  filepath) -> None:
    '''
    Get twittes on file put into dataframe
    '''
    
    self.filepath = filepath
    self.vaderAnalyzer = SentimentIntensityAnalyzer()

  def __clean(self, text):
    '''
    Cleaning a text
    '''
    clean_text = re.sub(r'RT+', '', text)
    clean_text = re.sub(r'@\S+', '', clean_text)
    clean_text = re.sub(r'https?\S+', '', clean_text)
    clean_text = clean_text.replace('\n',' ')
    clean_text = clean_text.replace('Em resposta','')
    clean_text = clean_text.replace('Mostrar esta','')

    return clean_text

  def __clean_retweets(self, text):
    '''
    Cleaning a text
    '''
    if (type(text) == str):
      clean_text = re.sub(r"[a-z]", '', text)
      clean_text = re.sub(r',', '.', clean_text)
    else:
      clean_text = str(text)

    return clean_text

  def clean_tweet(self, tweets_df):
    '''
    Tweets cleaning
    '''
    tweets_data_list = []
    tweets_df = tweets_df.reset_index()
    
    for item in tweets_df.itertuples(index=False):
      tweet_text = self.__clean(item.Embedded_text)
      retweet_text = self.__clean_retweets(item.Retweets)
      tweets_data = {
            'TweetText' : tweet_text,
            'Retweets' : retweet_text
        }
      tweets_data_list.append(tweets_data)
    
    return tweets_data_list

  def prepare_tweets_list(self):
    '''
    Transforming the data to DataFrame
    '''
    tweets_founded = pd.read_csv(self.filepath, header=0, dtype={'UserScreenName': 'str', 'UserName': 'str', 'Timestamp': 'str', 
                                                      'Text': 'str', 'Embedded_text': 'str', 'Emojis' : 'str', 
                                                      'Comments': 'str', 'Likes': 'str', 'Retweets': 'str', 'Imagelink': 'str',  
                                                      'Tweet URL': 'str'})
    new_df = tweets_founded[['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Embedded_text', 'Likes', 'Retweets']]
    new_df = new_df.copy()
    new_df.fillna(0, inplace=True)
    new_df['Date'] = pd.to_datetime(tweets_founded['Timestamp'], errors='coerce')
    new_df['Date'] = new_df['Date'].dt.strftime('%Y-%m-%d')
   
    return new_df

  def sentiment_polarity(self, tweets_text_list):
    '''
    Sentimental polarity
    '''
    tweets_sentiments_list = []
    sentiment_text = ''

    for tweet in tweets_text_list:
        polarity = TextBlob(tweet).sentiment.polarity
        
        if polarity > 0:
            sentiment_text = 'Positive'
        elif polarity < 0:
            sentiment_text = 'Negative'
        else:
            sentiment_text = 'Neutral'
        tweets_sentiment = {
            'Sentiment_Value':polarity,
            'Sentiment_Text' :sentiment_text
        }
        tweets_sentiments_list.append(tweets_sentiment)
    
    return tweets_sentiments_list

  def sentiment_polarity_from_vader(self, tweets_text_list):
    '''
    Sentimental analyse
    '''
    tweets_sentiments_list = []
    sentiment_text = ''

    for tweet in tweets_text_list:
        polarity = self.vaderAnalyzer.polarity_scores(tweet)
        
        if polarity['compound'] >= 0.05:
            sentiment_text = 'Positive'
        elif polarity['compound'] <= -0.05:
            sentiment_text = 'Negative'
        else:
            sentiment_text = 'Neutral'
        tweets_sentiment = {
            'Sentiment_Compound':polarity['compound'],
            'Sentiment_Neutral':polarity['neu'],
            'Sentiment_Negative':polarity['neg'],
            'Sentiment_Positive':polarity['pos'],
            'Sentiment_Text' :sentiment_text
        }
        tweets_sentiments_list.append(tweets_sentiment)
    
    return tweets_sentiments_list

