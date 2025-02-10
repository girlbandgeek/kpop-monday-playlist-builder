import requests
import configparser

config = configparser.RawConfigParser()
config.read('config')

mstdn_dict = dict(config.items('mastodon-auth'))

mstdn_token = mstdn_dict['mstdn_token']
print(mstdn_token)

url = 'https://mstdn.social/api/v1/statuses'
auth = {'Authorization': "Bearer "+mstdn_token.strip('"')}
print(auth)
params = {'status': 'I\'m posting from python. I\'m using config file.'}

response = requests.post(url, data=params, headers=auth)

print(response)

