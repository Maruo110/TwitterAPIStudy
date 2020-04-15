# -*- coding: utf-8 -*-

import json, config, worldid
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

url = "https://api.twitter.com/1.1/trends/place.json"

params = {
    'id' : worldid.Japan
}

req = twitter.get(url, params = params)

if req.status_code == 200:
    search_trend = json.loads(req.text)

    for trendinfo in search_trend[0]['trends']:
        print('＞' + trendinfo['name'] + '  [' + str(trendinfo['tweet_volume']) + ']')
else:
    print("ERROR: %d" % req.status_code)
