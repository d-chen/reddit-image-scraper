from bs4 import BeautifulSoup, SoupStrainer
import json
import os
import requests
import sys

DOWNLOAD_DIR = "/downloaded"

def get_reddit_page(subreddit):
    url = "http://www.reddit.com/r/" + subreddit + ".json"
    resp = requests.get(url)
    return resp.text

def get_url_from_album(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    url_list = []

    for link in soup.select('.album-view-image-link a'):
        url_list.append(link["href"])

    return url_list



def find_imgur_url(json_str):
    url_list = []
    data = json.loads(json_str)
    reddit_items = data["data"]["children"]

    for item in reddit_items:
        url = item["data"]["url"]
        if "imgur.com/" not in url:
            continue
        elif "i.imgur.com/" in url:
            url_list.append(str(url)) # direct link, no extra handling
        elif "imgur.com/a/" in url:
            direct_url_list = get_url_from_album(url) # collect all direct links
            url_list = url_list + direct_url_list

    return url_list



def usage():
    print "Usage: python main.py <subreddit-name>"

def main():
    args = sys.argv[1::]

    if len(args) != 1:
        usage()
        sys.exit()

    response = get_reddit_page(args[0])
    url_list = find_imgur_url(response)
    print url_list


main()