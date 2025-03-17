# Pull selected statuses with Mastodon API and process them
from mastodon import Mastodon
import datetime
from datetime import date
from datetime import timedelta
from datetime import time
from dateutil import parser
from dotenv import load_dotenv
import os
import sys
import re

#from datetime import datetime, date, time, timezone


load_dotenv()

mastodon = Mastodon(
        client_id=os.getenv("Client_key"),
        client_secret=os.getenv("Client_secret"),
        access_token=os.getenv("access_token"),
        api_base_url="https://mstdn.social"
)

def retrieve_statuses(hhtag, mmy_min, mmy_max, since_stat):
    hashtag_posts={}
    # hashtag_posts=mastodon.timeline_hashtag(hashtag = hhtag, min_id = my_min, max_id = my_max)
    # hashtag_posts=mastodon.timeline_hashtag(hashtag = hhtag, min_id = my_min, max_id = my_max, since_id = since_stat)
    # Need to add if statement here. There will be 2 different "mastodon.timeline_hashtag" calls, depending on whether
    # since_id has been set...
    if since_stat == "":
        hashtag_posts=mastodon.timeline_hashtag(hashtag = hhtag, min_id = my_min, max_id = my_max)
    else:
        hashtag_posts=mastodon.timeline_hashtag(hashtag = hhtag, max_id = my_max, since_id = since_stat)


    hashtag_dict = [(index, item) for index, item in enumerate(hashtag_posts)]
    hashtag_dict = dict(hashtag_dict)
    # define a dict to contain the output
    output_dict={}

    for key, value in hashtag_dict.items():
        # output_list.append(hashtag_dict[key]["id"])
        rlist=[]

        print(f"record number: ", key)
        print(f"status id: ", hashtag_dict[key]["id"])
        print(f"created_at: ", hashtag_dict[key]["created_at"])
        print(f"account id: ", hashtag_dict[key]["account"]["id"])
        print(f"account name: ", hashtag_dict[key]["account"]["acct"])
        
        # rlist.append(hashtag_dict[key]["id"])
        rlist.append(hashtag_dict[key]["created_at"])
        rlist.append(hashtag_dict[key]["account"]["id"])
        rlist.append(hashtag_dict[key]["account"]["acct"])

        ccontent = hashtag_dict[key]["content"]

        match = re.findall(r'(www\.youtube\.com/watch\?v=|youtu\.be/)([\w-]+)', ccontent)
        if len(match) > 0: 
            print(f"videos: ", match)
            vid_list=[]
            for iitem in match:
                vid_list.append(iitem[1])
            print("video ID's: ", vid_list)
            rlist.append(vid_list)
        else:
            print(f"videos: NOT MATCHED!!!")
            rlist.append({})

        # Generate a list of tags      
        tag_dict = hashtag_dict[key]["tags"]
        tag_list=[]
        for x in tag_dict:
            tag_list.append(x["name"])
            # print(f"name of the tag: ", x["name"])
        print(f"tag_list: ", tag_list)
        rlist.append(tag_list)

        # we will use the status id as the dict key
        kd_key = hashtag_dict[key]["id"]
        output_dict[kd_key] = rlist
    return output_dict
    

# define some variables:

# htag = 'FaceCards'
# start_date = date(2025, 2, 17)
htag = sys.argv[1]
# start_date = sys.argv[2]
start_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')

day = timedelta(days=1)
end_date = start_date + day
t_time = time(0, 0)
my_min = datetime.datetime.combine(start_date, t_time)
my_max = datetime.datetime.combine(end_date, t_time)
# For first go, set since_status to 0:
#since_status="113664559726097118"
since_status=parser.parse("2025-03-10 10:48:52+00:00")
# since_status=""

output_dict=retrieve_statuses(htag, my_min, my_max, since_status)

print("output_dict:")
print(output_dict)

# Let's explore the relations betweeen the statuses and the timestamps
for key in output_dict:
    print(key, output_dict[key][0], output_dict[key][1])
