import requests
import os
from dotenv import load_dotenv
import json


load_dotenv()

api_key = os.getenv("API_KEY")
url = "https://api.twitterapi.io/twitter/community/tweets"
query_string = {"community_id": "1700471046175154612"}
headers = {  "X-API-Key" : api_key  }


def fetchTweets():
    
    if api_key == None:
        print("Invalid API Key")
    else:  
        try:
            response = requests.get(url, headers=headers, params=query_string)
            response.raise_for_status()
            
            with open("community.json", "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
                
            return response.json()
            
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
    
        
with open("tweetDetail.json", "r") as f:
    json_file = json.load(f)
    getRelevantData(json_file)
    f.close()