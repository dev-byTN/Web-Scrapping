import requests
from bs4 import BeautifulSoup as bs
#from selenium import webdriver
headers = {"user-agent" : "toto"}
response = requests.get("https://httpbin.org/user-agent", headers = headers)
response.json()