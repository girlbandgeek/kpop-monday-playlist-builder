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

for key, value in hashtag_dict.items():
    print(f"record number: ", key)
    print(f"account id: ", hashtag_dict[key]["account"]["id"])
    print(f"account name: ", hashtag_dict[key]["account"]["acct"])
    print(f"status id: ", hashtag_dict[key]["id"])
    #print(f"content: ", hashtag_dict[key]["content"])
    # Note: pattern matching is not working yet!!!
    ccontent = hashtag_dict[key]["content"]
    match = re.match('https://www.youtube.com/watch?v=(\w){11}', ccontent)
    print(f"videos: ", match.groups())
    tag_dict = hashtag_dict[key]["tags"]
    print(f"tag_dict type: ", type(tag_dict))
    print(f"tag_dict: ", tag_dict)
    tag_list=[]
    for x in tag_dict:
        tag_list.append(x["name"])
        # print(f"name of the tag: ", x["name"])
    print(f"tag_list: ", tag_list)
    print(f"content type: ", type(hashtag_dict[key]["content"]))
    print(f"tags type: ", type(hashtag_dict[key]["tags"]))
    for kkey in hashtag_dict[key].keys():
        # Print each key and the value in the status
        print(f"{kkey}: ", hashtag_dict[key][kkey])
