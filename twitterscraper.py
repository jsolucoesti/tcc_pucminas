<<<<<<< HEAD
from calendar import month
from datetime import date, timedelta
from multiprocessing.connection import wait
import pandas as pd
from Scweet.scweet import scrape
from textblob import TextBlob
import datetime as dt1
import time

def scrap_tweets(start_date, end_date):
    start_time = time.time()

    with open('logs.txt', 'a+') as f:
        f.write(f"Starting on...\n")
        tweets = scrape(words=['bitcoin','Bitcoin','btc','BTC','Btc'], since=start_date.strftime('%Y-%m-%d'), 
        until=end_date.strftime('%Y-%m-%d'), from_account= None, interval=1, resume=False, filter_replies=False, 
        proximity=False, lang='en', display_type='Latest', limit=1000)
        f.write(f"---- Found {len(tweets)} tweets. ----\n")
        f.write(f"---- Took {time.time() - start_time} seconds ----\n")

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + dt1.timedelta(days=4)
    return next_month - dt1.timedelta(days=next_month.day)

def sentiment_polarity(tweets_text_list):
    '''
    Sentimental analyse
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

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# execute extractions
start_date = date(2021, 1, 1)
end_date = date(2022, 1, 1)
for date in daterange(start_date, end_date):
    date_final = date + timedelta(1)
    scrap_tweets(start_date=date, end_date=date_final)
#    print(f'DataInicial: {date.strftime("%Y-%m-%d")} DataFinal: {date_final.strftime("%Y-%m-%d")}')

#    last_day = last_day_of_month(datetime(2021, i, 1).date()).day
#    for d in range(1, last_day, 1):
#        start_date = datetime(2021, i, d).date()
#        end_date = datetime(2021, i, d+1).date()
#        scrap_tweets(start_date=start_date, end_date=end_date)

#    print(f'data_inicial: {start_date} data_final: {end_date}')
#    end_date = last_day_of_month(start_date)
#    scrap_tweets(start_date=start_date, end_date=end_date)

#start_date = datetime(2021, 1, 1).date()
#end_date = datetime(2021, 1, 2).date()
#scrap_tweets(start_date=start_date, end_date=end_date)

# saving dataset on file
tweets_df = pd.read_csv('outputs\\bitcoin_Bitcoin_btc_BTC_Btc_2021-01-01_2021-01-02.csv')
#print(tweets_df)

'''
tweets_filter2 = tweets_df[['Timestamp', 'Text']] 
tweets_filter2['Date'] = pd.to_datetime(tweets_filter2['Timestamp'], errors='coerce')
tweets_filter2['Date'] = tweets_filter2['Date'].dt.strftime('%Y-%m-%d')

tweets_filter2 = tweets_df[tweets_filter2['Date'] == '2021-01-02']
print(tweets_filter2.shape[0])

tweets_sentiment = pd.DataFrame(sentiment_polarity(tweets_df['Text']))
tweets_df['Sentiment_Value'] = tweets_sentiment['Sentiment_Value']
tweets_df['Sentiment_Text'] = tweets_sentiment['Sentiment_Text']

# Create a new DataFrame without neutral polarity
tweets_filter = tweets_df[tweets_df['Sentiment_Value']!=0]
tweets_filter = tweets_filter[['Timestamp', 'Text', 'Sentiment_Value', 'Sentiment_Text']]

# Tranform field Data to remove hour, min and sec
tweets_filter['Date'] = pd.to_datetime(tweets_filter['Timestamp'], errors='coerce')
tweets_filter['Date'] = tweets_filter['Date'].dt.strftime('%Y-%m-%d')
print(tweets_filter)
print(tweets_filter.describe())
=======
from calendar import month
from datetime import date, timedelta
from multiprocessing.connection import wait
import pandas as pd
from Scweet.scweet import scrape
from textblob import TextBlob
import datetime as dt1
import time

def scrap_tweets(start_date, end_date):
    start_time = time.time()

    with open('logs.txt', 'a+') as f:
        f.write(f"Starting on...\n")
        tweets = scrape(words=['bitcoin','Bitcoin','btc','BTC','Btc'], since=start_date.strftime('%Y-%m-%d'), 
        until=end_date.strftime('%Y-%m-%d'), from_account= None, interval=1, resume=False, filter_replies=False, 
        proximity=False, lang='en', display_type='Latest', limit=1000)
        f.write(f"---- Found {len(tweets)} tweets. ----\n")
        f.write(f"---- Took {time.time() - start_time} seconds ----\n")

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + dt1.timedelta(days=4)
    return next_month - dt1.timedelta(days=next_month.day)

def sentiment_polarity(tweets_text_list):
    '''
    Sentimental analyse
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

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# execute extractions
start_date = date(2021, 1, 1)
end_date = date(2022, 1, 1)
for date in daterange(start_date, end_date):
    date_final = date + timedelta(1)
    scrap_tweets(start_date=date, end_date=date_final)
#    print(f'DataInicial: {date.strftime("%Y-%m-%d")} DataFinal: {date_final.strftime("%Y-%m-%d")}')

#    last_day = last_day_of_month(datetime(2021, i, 1).date()).day
#    for d in range(1, last_day, 1):
#        start_date = datetime(2021, i, d).date()
#        end_date = datetime(2021, i, d+1).date()
#        scrap_tweets(start_date=start_date, end_date=end_date)

#    print(f'data_inicial: {start_date} data_final: {end_date}')
#    end_date = last_day_of_month(start_date)
#    scrap_tweets(start_date=start_date, end_date=end_date)

#start_date = datetime(2021, 1, 1).date()
#end_date = datetime(2021, 1, 2).date()
#scrap_tweets(start_date=start_date, end_date=end_date)

# saving dataset on file
tweets_df = pd.read_csv('outputs\\bitcoin_Bitcoin_btc_BTC_Btc_2021-01-01_2021-01-02.csv')
#print(tweets_df)

'''
tweets_filter2 = tweets_df[['Timestamp', 'Text']] 
tweets_filter2['Date'] = pd.to_datetime(tweets_filter2['Timestamp'], errors='coerce')
tweets_filter2['Date'] = tweets_filter2['Date'].dt.strftime('%Y-%m-%d')

tweets_filter2 = tweets_df[tweets_filter2['Date'] == '2021-01-02']
print(tweets_filter2.shape[0])

tweets_sentiment = pd.DataFrame(sentiment_polarity(tweets_df['Text']))
tweets_df['Sentiment_Value'] = tweets_sentiment['Sentiment_Value']
tweets_df['Sentiment_Text'] = tweets_sentiment['Sentiment_Text']

# Create a new DataFrame without neutral polarity
tweets_filter = tweets_df[tweets_df['Sentiment_Value']!=0]
tweets_filter = tweets_filter[['Timestamp', 'Text', 'Sentiment_Value', 'Sentiment_Text']]

# Tranform field Data to remove hour, min and sec
tweets_filter['Date'] = pd.to_datetime(tweets_filter['Timestamp'], errors='coerce')
tweets_filter['Date'] = tweets_filter['Date'].dt.strftime('%Y-%m-%d')
print(tweets_filter)
print(tweets_filter.describe())
>>>>>>> 1cd0091f7275821261e24d0e802cf822ad0770f1
'''