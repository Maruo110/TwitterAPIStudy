# -*- coding: utf-8 -*-
# TestGitHub
import json
from config import app_config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = app_config.CONSUMER_KEY
CS = app_config.CONSUMER_SECRET
AT = app_config.ACCESS_TOKEN
ATS = app_config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

url = "https://api.twitter.com/1.1/statuses/update.json" #ツイートポストエンドポイント

print("内容を入力してください。")
tweet = input('>> ') #キーボード入力の取得
print('*******************************************')

params = {"status" : tweet}

res = twitter.post(url, params = params) #post送信

if res.status_code == 200: #正常投稿出来た場合
    print("Success.")
else: #正常投稿出来なかった場合
    print("Failed. : %d"% res.status_code)