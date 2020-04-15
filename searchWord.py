# -*- coding: utf-8 -*-

import json, config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

# APIエンドポイント（スタンダード版＜短縮ツイート版＞）
#url = "https://api.twitter.com/1.1/search/tweets.json"

# APIエンドポイント（拡張版＜フルツイート版＞）
url = "https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended"

print("何を調べますか?")
keyword = input('>> ')
print('----------------------------------------------------')


params = {
    'q' : keyword,
    'lang' : 'ja',
    'result_type' : 'popular',
    'count' : 20
}

req = twitter.get(url, params = params)

if req.status_code == 200:
    search_timeline = json.loads(req.text)
    for tweet in search_timeline['statuses']:
        print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
        print('@' + tweet['user']['screen_name'])
        print('＞' + tweet['user']['name'])
        print('＞' + tweet['created_at'])
        print('＞RT=' + str(tweet['retweet_count']) + '　＞FV=' + str(tweet['favorite_count']))
        print('＞' + tweet['full_text'])
        # ツイートURL
        print('＞https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str'])

        # ハッシュタグ
        hashtaglist = tweet['entities']['hashtags']
        for hashtag in hashtaglist:
            print('＞#' + hashtag['text'])

        # リンクURL
        link_url_list = tweet['entities']['urls']
        for link_url in link_url_list:
            print('＞' + link_url['expanded_url'])

        print('▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')
#        print(tweet['user']['name'] + '::' + tweet['text'])
#        print(tweet['created_at'])
#        print('----------------------------------------------------')

else:
    print("ERROR: %d" % req.status_code)
