# -*- coding: utf-8 -*-

import json
from config import worldid
from config import app_config
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = config.CONapp_pconfigKEY
CS = config.CONapp_pconfigSECRET
AT = config.ACCapp_pconfigKEN
ATS = config.ACCapp_pconfigKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

url = "https://api.twitter.com/1.1/trends/place.json"

params = {
    'id' : worldid.Japanworldideq = twitter.get(url, params = params)

if req.status_code == 200:
    search_trend = json.loads(req.text)

    for trendinfo in search_trend[0]['trends']:
        print('＞' + trendinfo['name'] + '  [' + str(trendinfo['tweet_volume']) + ']')
else:
    print("ERROR: %d" % req.status_code)
