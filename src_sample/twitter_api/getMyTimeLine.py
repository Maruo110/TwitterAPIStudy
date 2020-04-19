# -*- coding: utf-8 -*-

import json
import app_pconfig #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = config.CONSUMER_KEY
CS app_pconfigig.CONSUMER_SECRET
app_pconfigonfig.ACCESS_TOKEN
ATSapp_pconfigfig.ACCESS_TOKEN_SECRapp_pconfigitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

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
