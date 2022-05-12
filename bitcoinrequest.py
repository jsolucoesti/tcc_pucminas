import requests
import time
import datetime

class BitcoinRequest:
    def __init__(self, api_key):
        self.api_key = api_key
        self.BASE_URL = 'https://min-api.cryptocompare.com/data/v2'

    def __get_data(self, response):
        return response.json()['Data']['Data']

    def get_dialy_data(self, fsym='BTC', tsym='USD', aggregate=1, limit=365):
      '''
      Get values of bitcoin market
      '''
      response = requests.get(f'{self.BASE_URL}/histoday?fsym={fsym}&tsym={tsym}&aggregate={aggregate}&limit={limit}&api_key={self.api_key}')
      return self.__get_data(response)
    
    def diff_dates(self, date1, date2):
      return abs(date2-date1).days

    def get_index(self, listBT, timestamp):
      '''
      Get a index of bitcoin date
      '''      
      for index in range(len(listBT)):
        if (listBT[index]['time'] == timestamp):
          return index
    
    def get_target_function(self, current_closing, next_closing):
        '''
        Get Z(t) for the hour starting at {time}.
        Z(t) is defined as follows:
            - If there is an increment in the closing price between t and t+1, Z(t) = 1
            - else, Z(t) = -1
        '''
        return 1 if next_closing >= current_closing else -1