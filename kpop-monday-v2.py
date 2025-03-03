# foo
from mastodon import Mastodon
import time
from dotenv import load_dotenv
import os
# import random
# import json
import pickle

# define some variables:
htag = 'FaceCards'
# load the Mastodon key info from .env
load_dotenv()
# Open a file to save the data:
f = open('../Data/'+htag+'.pickle', 'wb')

mastodon = Mastodon(
        client_id=os.getenv("Client_key"),
        client_secret=os.getenv("Client_secret"),
        access_token=os.getenv("access_token"),
        api_base_url="https://mstdn.social"
)

hashtag_posts={}
hashtag_posts=mastodon.timeline_hashtag(hashtag = htag)
hashtag_dict = [(index, item) for index, item in enumerate(hashtag_posts)]
hashtag_dict = dict(hashtag_dict)
pickle.dump(hashtag_dict, f)
f.close()
