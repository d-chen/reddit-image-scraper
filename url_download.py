import urllib2
import os

DOWNLOAD_DIR = os.getcwd() + "/downloaded/"

def download_list(subreddit, url_list):
    file_dir = DOWNLOAD_DIR + subreddit.lower() + "/"

    try:
        os.makedirs(file_dir)
    except OSError:
        if not os.path.isdir(file_dir):
            print "Error: Unable to create file directory."
            print "Download halted."
            raise


    for url in url_list:
        file_name = file_dir + url.split('/')[-1]

        # check if file was downloaded
        if not os.path.isfile(file_name):
            print "Downloading from " + url
            image_file = urllib2.urlopen(url)
            with open(file_name, "ab+") as destination:
                destination.write(image_file.read())
        else:
            print file_name +"' already exists."

    print "Download from r/" + subreddit + " complete."

