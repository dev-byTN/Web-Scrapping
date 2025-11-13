import requests
import time
import emoji
import os
import json
from json import JSONEncoder
from typing import List, Dict
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import nbformat
from nbclient import NotebookClient


class Tweet:
    def __init__(self, items=None):
        self.l = items
        
    def __init__(self, username, tweet, date, name, createdAt, followers, following):
        self.username = username
        self.tweet = tweet
        self.date = date
        self.name = name
        self.createdAt = createdAt
        self.followers = followers
        self.following = following
        
    def toDict(self):
        
        return {  "username" : self.username,
                  "tweet" : self.tweet,
                  "date" : self.date,
                  "name" : self.name,
                  "createdAt" : self.createdAt,
                  "followers" : self.followers,
                  "following" : self.following
                }
        
    def __str__(self):
        return { f" {self.username}, {self.tweet}, {self.date}, {self.name}, {self.createdAt}, {self.followers}, {self.following}"}
       
    def toJSON(self): # To make the Object JSON Seriable
        return json.dumps(
            self,
            default=lambda o: o.__dict__)

        
def fetch_all_tweets(query: str, api_key: str, url) -> List[Dict]:  #From their Documentation

    
    headers = {"x-api-key": api_key}
    all_tweets = []
    seen_tweet_ids = set()  
    cursor = None
    last_min_id = None
    max_retries = 50

    while True:
        
        params = {
            "query": query,
            "queryType": "Latest"
        }

        # Add cursor if available (for regular pagination)
        if cursor:
            params["cursor"] = cursor
        elif last_min_id:
            # Add max_id if available (for fetching beyond initial limit)
            params["query"] = f"{query} max_id:{last_min_id}"

        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.get(base_url, headers=headers, params=params)
                response.raise_for_status() 
                data = response.json()

                tweets = data.get("tweets", [])
                has_next_page = data.get("has_next_page", False)
                cursor = data.get("next_cursor", None)

                new_tweets = [tweet for tweet in tweets if tweet.get("id") not in seen_tweet_ids]
                
                for tweet in new_tweets:
                    seen_tweet_ids.add(tweet.get("id"))
                    all_tweets.append(tweet)

                # If no new tweets and no next page, break the loop
                if not new_tweets and not has_next_page:
                    return all_tweets

                # Update last_min_id from the last tweet if available
                if new_tweets:
                    last_min_id = new_tweets[-1].get("id")

                # If no next page but we have new tweets, try with max_id
                if not has_next_page and new_tweets:
                    cursor = None  # Reset cursor for max_id pagination
                    break

                # If has next page, continue with cursor
                if has_next_page:
                    break

            except requests.exceptions.RequestException as e:
                retry_count += 1
                if retry_count == max_retries:
                    print(f"Failed to fetch tweets after {max_retries} attempts: {str(e)}")
                    return all_tweets

                if hasattr(response, 'status_code') and response.status_code == 429: #Rate limit error
                    print("Rate limit reached. Waiting for 1 second...")
                    time.sleep(1)  
                else:
                    break  
                    print(f"Error occurred: {str(e)}. Retrying {retry_count}/{max_retries}")
                    time.sleep(2 ** retry_count)
                    

        # If no more pages and no new tweets with max_id, we're done
        if not has_next_page and not new_tweets:
            break

    return all_tweets


def runNotebook(): #to execute Jupyter Notebook file
    
    with open("cleaning.ipynb", "r") as f:
        nb = nbformat.read(f, as_version=4)
        
    client = NotebookClient(nb)
    client.execute()
        
def readJsonFile():
    
    with open("community.json", "r") as f:
        data = json.load(f)
        
    return data
        
        
def getRelevantData(data):
    
    listOfTweet = []
    for i in data:
        
        tweet = i["text"]
        date = i["createdAt"]
        
        authorInfo = i["author"]
        for j in authorInfo:
            name = authorInfo["name"]
            username = authorInfo["userName"]
            followers = authorInfo["followers"]
            following = authorInfo["following"]
            createdAt = authorInfo["createdAt"]
            
        objectTweet = Tweet(username, tweet, date, name, createdAt, followers, following)   
        objectTweet = objectTweet.toDict() #Save it in JSON Format
        listOfTweet.append(objectTweet)
        
    return listOfTweet

    
def saveTweetsInJson(data):
    
    with open("fetchedTweets.json", "w", encoding="utf8") as f:
        json.dump(data, f, sort_keys=False)
    f.close()

if __name__ == "__main__":
    
    load_dotenv()
    api_key =  os.getenv("API_KEY")
    base_url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    query = "depression lang:fr"
    
    #First we fetch the tweers
    fetch = fetch_all_tweets(query, api_key, base_url)
    print(f"Fetched {len(fetch)} unique tweets")
    
    #Then I get the informations that I want
    result = getRelevantData(fetch)
    saveTweetsInJson(result)
    
    #I clean it into a Jupyter notebook file
    runNotebook()