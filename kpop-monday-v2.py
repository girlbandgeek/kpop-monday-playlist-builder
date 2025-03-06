# Dump selected statuses to file using pickle format
# Usage: python3 kpop-monday-v2.py HashTag YYYY-MM-DD
from mastodon import Mastodon
import datetime
from datetime import time
from datetime import date
from datetime import timedelta
from dotenv import load_dotenv
import os
import pickle
import sys

# define some variables:
htag = sys.argv[1]
mon_date = sys.argv[2]
start_date = date.fromisoformat(mon_date)
day = timedelta(days=1)
end_date = start_date + day
t_time = time(0, 0)
my_min = datetime.datetime.combine(start_date, t_time)
my_max = datetime.datetime.combine(end_date, t_time)

# load the Mastodon key info from .env
load_dotenv()

# Open a file to save the data:
data_path=os.getenv("data_path")
f = open(data_path+htag+'.pickle', 'wb')

mastodon = Mastodon(
        client_id=os.getenv("Client_key"),
        client_secret=os.getenv("Client_secret"),
        access_token=os.getenv("access_token"),
        api_base_url="https://mstdn.social"
)

hashtag_posts={}
hashtag_posts=mastodon.timeline_hashtag(hashtag = htag, min_id = my_min, max_id = my_max)
hashtag_dict = [(index, item) for index, item in enumerate(hashtag_posts)]
hashtag_dict = dict(hashtag_dict)
pickle.dump(hashtag_dict, f)
f.close()
