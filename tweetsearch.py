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

#instanciando a classe
analyzer = TweetSearch('tweets_btc_2021-01-01_to_2021-12-31.csv')
#transformando em Dataframe
tweets_df = analyzer.prepare_tweets_list()
#realizando a limpeza dos tweets
tweets_cleaned = analyzer.clean_tweet(tweets_df)
tweets_cleaned_df = pd.DataFrame(tweets_cleaned)
tweets_df['TweetTextClean'] = tweets_cleaned_df['TweetText']
#realizando a analise de sentimentos com VADER
tweets_sentiment = analyzer.sentiment_polarity_from_vader(tweets_df['TweetTextClean'])
tweets_sentiment = pd.DataFrame(tweets_sentiment)

#data analyser
#criando as novas colunas on DataFrame
tweets_df[['Sentiment_Compound', 'Sentiment_Neutral', 'Sentiment_Negative', 'Sentiment_Positive', 'Sentiment_Text']] = 
tweets_sentiment[['Sentiment_Compound', 'Sentiment_Neutral', 'Sentiment_Negative', 'Sentiment_Positive', 'Sentiment_Text']]
#gerando um novo dataframe somente com as informações necessarias nas próximas etapas
tweets_filter = tweets_df[['Date', 'TweetTextClean', 'Sentiment_Compound', 'Sentiment_Neutral', 'Sentiment_Negative', 'Sentiment_Positive', 'Sentiment_Text']]
#vizualizando a ultima linha do dataset
tweets_filter.iloc[-1]

# Testando proximo passo
from datetime import date, timedelta 
d = date(2021, 10, 18)
sum_pos = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Positive']
sum_neg = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Negative']
sum_neu = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Neutral']
sum_comp = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Compound']
print(f'Data: {d.strftime("%Y-%m-%d")} Soma_Pos:{sum_pos} Soma_Neg:{sum_neg} Soma_neu:{sum_neu} Soma_comp:{sum_comp}')

# Agrupando os dados por dia
from datetime import date, timedelta 
import time

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def groupTweetsByDay(tweets):
  # Grouping tweets by day
  start_date = date(2021, 1, 1)
  end_date = date(2022, 1, 1)
  dtypes = np.dtype([('date', str),('neu_mean', float), ('neg_mean', float), ('pos_mean', float), ('comp_mean', float), ('pol_mean', float), ('qtd_day', int)])
  new_df = pd.DataFrame(np.empty(0, dtype=dtypes))

  for d in daterange(start_date, end_date):
    sum_neu = tweets[(tweets.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Neutral']
    sum_neg = tweets[(tweets.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Negative']
    sum_pos = tweets[(tweets.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Positive']
    sum_comp = tweets[(tweets.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Compound']
    total_tweets_of_day = tweets[(tweets.Date==d.strftime("%Y-%m-%d"))].count()['Date']
    new_row = {
         'date': d.strftime("%Y-%m-%d"), 
         'neu_mean': sum_neu/total_tweets_of_day, 
         'neg_mean': sum_neg/total_tweets_of_day, 
         'pos_mean': sum_pos/total_tweets_of_day, 
         'comp_mean': sum_comp/total_tweets_of_day, 
         'pol_mean': math.sqrt(sum_pos/total_tweets_of_day * sum_neg/total_tweets_of_day),
         'qtd_day': total_tweets_of_day
         }
    new_df = new_df.append(new_row, ignore_index=True)
    
  return new_df

#grouping data per day
new_df = groupTweetsByDay(tweets_filter)