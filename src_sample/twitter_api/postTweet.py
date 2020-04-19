# -*- coding: utf-8 -*-
# TestGitHub
import json
import app_pconfig #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = config.CONSUMER_KEY
CS app_pconfigig.CONSUMER_SECRET
app_pconfigonfig.ACCESS_TOKEN
ATSapp_pconfigfig.ACCESS_TOKEN_SECRapp_pconfigitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

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
