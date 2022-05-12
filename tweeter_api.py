from email import header
from urllib import response
import requests
import json
from datetime import datetime
import dateutil.parser

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAK2KRAEAAAAAW%2BsH09xL6PpxZ%2FalypgTqWxwhcg%3DybBZb0IYIHGmdZOlNQQ4w0dyskNaS2vtF57l7cH11ZJiuy8uuG"

#define search twitter function
def search_twitter(query, tweet_fields, bearer_token = BEARER_TOKEN):
    
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )

    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#search term
query = "bitcoin lang:en"
start_time = dateutil.parser.parse('2022-03-04T12:00:00').isoformat("T") + "Z"
end_time = dateutil.parser.parse('2022-03-05T12:00:00').isoformat("T") + "Z"

#twitter fields to be returned by api call
tweet_fields = f"tweet.fields=text,author_id,created_at&start_time={start_time}&end_time={end_time}&max_results=10"

#twitter api call
json_response = search_twitter(query=query, tweet_fields=tweet_fields, bearer_token=BEARER_TOKEN)

#pretty printing 
print(json.dumps(json_response, indent=4, sort_keys=True))