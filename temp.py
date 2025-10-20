import requests
import os
from dotenv import load_dotenv
import json
import time


load_dotenv()

api_key = os.getenv("API_KEY")
url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
headers = {  
    "X-API-Key" : api_key  
}




def fetchTweets(query):
    
    seen_tweet_ids = set()  # Set to track unique tweet IDs
    cursor = None
    last_min_id = None
    max_retries = 50
    listt = []
    
    if api_key == None:
        print("Invalid API Key")
        
    else:  
        try:
            query_string = {
                "query" : query,
                "queryType":"Latest",
            }
            
            # Add cursor if available (for regular pagination)
            if cursor:
                query_string["cursor"] = cursor
            elif last_min_id:
                # Add max_id if available (for fetching beyond initial limit)
                query_string["query"] = f"{query} max_id:{last_min_id}"

            for i in range(1,max_retries):

                response = requests.get(url, headers=headers, params=query_string)
                response.raise_for_status()
                data = response.json()
                
                
                listt.append(data)
                time.sleep(5)
                
            print(listt)
            #with open("community.json", "w", encoding="utf-8") as f:
             #  json.dump(listt, f, ensure_ascii=False, indent=4)
                
            #return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"Erreur HTTP : {e}")
        

def getRelevantData(data):
    
    listOfTweet = []
    for i in data["tweets"]:
        
        tweet = i["text"]
        date = i["createdAt"]
        
        authorInfo = i["author"]
        for j in authorInfo:
            name = authorInfo["name"]
            username = authorInfo["userName"]
            followers = authorInfo["followers"]
            following = authorInfo["following"]
            creadtedAt = authorInfo["createdAt"]
            
        list = [username, tweet, date, name, creadtedAt, followers, following]
        listOfTweet.append(list)
    print(list)
    
    
with open("tweetDetail.json", "w") as f:
    json_file = fetchTweets()
    json.dump(json_file, f)
    f.close()
    
#getRelevantData(json_file)