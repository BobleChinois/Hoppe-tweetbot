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
pics_dir = os.path.join(os.path.dirname(__file__), 'pics')

def parseSource(text):
    # Identify 'Source:' using regex
    m = re.search(r'(Source: )(.*)', text)
    link = m.group(2)
    # return a link
    if link != None:
        return link
    else:
        raise RuntimeError('No source')

def matchPic(link):
    # Match the following link with an image file
    if link == "https://mises.org/library/theory-socialism-and-capitalism-0":
        return 'ATSC.jpg'
    elif link == "":
        return 'DGTF.jpg'
    elif link == "":
        return 'FATMTD.jpg'
    elif link == "":
        return 'GLR.jpg'
    elif link == "":
        return 'SHM.jpg'
    elif link == "":
        return 'TEEPP.jpg'
    else:
        return None


try:
    with open('quotes', 'r+') as tweetfile:
        buff = tweetfile.readlines()

    for line in buff[:]:
        line = line.strip(r'\n')
        link = parseSource(line)
        link_length = len(link)
        line_length = len(line) - link_length + 23
        if line_length <= 280 and len(line)>0:
            print("Tweeting...")
            source = matchPic(link)
            
            if source != None:
                filename = os.path.join(pics_dir, source) 
            else:
                filename = os.path.join(pics_dir, \
                    choice(os.listdir(pics_dir))) 

            pic = open(filename, 'rb')
            response = twitter.upload_media(media=pic)

            twitter.update_status(status=line, \
                    media_ids=[response['media_id']])
            
            with open('quotes', 'w') as tweetfile:
                buff.remove(line)
                tweetfile.writelines(buff)
            print("Tweeted!")
            time.sleep(3600)
        else:
            print("Skipped line - too long a quote")
            print(line, 'is ', line_length, 'long')
            continue
    print("No more lines to tweet...")

except TwythonError as e:
    print(e)
