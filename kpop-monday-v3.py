# Pull selected statuses with Mastodon API and process them
from mastodon import Mastodon
import datetime
from datetime import date
from datetime import timedelta
from datetime import time
from dotenv import load_dotenv
import os
import random
#from datetime import datetime, date, time, timezone
# define some variables:
htag = 'FaceCards'
start_date = date(2025, 2, 17)
day = timedelta(days=1)
end_date = start_date + day
t_time = time(0, 0)
my_min = datetime.datetime.combine(start_date, t_time)
my_max = datetime.datetime.combine(end_date, t_time)
# print('my_min: ', my_min)
# print('my_max: ', my_max)

load_dotenv()

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
for key, value in hashtag_dict.items():
    print(f"{key}:")
    # print(f"account id: ", hashtag_dict[key]["id"])
    print(f"account id: ", hashtag_dict[key]["account"]["id"])
    print(f"account username: ", hashtag_dict[key]["account"]["username"])
    print(f"account name: ", hashtag_dict[key]["account"]["acct"])
    print(f"content: ", hashtag_dict[key]["content"])
    for kkey in hashtag_dict[key].keys():
        # Print each key and the value in the status
        print(f"{kkey}: ", hashtag_dict[key][kkey])
'''
for key in hashtag_dict[0].keys():
    print(f"{key}: ", hashtag_dict[0][key])
'''
