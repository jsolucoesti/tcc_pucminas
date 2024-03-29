<<<<<<< HEAD
import pandas as pd
import tweetsearch as TweetSearch
import bitcoinrequest as BitcoinRequest
from datetime import date, timedelta 
import time

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
d = date(2021, 10, 18)
sum_pos = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Positive']
sum_neg = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Negative']
sum_neu = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Neutral']
sum_comp = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Compound']
print(f'Data: {d.strftime("%Y-%m-%d")} Soma_Pos:{sum_pos} Soma_Neg:{sum_neg} Soma_neu:{sum_neu} Soma_comp:{sum_comp}')

# Agrupando os dados por dia
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

import time
import datetime

#capture bitcoin data
apy_key = "582a4eea85fa4058d78c6994e9f7af704768d5d5eb93e10dee801962c3695823"

bitcoinRequest = BitcoinRequest(api_key=apy_key)
data_inicial = datetime.datetime(2020, 12, 31)
data_final = datetime.datetime.now()
days = abs(data_inicial-data_final).days
jsonData = bitcoinRequest.get_dialy_data(fsym='BTC', tsym='USD', aggregate=1, limit=days)

# add informations about bitcoin
bt_close = []
bt_open = []
bt_high = []
bt_low = []
bt_volumeto = []
bt_target = []
for item in new_df.itertuples(index=False):
  timestamp = time.mktime(datetime.datetime.strptime(item.date, "%Y-%m-%d").timetuple())
  index = bitcoinRequest.get_index(jsonData, timestamp)
  if index != None:
    bt_close.append(jsonData[index-1]['close'])
    bt_open.append(jsonData[index]['open'])
    bt_high.append(jsonData[index]['high'])
    bt_low.append(jsonData[index]['low'])
    bt_volumeto.append(jsonData[index]['volumeto'])
    bt_target.append(bitcoinRequest.get_target_function(jsonData[index-1]['close'], jsonData[index]['close']))
    
new_df['bt_close'] = bt_close
new_df['bt_open'] = bt_open
new_df['bt_high'] = bt_high
new_df['bt_low'] = bt_low
new_df['bt_volumeto'] = bt_volumeto
new_df['bt_target'] = bt_target

#generate final dataset
=======
import pandas as pd
import tweetsearch as TweetSearch
import bitcoinrequest as BitcoinRequest
from datetime import date, timedelta 
import time

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
d = date(2021, 10, 18)
sum_pos = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Positive']
sum_neg = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Negative']
sum_neu = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Neutral']
sum_comp = tweets_filter[(tweets_filter.Date==d.strftime("%Y-%m-%d"))].sum()['Sentiment_Compound']
print(f'Data: {d.strftime("%Y-%m-%d")} Soma_Pos:{sum_pos} Soma_Neg:{sum_neg} Soma_neu:{sum_neu} Soma_comp:{sum_comp}')

# Agrupando os dados por dia
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

import time
import datetime

#capture bitcoin data
apy_key = "582a4eea85fa4058d78c6994e9f7af704768d5d5eb93e10dee801962c3695823"

bitcoinRequest = BitcoinRequest(api_key=apy_key)
data_inicial = datetime.datetime(2020, 12, 31)
data_final = datetime.datetime.now()
days = abs(data_inicial-data_final).days
jsonData = bitcoinRequest.get_dialy_data(fsym='BTC', tsym='USD', aggregate=1, limit=days)

# add informations about bitcoin
bt_close = []
bt_open = []
bt_high = []
bt_low = []
bt_volumeto = []
bt_target = []
for item in new_df.itertuples(index=False):
  timestamp = time.mktime(datetime.datetime.strptime(item.date, "%Y-%m-%d").timetuple())
  index = bitcoinRequest.get_index(jsonData, timestamp)
  if index != None:
    bt_close.append(jsonData[index-1]['close'])
    bt_open.append(jsonData[index]['open'])
    bt_high.append(jsonData[index]['high'])
    bt_low.append(jsonData[index]['low'])
    bt_volumeto.append(jsonData[index]['volumeto'])
    bt_target.append(bitcoinRequest.get_target_function(jsonData[index-1]['close'], jsonData[index]['close']))
    
new_df['bt_close'] = bt_close
new_df['bt_open'] = bt_open
new_df['bt_high'] = bt_high
new_df['bt_low'] = bt_low
new_df['bt_volumeto'] = bt_volumeto
new_df['bt_target'] = bt_target

#generate final dataset
>>>>>>> 1cd0091f7275821261e24d0e802cf822ad0770f1
new_df.to_csv("matriz_resultado_rede_neural.csv", index=False)