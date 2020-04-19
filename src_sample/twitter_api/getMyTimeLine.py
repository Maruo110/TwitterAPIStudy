# -*- coding: utf-8 -*-

import json
from config import app_config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = app_config.CONSUMER_KEY
CS = app_config.CONSUMER_SECRET
AT = app_config.ACCESS_TOKEN
ATS = app_config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

params ={'count' : 5}
req = twitter.get(url, params = params)

if req.status_code == 200:
    timeline = json.loads(req.text)
    for tweet in timeline:
        print(tweet['user']['name']+'::'+tweet['text'])
        print(tweet['created_at'])
        print('----------------------------------------------------')
else:
    print("ERROR: %d" % req.status_code)
