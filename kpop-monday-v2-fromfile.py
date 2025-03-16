# Process statuses previously downloaded to file
# Usage: python3 kpop-monday-v2-fromfile.py HashTag
from mastodon import Mastodon
import time
from dotenv import load_dotenv
import os
import sys
import re
import random
import pickle
# define some variables:
# htag = 'FaceCards'
htag = sys.argv[1]

load_dotenv()

# Open data file:
f = open('../Data/'+htag+'.pickle', 'rb')

hashtag_dict = pickle.loads(f.read())
#  to contain the status records
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

    #print(f"content: ", hashtag_dict[key]["content"])
    # Note: pattern matching is not working yet!!!
    ccontent = hashtag_dict[key]["content"]
    # print(f"ccontent: ", ccontent)
    # match = re.findall(r'www\.youtube\.com/watch\?v=(\w+)', ccontent)
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

  
    tag_dict = hashtag_dict[key]["tags"]
    # print(f"tag_dict type: ", type(tag_dict))
    # print(f"tag_dict: ", tag_dict)
    tag_list=[]
    for x in tag_dict:
        tag_list.append(x["name"])
        # print(f"name of the tag: ", x["name"])
    print(f"tag_list: ", tag_list)
    rlist.append(tag_list)
    # print(f"content type: ", type(hashtag_dict[key]["content"]))
    # print(f"tags type: ", type(hashtag_dict[key]["tags"]))

    # we will use the status id as the dict key
    kd_key = hashtag_dict[key]["id"]
    output_dict[kd_key] = rlist

    '''
    for kkey in hashtag_dict[key].keys():
        # Print each key and the value in the status
        print(f"{kkey}: ", hashtag_dict[key][kkey])
    '''

print("output_dict:")
print(output_dict)

# Let's explore the relations betweeen the statuses and the timestamps
for key in output_dict:
    print(key, output_dict[key][0], output_dict[key][1])
