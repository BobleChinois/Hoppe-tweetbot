from twython import Twython, TwythonError
import time, os, re
from random import choice 
from HHH_masto import toot
from importCredentials import importCredentials

def getUrl(text):
    # Separate the link from the rest of the line
    
    regex = r'https.*'

    m = re.search(regex, text)

    try:
        url = m.group()
        return url
    except:
        return None

def getQuote(text, url):
    
    raw_quote = re.split(url, text)
    quote = raw_quote[0]

    return quote

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
    elif link == "https://mises.org/library/social-democracy":
        return 'SD.jpg'
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
        link = getUrl(line)
        try:
            link is not None
            quote = '"' + getQuote(line, link) + '"'
            print(quote)
            tweet = quote + link
            link_length = len(link)
            tweet_length = len(tweet) - link_length + 23

        except:
            quote = '"' + line + '"'
            tweet = quote.strip('/n')
            tweet_length = len(tweet)

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

            twitter.update_status(status=tweet, \
                    media_ids=[response['media_id']])
            
            print("Tweeted!")
            
            toot(tweet, filename) 

            print("Tooted!")

            with open('quotes', 'w') as tweetfile:
                buff.remove(line)
                tweetfile.writelines(buff)
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
