import argparse
import json
import requests
import sys

import file_download

from bs4 import BeautifulSoup, SoupStrainer

# Get the subreddit
# TODO: add support for extra command line options
# how many posts? (default=25, max=100)
# what category? (default=hot, others=new,rising,controversial,top)
def get_reddit_page(subreddit):
    url = "http://www.reddit.com/r/" + subreddit + ".json"
    resp = requests.get(url)
    return resp.text

# Find the 'i.imgur.com/' link(s) from 'imgur.com/a/'
def get_url_from_album(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    url_list = []

    for link in soup.select('.album-view-image-link a'):
        url_list.append(link["href"])

    return url_list

# Find the 'i.imgur.com/' link from 'imgur.com/gallery/' or 'imgur.com/'
def get_url_from_gallery(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)

    link = str(soup.find(rel="image_src")["href"])
    if link.endswith('?1'):
        link = link[:len(link)-2]
    return link

# Parse the subreddit data for imgur links
def find_imgur_url(json_str):
    url_list = []
    data = json.loads(json_str)
    reddit_items = data["data"]["children"]

    for item in reddit_items:
        url = item["data"]["url"]
        if "imgur.com/" not in url:
            continue
        elif "i.imgur.com/" in url or str(url).endswith(('.jpeg', '.jpg', '.png', 'gif')):
            url = str(url)
            if url.endswith('?1'): # remove suffix for naming downloaded files later
                url = url[:len(url)-2]
            url_list.append(url)
            #print url
        elif "imgur.com/a/" in url and not "#" in url:
            direct_url_list = get_url_from_album(url)
            url_list = url_list + direct_url_list
            #print direct_url_list
        else:
            direct_url = get_url_from_gallery(url)
            url_list.append(direct_url)
            #print direct_url

    return url_list



def usage():
    print "Usage: python main.py <subreddit-name>"

def 

def main():
    args = sys.argv[1::]

    if len(args) != 1:
        usage()
        sys.exit()

    response = get_reddit_page(args[0])
    url_list = find_imgur_url(response)
    file_download.download_list(args[0], url_list)

main()