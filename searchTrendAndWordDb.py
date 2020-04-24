# -*- coding: utf-8 -*-
import time
import threading
from google_cloud_api.analyze_entities import getAnalizeEntityResult

def run_searchTrendInfo():

    import json, sqlite3, datetime, logging.config, requests
    from config import worldid
    from config import app_config
    from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
    from datetime import datetime
    from dao import tweetdbDao
    from google_cloud_api import natural_language, analyze_entities
    from google.cloud.language_v1 import enums
    from util import utils
    from logging import getLogger
    from bs4 import BeautifulSoup

    logging.config.fileConfig('logging.conf')
    logger = getLogger()
    logger.info('▼▼▼▼▼▼START▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
    date_today = datetime.now().strftime("%Y-%m-%d")
    date_time = datetime.now().strftime("%H:%M:%S")

    logger.info('｜処理日: %s', date_today)
    logger.info('｜処理時間: %s', date_time)


    CK = app_config.CONSUMER_KEY
    CS = app_config.CONSUMER_SECRET
    AT = app_config.ACCESS_TOKEN
    ATS = app_config.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

    # APIエンドポイント（トレンド取得）
    url = "https://api.twitter.com/1.1/trends/place.json"
    # APIエンドポイント（ツイート取得＜拡張版＞）
    url2 = "https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended"

    params = {'id' : worldid.Japan, 'exclude': 'hashtags'}

    req = twitter.get(url, params = params)

    count_trend     = 0
    count_tweet     = 0
    count_hashtag   = 0
    count_linkedurl = 0

    db_connection = sqlite3.connect(app_config.DB_NAME)
    db_cursol = db_connection.cursor()

    if req.status_code == 200:
        logger.debug('｜◇Twitter OAuth認証通過')

        search_trend = json.loads(req.text)

        for trendinfo in search_trend[0]['trends']:
            trend_word = trendinfo['name']

            hashtag_flg = 0
            trend_word_id = -1
            trend_sentiment_score = 0.0
            trend_linked_tweet_cnt = 0

            if trend_word[0] == '#':
                hashtag_flg = 1
                trend_word_id = tweetdbDao.getHashTagId(db_cursol, trend_word)

                if trend_word_id < 0:
                    tweetdbDao.insertHashTagTbl(db_connection, db_cursol, trend_word)
                    trend_word_id = tweetdbDao.getHashTagId(db_cursol, trend_word)
            else:
                pass

            logger.debug('｜▽trend_word: %s', trend_word)

            trend_volume = trendinfo['tweet_volume']

            if trend_volume is None:
                tweet_volume = "-1"
            else:
                tweet_volume = str(trend_volume)

            insert_values = "'" + trend_word + "','" + str(date_today) + "','" + str(date_time) + "'"
            insert_values = insert_values + "," + tweet_volume
            insert_values = insert_values + "," + str(hashtag_flg)
            insert_values = insert_values + "," + str(trend_word_id)

            #print("insert_values＝" + insert_values)
            tweetdbDao.insertTrendTbl(db_connection, db_cursol, insert_values)
            trendid = tweetdbDao.getMaxIdTrendTbl(db_cursol)
            count_trend += 1

            params2 = {
                'q' : trend_word,
                'lang' : 'ja',
                'result_type' : 'popular',
                'count' : app_config.GET_TWEET_CNT
            }

            req2 = twitter.get(url2, params = params2)

            if req2.status_code == 200:
                search_timeline = json.loads(req2.text)

                for tweet in search_timeline['statuses']:
                    count_tweet += 1
                    trend_linked_tweet_cnt += 1

                    logger.debug('｜｜▽tweet')

                    tweet_datetime = utils.convert_datetime(tweet['created_at'])
                    tweet_url = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str']
                    tweet_text = removeNoise(tweet['full_text'])

                    # GCP実行
                    logger.debug('｜｜｜[GCP]tweet_text: %s, ', tweet_text)
                    tweet_sentiment = natural_language.getSentiment(tweet_text)
                    tweet_sentiment_score     = '{:.02f}'.format(tweet_sentiment.score)
                    tweet_sentiment_magnitude = '{:.05f}'.format(tweet_sentiment.magnitude)
                    tweet_valid_str_count = len(tweet_text)

                    trend_sentiment_score = trend_sentiment_score + float(tweet_sentiment_score)

                    logger.debug('｜｜｜tweet_sentiment_score :%s', tweet_sentiment_score)


                    tweet_insert_value = "'@" + tweet['user']['screen_name'] + "'"
                    tweet_insert_value = tweet_insert_value + ", '" + tweet_text + "'"
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet['retweet_count'])
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet['favorite_count'])
                    tweet_insert_value = tweet_insert_value + ", '" + tweet_url + "'"
                    tweet_insert_value = tweet_insert_value + ", '" + str(tweet_datetime) + "'"
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet_sentiment_score)
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet_sentiment_magnitude)
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet_valid_str_count)

                    #print ("tweet_insert_value＝" + tweet_insert_value)

                    tweetdbDao.insertTweetTbl(db_connection, db_cursol, tweet_insert_value)
                    tweet_id = tweetdbDao.getMaxIdTweetTbl(db_cursol)

                    logger.debug('｜｜｜tweet_id: %s, tweet_url: %s', str(tweet_id), tweet_url)

                    if tweetdbDao.getExistRecordByTrendTweet(db_cursol, trendid, tweet_id) == False:
                        tweetdbDao.insertTrendTweet(db_connection, db_cursol, trendid, tweet_id)
                    else:
                        pass

                    # ------------------------------------------------------------------------
                    # GCP Entity解析処理
                    # ------------------------------------------------------------------------
                    tweet_entities = analyze_entities.getAnalizeEntityResult(tweet_text)
                    for entity in tweet_entities.entities:
                        entity_name = entity.name
                        entity_type = format(enums.Entity.Type(entity.type).name)
                        entity_salience = float(entity.salience)
                        entity_url = ""

                        # 「NUMBER」タイプは登録処理をスキップする
                        if entity_type ==  "NUMBER":
                            pass
                        else:
                            # ■固有名詞テーブル登録処理
                            if tweetdbDao.getExistRecordByWordName(db_cursol, entity_name) == False:
                                tweetdbDao.insertWordNameTbl(db_connection, db_cursol, entity_name, entity_type, entity_url, entity_salience)
                            else:
                                pass

                            entity_wordnameid = tweetdbDao.getWordNameId(db_cursol, entity_name)

                            # ■ツイート関連固有名詞テーブル登録処理
                            if tweetdbDao.getExistRecordByTweetWordName(db_cursol, tweet_id, entity_wordnameid) == False:
                                tweetdbDao.insertTweetWordNameTbl(db_connection, db_cursol, tweet_id, entity_wordnameid)
                            else:
                                tweetdbDao.updateTweetWordNameTbl(db_connection, db_cursol, tweet_id, entity_wordnameid)

                    # ハッシュタグ
                    hashtaglist = tweet['entities']['hashtags']

                    for hashtag in hashtaglist:
                        tweet_hashtag = hashtag['text']

                        tweet_hashtagid = tweetdbDao.getHashTagId(db_cursol, tweet_hashtag)

                        if tweet_hashtagid < 0:
                            tweetdbDao.insertHashTagTbl(db_connection, db_cursol, tweet_hashtag)
                            tweet_hashtagid = tweetdbDao.getHashTagId(db_cursol, tweet_hashtag)
                            count_hashtag += 1
                        else:
                            pass

                        if tweetdbDao.getExistRecordByTweetHashtag(db_cursol, tweet_id, tweet_hashtagid) == False:
                            tweetdbDao.insertTweetHashtagTbl(db_connection, db_cursol, tweet_id, tweet_hashtagid)
                        else:
                            pass

                    # リンクURL
                    link_url_list = tweet['entities']['urls']

                    for link_url in link_url_list:
                        url = link_url['expanded_url']

                        url_id = tweetdbDao.getUrlId(db_cursol, url)

                        if url_id < 0:
                            # スクレイピング
                            #web_res = requests.get(url).text

                            #web_soup = BeautifulSoup(requests.get(url).apparent_encoding,  'html.parser')

                            #web_soup = BeautifulSoup(web_res, 'html.parser')

                            html = requests.get(url)
                            html.encoding = html.apparent_encoding
                            web_soup = BeautifulSoup(html.text, "html.parser")


                            ptag = web_soup.find_all("p")
                            url_title = web_soup.find_all("title")
                            ptag_value = ""
                            url_title_value = ""

                            for p in ptag:
                                ptag_value = ptag_value + '　' + p.text

                            for ptitle in url_title:
                                url_title_value = url_title_value + '　' + ptitle.text

                            ptag_value = removeNoise(ptag_value)
                            url_title_value = removeNoise(url_title_value)

                            # GCP実行
                            logger.debug('｜｜｜[GCP]ptag_value: %s, ', ptag_value)
                            ulr_sentiment = natural_language.getSentiment(ptag_value)
                            ulr_sentiment_score     = '{:.02f}'.format(ulr_sentiment.score)
                            ulr_sentiment_magnitude = '{:.05f}'.format(ulr_sentiment.magnitude)
                            ulr_valid_str_count = len(ptag_value)

                            url_insert_value = "'" + url + "'"
                            url_insert_value = url_insert_value + ", " + str(ulr_sentiment_score)
                            url_insert_value = url_insert_value + ", " + str(ulr_sentiment_magnitude)
                            url_insert_value = url_insert_value + ", " + str(ulr_valid_str_count)
                            url_insert_value = url_insert_value + ", '" + url_title_value + "'"
                            url_insert_value = url_insert_value + ", '" + ptag_value + "'"

                            tweetdbDao.insertUrlTbl(db_connection, db_cursol, url_insert_value)
                            url_id = tweetdbDao.getMaxUrlId(db_cursol)
                            count_linkedurl += 1

                            # ------------------------------------------------------------------------
                            # 文章テーブル登録処理
                            # ------------------------------------------------------------------------
                            url_sentences = removeNoise(ptag_value)
                            url_sentences = url_sentences.split("◆")

                            for sentence in url_sentences:
                                sentence = sentence.strip()

                                if len(sentence) > 1:
                                    if tweetdbDao.getExistRecordBySentence(db_cursol, sentence) == False:
                                        tweetdbDao.insertSentenceTbl(db_connection, db_cursol, sentence)
                                        sentence_id = tweetdbDao.getSentenceId(db_cursol, sentence)

                                    else:
                                        sentence_id = tweetdbDao.getSentenceId(db_cursol, sentence)
                                        tweetdbDao.updateSentence(db_connection, db_cursol, sentence_id)

                                    if tweetdbDao.getExistRecordBySentenceUrl(db_cursol, url_id, sentence_id) ==  False:
                                        tweetdbDao.insertSentenceUrlTbl(db_connection, db_cursol, url_id, sentence_id)
                                    else:
                                        pass

                                else:
                                    pass
                            # ------------------------------------------------------------------------
                            # GCP Entity解析処理
                            # ------------------------------------------------------------------------
                            web_entities = analyze_entities.getAnalizeEntityResult(ptag_value)
                            for entity in web_entities.entities:
                                entity_name = removeNoise(entity_name)
                                entity_type = format(enums.Entity.Type(entity.type).name)
                                entity_salience = float(entity.salience)
                                entity_url = ""

                                # 「NUMBER」タイプは登録処理をスキップする
                                if entity_type ==  "NUMBER":
                                    pass
                                else:
                                    # ■固有名詞テーブル登録処理
                                    if tweetdbDao.getExistRecordByWordName(db_cursol, entity_name) == False:
                                        logger.debug('｜｜｜getExistRecordByWordName(entity_name): %s', entity_name)
                                        tweetdbDao.insertWordNameTbl(db_connection, db_cursol, entity_name, entity_type, entity_url, entity_salience)
                                    else:
                                        pass

                                    entity_wordnameid = tweetdbDao.getWordNameId(db_cursol, entity_name)

                                    # ■Web関連固有名詞テーブル登録処理
                                    if tweetdbDao.getExistRecordByUrlWordName(db_cursol, url_id, entity_wordnameid) == False:
                                        tweetdbDao.insertUrlWordNameTbl(db_connection, db_cursol, url_id, entity_wordnameid)
                                    else:
                                        tweetdbDao.updateUrlWordNameTbl(db_connection, db_cursol, url_id, entity_wordnameid)

                        else:
                            pass

                        if tweetdbDao.getExistRecordByTweetUrl(db_cursol, tweet_id, url_id) == False:
                            tweetdbDao.insertTweetUrl(db_connection, db_cursol, tweet_id, url_id)
                        else:
                            pass

                    logger.debug('｜｜△')

                # トレンド情報にGCP結果を更新
                if trend_linked_tweet_cnt <= 0:
                    ave_tweet_sentiment_score = 0
                else:
                    ave_tweet_sentiment_score = trend_sentiment_score/trend_linked_tweet_cnt

                tweetdbDao.updateTrendTblGcpResult(db_connection, db_cursol, trendid, ave_tweet_sentiment_score)

                logger.debug('｜△')

            else:
                logger.debug('｜!ERR! StatusCode: %s', req2.status_code)
                logger.debug('｜△')

    else:
        logger.debug('｜◇Twitter OAuth認証≪失敗≫')
        logger.debug('｜!ERR! StatusCode: %s', req.status_code)

    logger.info('｜トレンド情報登録[正常終了]')

    db_connection.commit()
    db_connection.close()

    logger.info('｜count_trend    : %d'    , count_trend)
    logger.info('｜count_tweet    : %d'    , count_tweet)
    logger.info('｜count_hashtag  : %d'  , count_hashtag)
    logger.info('｜count_linkedurl: %d', count_linkedurl)
    logger.info('▲▲▲▲▲▲END▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')


def removeNoise(str):
    from util import utils

    result_str = str
    result_str = utils.removeSingleCotation(result_str)
    result_str = utils.removeEmojiStr(result_str)
    result_str = utils.removeUrlLinkStr(result_str)
    result_str = utils.removeHashTagStr(result_str)
    result_str = utils.removeHashTag2Str(result_str)
    result_str = utils.removeMensyonStr(result_str)
    result_str = utils.removeKaigyou(result_str)
    result_str = utils.removeTabStr(result_str)
    result_str = utils.removeSpacesStr(result_str)

    return result_str


if __name__ == '__main__':
    run_searchTrendInfo()


"""
def schedule(interval, f, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)


if __name__ == '__main__':
    schedule(300, run_searchTrendInfo)
    #run_searchTrendInfo()
"""
