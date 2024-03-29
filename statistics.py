<<<<<<< HEAD
import pandas as pd
from datetime import date, timedelta 

df = pd.read_csv('union\\tweets_btc_2021-01-01_to_2021-12-31.csv')
#df = pd.read_csv('union\\bitcoin_Bitcoin_btc_BTC_Btc_2021-12-31_2022-01-01.csv')
df['Date'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
#print(df.head(-5))
d = date(2021, 12, 30)
#print(d.strftime("%Y-%m-%d"))
print(df[(df.Date==d.strftime("%Y-%m-%d"))])
#print(df[(df.Date=="2021-12-31")])
#print(len(df.index))
#print(df.head())
#df['Date'] = pd.to_datetime(df['Timestamp'], errors='coerce')
#d = date(2021, 12, 31)
=======
import pandas as pd
from datetime import date, timedelta 

df = pd.read_csv('union\\tweets_btc_2021-01-01_to_2021-12-31.csv')
#df = pd.read_csv('union\\bitcoin_Bitcoin_btc_BTC_Btc_2021-12-31_2022-01-01.csv')
df['Date'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
#print(df.head(-5))
d = date(2021, 12, 30)
#print(d.strftime("%Y-%m-%d"))
print(df[(df.Date==d.strftime("%Y-%m-%d"))])
#print(df[(df.Date=="2021-12-31")])
#print(len(df.index))
#print(df.head())
#df['Date'] = pd.to_datetime(df['Timestamp'], errors='coerce')
#d = date(2021, 12, 31)
>>>>>>> 1cd0091f7275821261e24d0e802cf822ad0770f1
#print(df[(df.Date==d.strftime("%Y-%m-%d"))])