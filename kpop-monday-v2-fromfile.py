# Process statuses previously downloaded to file
# Usage: python3 kpop-monday-v2-fromfile.py HashTag
from mastodon import Mastodon
import time
from dotenv import load_dotenv
import os
import sys
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
    print(f"{key}:")
    # print(f"account id: ", hashtag_dict[key]["id"])
    print(f"account id: ", hashtag_dict[key]["account"]["id"])
    print(f"account username: ", hashtag_dict[key]["account"]["username"])
    print(f"account name: ", hashtag_dict[key]["account"]["acct"])
    print(f"content: ", hashtag_dict[key]["content"])
    for kkey in hashtag_dict[key].keys():
        # Print each key and the value in the status
        print(f"{kkey}: ", hashtag_dict[key][kkey])
