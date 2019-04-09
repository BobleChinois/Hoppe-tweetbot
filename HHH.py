from twython import Twython, TwythonError
import time
import os
from random import choice 
import re
from HHH_masto import toot
from importCredentials import importCredentials

def parseText(text):
    # Separate the quote from the link
    tweet = {}
    regex = r'(?P<quote>.*)?(?P<link>https.*)?'

    m = re.search(regex, text)

    tweet = m.groupdict("")

    return tweet

def matchPic(link):
    # Match the following link with an image file
    if link == "https://mises.org/library/theory-socialism-and-capitalism-0":
        return 'ATSC.jpg'
    elif link == "https://mises.org/library/democracy-god-failed-1":
        return 'DGTF.jpg'
    elif link == "https://mises-media.s3.amazonaws.com/From%20Aristocracy%20to%20Monarchy%20to%20Democracy_Hoppe_Text%202014.pdf":
        return 'FATMTD.jpg'
    elif link == "https://mises.org/library/getting-libertarianism-right":
        return 'GLR.jpg'
    elif link == "https://mises.org/library/short-history-man-progress-and-decline":
        return 'SHM.jpg'
    elif link == "https://mises.org/library/economics-and-ethics-private-property-0":
        return 'TEEPP.jpg'
    else:
        return None

cred_dir = os.path.join(os.path.dirname(__file__), 'twitter_id')
books_dir = os.path.join(os.path.dirname(__file__), 'books')
memes_dir = os.path.join(os.path.dirname(__file__), 'memes')

creds = importCredentials(cred_dir) 
twitter = Twython(*creds)

try:
    with open('quotes', 'r+') as tweetfile:
        buff = tweetfile.readlines()

    for line in buff[:]:
       
        line = line.strip(r'\n')
        text = parseText(line) 
        quote = '"' + text['quote'] + '"'
        link = text['link']
        tweet = quote + link

        link_length = len(link)
        tweet_length = len(tweet) - link_length + 23

        if tweet_length <= 280:
            print("Tweeting...")

            source = matchPic(link)
            
            if source != None:
                filename = os.path.join(books_dir, source) 
            else:
                filename = os.path.join(memes_dir, \
                    choice(os.listdir(memes_dir))) 

            pic = open(filename, 'rb')
            response = twitter.upload_media(media=pic)

            print(f"{tweet}")

            #twitter.update_status(status=tweet, \
            #        media_ids=[response['media_id']])
            
            print("Tweeted!")
            
            toot(tweet, filename) 

            print("Tooted!")

            #with open('quotes', 'w') as tweetfile:
            #    buff.remove(line)
            #    tweetfile.writelines(buff)
            time.sleep(21600)
        else:
            print("Skipped line - too long or non-existent")
            with open('quotes', 'w') as tweetfile:
                buff.remove(line)
                tweetfile.writelines(buff)
            continue

    print("No more lines to tweet...")

except TwythonError as e:
    print(e)
