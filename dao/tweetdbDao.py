# -*- coding: utf-8 -*-

def insertTrendTbl(conn, cur, insertValues):

    cur.execute("INSERT INTO t_trend(s_trendword, s_syutokuymd, s_syutokutime, n_tweetvolume, n_hashtagflg, n_hashtagid) values(" + insertValues + ")")
    conn.commit()


def getMaxIdTrendTbl(cur):

    cur.execute("SELECT max(n_trendid) FROM t_trend")

    result = cur.fetchone()
    return  int(result[0])

def updateTrendTblGcpResult(conn, cur, trend_id, trend_sentiment_score):

    cur.execute("UPDATE t_trend set r_avetweetsentimentscore = " + str(trend_sentiment_score) + " where n_trendid = " + str(trend_id))
    conn.commit()


def insertTweetTbl(conn, cur, insertValues):

    cur.execute("INSERT INTO t_tweet(s_userid, s_tweettext, n_retweetvolume, n_favoritevolume, s_tweeturl, s_tweettime, r_tweetsentimentscore, r_tweetsentimentsmagnitude, n_tweetvalidstrcount) values(" + insertValues + ")")
    conn.commit()


def getMaxIdTweetTbl(cur):

    cur.execute("SELECT max(n_tweetid) FROM t_tweet")

    result = cur.fetchone()
    return  int(result[0])


def insertTrendTweet(conn, cur, trend_id, tweet_id):

    cur.execute("INSERT INTO t_trendtweet(n_trendid, n_tweetid) values(" + str(trend_id) + ", " + str(tweet_id) + ")")
    conn.commit()


def getExistRecordByTrendTweet(cur, trend_id, tweet_id):

    cur.execute("SELECT count(n_trendid) FROM t_trendtweet where n_trendid = " + str(trend_id) + " and n_tweetid = " + str(tweet_id))

    result = cur.fetchone()

    if int(result[0]) > 0:
        return True
    else:
        return False

def getHashTagId(cur, hashtag_word):

    cur.execute("SELECT n_hashtagid FROM t_hashtag where s_hashtagword = '" + hashtag_word + "'")

    result = cur.fetchone()

    if result is None:
        return -1
    else:
        return  int(result[0])


def insertHashTagTbl(conn, cur, hashtag_word):
    cur.execute("INSERT INTO t_hashtag(s_hashtagword) values('" + hashtag_word + "')")
    conn.commit()


def insertUrlTbl(conn, cur, insertValues):
    cur.execute("INSERT INTO t_url(s_linkedurl, r_sentimentscore, r_sentimentsmagnitude, n_validstrcount, s_title) values(" + insertValues + ")")
    conn.commit()


def getUrlId(cur, url):
    cur.execute("SELECT n_linkedurlid FROM t_url where s_linkedurl = '" + url + "'")

    result = cur.fetchone()

    if result is None:
        return -1
    else:
        return  int(result[0])


def getMaxUrlId(cur):

    cur.execute("SELECT max(n_linkedurlid) FROM t_url")

    result = cur.fetchone()
    return  int(result[0])

def insertTweetUrl(conn, cur, tweet_id, url_id):

    cur.execute("INSERT INTO t_tweeturl(n_tweetid, n_linkedurlid) values(" + str(tweet_id) + ", " + str(url_id) + ")")
    conn.commit()

def getExistRecordByTweetUrl(cur, tweet_id, url_id):

    cur.execute("SELECT count(n_tweetid) FROM t_tweeturl where n_tweetid = " + str(tweet_id) + " and n_linkedurlid= " + str(url_id))

    result = cur.fetchone()

    if int(result[0]) > 0:
        return True
    else:
        return False


def insertTweetHashtagTbl(conn, cur, tweet_id, hashtag_id):

    cur.execute("INSERT INTO t_tweethashtag(n_tweetid, n_hashtagid) values(" + str(tweet_id) + ", " + str(hashtag_id) + ")")
    conn.commit()


def getExistRecordByTweetHashtag(cur, tweet_id, hashtag_id):

    cur.execute("SELECT count(n_tweetid) FROM t_tweethashtag where n_tweetid = " + str(tweet_id) + " and n_hashtagid= " + str(hashtag_id))

    result = cur.fetchone()

    if int(result[0]) > 0:
        return True
    else:
        return False

def getExistRecordByWordName(cur, word_name):

    cur.execute("SELECT count(n_wordnameid) FROM t_wordname where s_wordname = '" + word_name + "'")

    result = cur.fetchone()

    if int(result[0]) > 0:
        return True
    else:
        return False


def insertWordNameTbl(conn, cur, word_name, word_type, wikipedia_url, saliences_score):

    insert_value = "'" + word_name + "'"
    insert_value = insert_value + ", '" + word_type + "'"
    insert_value = insert_value + ", '" + wikipedia_url + "'"
    insert_value = insert_value + ", " + str(saliences_score)

    cur.execute("INSERT INTO t_wordname(s_wordname, s_wordtype, s_wikipediaurl, r_saliencescore) values(" + insert_value + ")")
    conn.commit()


def getExistRecordByTweetWordName(cur, tweet_id, wordname_id):

    from_statement = "t_tweetwordname"
    select_statement = "count(n_tweetid)"

    where_statement = "n_tweetid = " + str(tweet_id)
    where_statement = where_statement + " and n_wordnameid = " + str(wordname_id)

    cur.execute("SELECT " + select_statement + " FROM " + from_statement + " where "+ where_statement)

    result = cur.fetchone()

    if int(result[0]) > 0:
        return True
    else:
        return False

def getWordNameId(cur, word_name):

    where_statement = "s_wordname = '" + word_name + "'"

    cur.execute("SELECT max(n_wordnameid) FROM t_wordname WHERE " + where_statement)

    result = cur.fetchone()
    return  int(result[0])


def insertTweetWordNameTbl(conn, cur, tweet_id, wordname_id):

    table_name = "t_tweetwordname"

    insert_value = str(tweet_id)
    insert_value = insert_value + ", " + str(wordname_id)
    insert_value = insert_value + ", 1"

    cur.execute("INSERT INTO " + table_name + " (n_tweetid, n_wordnameid, n_count) values(" + insert_value + ")")
    conn.commit()


def updateTweetWordNameTbl(conn, cur, tweet_id, wordname_id):

    where_statement = "n_tweetid = " + str(tweet_id)
    where_statement = where_statement + " and n_wordnameid = " + str(wordname_id)

    cur.execute("SELECT n_count FROM t_tweetwordname WHERE " + where_statement)

    result = cur.fetchone()

    cur.execute("UPDATE t_tweetwordname set n_count = " + str(int(result[0]) + 1) + " where " + where_statement)
    conn.commit()

"""
def getHashTagId(cur, hashtag_word):
    cur.execute("SELECT n_hashtagid FROM t_hashtag where s_hashtagword = '" + hashtag_word + "'")

    result = cur.fetchone()
    return  int(result[0])
"""
