# -*- coding: utf-8 -*-

import json, worldid
import app_pconfig
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = config.CONapp_pconfigKEY
CS = config.CONapp_pconfigSECRET
AT = config.ACCapp_pconfigKEN
ATS = config.ACCapp_pconfigKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

# APIエンドポイント（トレンド取得）
url = "https://api.twitter.com/1.1/trends/place.json"

# APIエンドポイント（ツイート取得＜拡張版＞）
url2 = "https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended"

params = {
    'id' : worldid.Japan
}

req = twitter.get(url, params = params)

if req.status_code == 200:
    search_trend = json.loads(req.text)

    for trendinfo in search_trend[0]['trends']:
        print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
        print('＞' + trendinfo['name'] + '  [' + str(trendinfo['tweet_volume']) + ']')

        params2 = {
            'q' : trendinfo['name'],
            'lang' : 'ja',
            'result_type' : 'popular',
            'count' : 3
        }

        req2 = twitter.get(url2, params = params2)

        if req2.status_code == 200:
            search_timeline = json.loads(req2.text)
            for tweet in search_timeline['statuses']:
                print('-----------------------------------------------------')
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

                print('-----------------------------------------------------')

        else:
            print("ERROR: %d" % req2.status_code)

        print('▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')

else:
    print("ERROR: %d" % req.status_code)
