import argparse
import json
import requests
import sys

import file_download

from bs4 import BeautifulSoup, SoupStrainer

# Get the subreddit
def get_reddit_page(subreddit, post_type, limit, time):
    url =   "http://www.reddit.com/r/" + subreddit + "/" + post_type + \
            ".json" + "?limit=" + str(limit)

    if post_type == "top" and not time == "hour":
        url = url + "?sort=top&t=" + time

    print "Retrieving page: " + url
    resp = requests.get(url)
    return resp.text


# Find the 'i.imgur.com/' link(s) from 'imgur.com/a/'
def get_url_from_album(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    url_list = []

    for link in soup.select('.album-view-image-link a'):
        url = link["href"]
        
        if not url.startswith("http:"):
            url = "http:" + url

        url_list.append(url)

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


def main():
    parser = argparse.ArgumentParser(description="Download Imgur images from specified subreddit")
    parser.add_argument("subreddit", help="Subreddit to download from")

    parser.add_argument("-l", "--limit", type=int, default=25, help="Maximum number of posts [default:25 max:100]")
    parser.add_argument("-t", "--time", choices=['hour', 'day', 'week', 'month', 'year', 'all'], default='day', help="Time period to check [default: day]")

    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument("--hot", action="store_true", help="Download hot posts [default]")
    type_group.add_argument("--controversial", action="store_true", help="Download controversial posts")
    type_group.add_argument("--rising", action="store_true", help="Download rising posts")
    type_group.add_argument("--top", action="store_true", help="Download top posts")

    args = parser.parse_args()
    if args.hot:
        post_type = 'hot'
    elif args.controversial:
        post_type = 'controversial'
    elif args.rising:
        post_type = 'rising'
    elif args.top:
        post_type = 'top'
    else:
        post_type = 'hot'

    response = get_reddit_page(args.subreddit, post_type, args.limit, args.time)
    url_list = find_imgur_url(response)
    file_download.download_list(args.subreddit, url_list)

main()