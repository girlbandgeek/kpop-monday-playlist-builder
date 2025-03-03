# foo
from mastodon import Mastodon
import time
from dotenv import load_dotenv
import os
import random

load_dotenv()

# Import data file
f_input = open("/home/azureuser/Work/Data/facecards.out", "r")

mastodon = Mastodon(
        client_id=os.getenv("Client_key"),
        client_secret=os.getenv("Client_secret"),
        access_token=os.getenv("access_token"),
        api_base_url="https://mstdn.social"
)


'''

print(hashtag_posts)
'''
hashtag_posts={}
hashtag_posts=mastodon.timeline_hashtag(hashtag = "FaceCards")

foo=json_out=staticfrom_json(json_str: str)→ Entity
print(foo)
'''
staticfrom_json(json_str: str)→ Entity
hashtag_posts={}
hashtag_posts=print(f_input.read())

hashtag_dict = [(index, item) for index, item in enumerate(hashtag_posts)]
hashtag_dict = dict(hashtag_dict)
# print(hashtag_dict)
for key, value in hashtag_dict.items():
    print(f"{key}:")
    for kkey in hashtag_dict[key].keys():
        # Print each key and the value in the status
        print(f"{kkey}: ", hashtag_dict[key][kkey])
hashtag_dict = dict(hashtag_dict)
for key, value in hashtag_dict.items():
    print(f"{key}:")

# Print each status on separate line:
for key in hashtag_posts:
    print(key)

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
for key in hashtag_dict[0].keys():
    print(f"{key}: ", hashtag_dict[0][key])
'''
