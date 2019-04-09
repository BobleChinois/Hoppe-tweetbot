from mastodon import Mastodon
import os

def toot(tweet, filename):

    cred_dir = os.path.join(os.path.dirname(__file__), 'masto_id')
    mastodon = Mastodon(
            access_token = cred_dir,
            api_base_url = 'https://liberdon.com'
            )

    media_id = mastodon.media_post(filename)

    mastodon.status_post(tweet, media_ids=media_id)

    return('Tooted: ', tweet)
