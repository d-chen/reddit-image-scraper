#Reddit Image Scraper

Tool for downloading Imgur images from Reddit

###Usage

```
usage: main.py [-h] [-l LIMIT] [-t {hour,day,week,month,year,all}]
               [--hot | --controversial | --rising | --top]
               subreddit

Download Imgur images from specified subreddit

positional arguments:
  subreddit             Subreddit to download from

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        Maximum number of posts [default:25 max:100]
  -t {hour,day,week,month,year,all}, --time {hour,day,week,month,year,all}
                        Time period to check [default: day]
  --hot                 Download hot posts [default]
  --controversial       Download controversial posts
  --rising              Download rising posts
  --top                 Download top posts
```

###Requirements
Install BeautifulSoup, Requests with pip:

`pip install -r requirements.txt`
