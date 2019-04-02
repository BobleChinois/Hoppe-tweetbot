from twython import Twython, TwythonError
import time
import os
from random import choice 
import re

APP_KEY = "AZGNmseKabNe9zy1Ud3bg0qtA"
APP_SECRET = "6sZOdFQVZbHZtbRd1XMUVEDEKhzgXHw3vI5BibTyJOqRSPjW1P"
OAUTH_TOKEN = "1110509646228480000-4YWPWBKLdwxIDqFPut86bUAWE1J7Xi"
OAUTH_TOKEN_SECRET = "87jwWi9ITxfbr7t2T4qCG6r6uaVFtR7CayU33UO3gPwD8"

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
books_dir = os.path.join(os.path.dirname(__file__), 'books')
memes_dir = os.path.join(os.path.dirname(__file__), 'memes')

def parseText(text):
    # Separate the quote from the link
    m = re.search(r'(?P<quote>.*)(?P<link>(https.*)?)', text)
    tweet = m.groupdict("")
    # return a dict object with the quote and the link if any
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
        if tweet_length <= 280 and len(line) > 0:
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

            twitter.update_status(status=tweet, \
                    media_ids=[response['media_id']])
            
            with open('quotes', 'w') as tweetfile:
                buff.remove(line)
                tweetfile.writelines(buff)
            print("Tweeted!")
            time.sleep(3600)
        else:
            print("Skipped line - too long or nothing")
            print(line, 'is ', line_length, 'long')
            continue
    print("No more lines to tweet...")

except TwythonError as e:
    print(e)
