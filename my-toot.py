# Write some code to post a status on our timeline
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

stp1 = 'Hi! Here is the KpopMonday compilation playlist for December 2, 2024.'
stp2 = 'This week\'s theme is #TwoSongsOneTitle'
stp3 = 'Total number of toots for  TwoSongsOneTitle is:  77'
stp4 = 'Top contributor(s) this week with 31 toots:  Erzbet@apobangpo.space'
stp5 = 'https://youtube.com/playlist?list=PLZyP4b181sFYgqLdKYRNzFhWVx1_iYWwp&si=zMl2upkP9OV34UJu'
stp6 = '#fake_tag'
'''
x = ' '.join(("multiline String ",
			"Python Language",
			"Welcome to GFG"))
print(x)
'''
status_text = '\n\n'.join((stp1, stp2, stp3, stp4, stp5, stp6))
print(status_text)

mastodon.status_post(status = status_text, visibility = "public")
