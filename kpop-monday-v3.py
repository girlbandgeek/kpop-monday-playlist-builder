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

# Define some variables
start_buffer = timedelta(hours=2)  # Bonus time *before* 00:00
tz_adjust = timedelta(hours=-7)  # Set to -7 for computer in Pacific time
day_len = timedelta(days=1, hours=12)  # Total length of kpopmonday, e.g. 36 hrs
# List of accounts not to include, e.g. not our own user and possibly others to block ;)
excluded_users=['kpopmondayplaylistbot@mstdn.social']

load_dotenv()

mastodon = Mastodon(
        client_id=os.getenv("Client_key"),
        client_secret=os.getenv("Client_secret"),
        access_token=os.getenv("access_token"),
        api_base_url="https://mstdn.social"
)

def retrieve_statuses(hhtag, mmy_min, mmy_max, since_stat, max_key):
    print("hhtag", "mmy_min", "mmy_max", "since_stat", "max_key")
    print(hhtag, mmy_min, mmy_max, since_stat, max_key)
    hashtag_posts={}
    # There will be 2 different "mastodon.timeline_hashtag" calls, depending on whether since_id has been set...
    # This is part of recursive logic, to handle API limit of ~20 statuses retrieved per call
    if since_stat == "":
        hashtag_posts=mastodon.timeline_hashtag(hashtag = hhtag, min_id = mmy_min, max_id = mmy_max)
    else:
        hashtag_posts=mastodon.timeline_hashtag(hashtag = hhtag, min_id = since_stat, max_id = mmy_max)

    # convert list to dict
    hashtag_dict = [(index, item) for index, item in enumerate(hashtag_posts)]
    hashtag_dict = dict(hashtag_dict)

    # define a dict to contain the output
    results_dict={}
    
    for key, value in hashtag_dict.items():
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
            # remove duplicate videos
            new_vid_list = list(set(vid_list))
            print("video ID's: ", new_vid_list)
            rlist.append(new_vid_list)
        else:
            print(f"videos: NOT MATCHED!!!")
            rlist.append([])

        # Generate a list of tags      
        tag_dict = hashtag_dict[key]["tags"]
        tag_list=[]
        for x in tag_dict:
            tag_list.append(x["name"])
            # print(f"name of the tag: ", x["name"])
        print(f"tag_list: ", tag_list)
        
        # we will use the status id as the dict key
        # Make sure we are getting only #kpopmonday statuses and also,
        # Exclude statuses from list of excluded user
        if "kpopmonday" in tag_list and hashtag_dict[key]["account"]["acct"].lower() not in excluded_users:
            kd_key = hashtag_dict[key]["id"]
            results_dict[kd_key] = rlist
        else:
            continue    # skip if desired conditions not met         
        
    # Remove potential duplicate record 
    if max_key in results_dict.keys():
        del results_dict[max_key]

    return results_dict
    

# htag = 'FaceCards'
# start_date = date(2025, 2, 17)
htag = sys.argv[1]
start_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
# delta = timedelta(days=1, hours=12)
# uncomment following 2 lines for Pacific time
# adjust = timedelta(hours=8)
t_time = time(0, 0)  # minutes, seconds
start_date = datetime.datetime.combine(start_date, t_time)
# Implement date, time adustments
my_min = start_date - start_buffer + tz_adjust
my_max = my_min + day_len
# For first go, set since_status to null:
since_status=""
output_dict={}
max_key='0'

while(True):
    records_to_add=retrieve_statuses(htag, my_min, my_max, since_status, max_key)

    if len(records_to_add) == 0:
        print("Records to add = 0")
        break

    # find latest record
    max_key = max(records_to_add, key=records_to_add.get)
    #since_status=parser.parse(records_to_add[max_key][0])
    since_status=(records_to_add[max_key][0])
    print(f"max_key: ", max_key, "since_status: ", since_status, "max_key: ", max_key)
    output_dict.update(records_to_add)

print("output_dict:")
print(output_dict)

# Let's explore the relations betweeen the statuses and the timestamps
ccount=0
for key in sorted(output_dict.keys()):
    ccount=ccount+1
    print("RECORD: ",ccount, key, output_dict[key][0], output_dict[key][1], output_dict[key][2])

# Build the list of playlist videos, and Generate some 
# stats for this collection of statuses
playlist_vids = []
stats_dict = {}
der_count=0
for key in sorted(output_dict.keys()):
    if output_dict[key][3] != []:
        for i_item in output_dict[key][3]:
            playlist_vids.append(i_item)
    # playlist_vids.append(output_dict[key][3])
    if output_dict[key][2] in stats_dict.keys():
        stats_dict[output_dict[key][2]] = stats_dict[output_dict[key][2]] + 1
    else:
        stats_dict[output_dict[key][2]] = 1
        
leader_count = max(stats_dict.values())
leader_board = ""
for key, value in stats_dict.items():
    if value == leader_count:
        if leader_board == "":
            leader_board = key
        else:
            leader_board = leader_board + ', ' + key
    else:
        continue


print(f"Total number of posts for ", htag, "is: ", ccount)
print(f"Top contributor(s) this week with", leader_count, "posts are: ", leader_board)
print(f"Playlist videos :", playlist_vids)

'''
print("stats_dict:")
print(stats_dict)
'''
