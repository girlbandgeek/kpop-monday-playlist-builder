# foo
from mastodon import Mastodon
import time
from dotenv import load_dotenv
import os
import random

load_dotenv()

mastodon = Mastodon(
        client_id=os.getenv("Client_key"),
        client_secret=os.getenv("Client_secret"),
        access_token=os.getenv("access_token"),
        api_base_url="https://mstdn.social"
)

'''
# get my account id
my_account = mastodon.account_verify_credentials()
print(my_account.id)
'''

'''
following=mastodon.account_following(113966619355975527)

following_posts = []
for i in following:
    for posts in mastodon.account_statuses(i):
        following_posts.append(posts.id)

print(following_posts)
'''

hashtag_posts={}
hashtag_posts=mastodon.timeline_hashtag(hashtag = "FaceCards")
# Print the first status
#print(hashtag_posts[1])

# Print each status on separate line:
#for key in hashtag_posts:
#    print(key)

hashtag_dict = [(index, item) for index, item in enumerate(hashtag_posts)]
hashtag_dict = dict(hashtag_dict)
for key, value in hashtag_dict.items():
    print(f"{key}: {value}")
