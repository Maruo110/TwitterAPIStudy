# -*- coding: utf-8 -*-

import app_pconfig
from requests_oauthlib import OAuth1Session
import datetime, time

CK = app_pconfig.CONSUMER_KEY
CS = app_pconfig.CONSUMER_SECRET
AT = app_pconfig.ACCESS_TOKEN
ATS = app_pconfig.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

url = "https://api.twitter.com/1.1/statuses/user_timeline.json" #タイムライン取得エンドポイント

res = twitter.get(url)

limit = res.headers['x-rate-limit-remaining'] #リクエスト可能残数の取得
reset = res.headers['x-rate-limit-reset'] #リクエスト可能残数リセットまでの時間(UTC)
sec = int(res.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.datetime.now().timetuple()) #UTCを秒数に変換

print ("limit: " + limit)
print ("reset: " +  reset)
print ('reset sec:  %s' % sec)