# -*- coding: utf-8 -*-
from google.cloud.language_v1.proto.language_service_pb2 import Sentence

def getInsertSqlStatement(tblNm, colList, insertValues):
    sql= "INSERT INTO " + tblNm + "(" + colList + ") values(" + insertValues + ")"
    print(sql)
    return sql

def getSelectMaxSqlStatement(tblNm, colNm):
    sql= "SELECT MAX(" + colNm + ") FROM " + tblNm
    print(sql)
    return sql

def getSelectSqlStatement(tblNm, colNm, whereValues):
    sql= "SELECT " + colNm + " FROM " + tblNm + " WHERE " + whereValues
    print(sql)
    return sql

def getUpdateSqlStatement(tblNm, setValues, whereValues):
    sql= "UPDATE " + tblNm + " SET " + setValues + " WHERE " + whereValues
    print(sql)
    return sql

# ===============================================================================================================

def insertTrendTbl(conn, cur, syutokuymd, syutokutime, tweetvolume, avetweetsentimentscore, trendword):

    tblNm = "app_trend"
    colList = "syutokuymd, syutokutime, tweetvolume, avetweetsentimentscore, trendword"
    insertValues = "'" + str(syutokuymd) + "', "
    insertValues = insertValues +  "'" + str(syutokutime) + "', "
    insertValues = insertValues +  str(tweetvolume) + ", "
    insertValues = insertValues +  str(avetweetsentimentscore) + ", "
    insertValues = insertValues +  "'" + trendword + "'"

    cur.execute(getInsertSqlStatement(tblNm, colList, insertValues))
    conn.commit()


def getMaxIdByTrendTbl(cur):
    tblNm = "app_trend"
    colNm = "id"

    cur.execute(getSelectMaxSqlStatement(tblNm, colNm))
    result = cur.fetchone()
    return  int(result[0])


def updateTrendTblGcpResult(conn, cur, trend_id, avetweetsentimentscore):

    tblNm = "app_trend"
    setValues = "avetweetsentimentscore = " + str(avetweetsentimentscore)
    whereValues = "id = " + str(trend_id)

    cur.execute(getUpdateSqlStatement(tblNm, setValues, whereValues))
    conn.commit()


def insertTweetTbl(conn, cur, userid, retweetvolume, favoritevolume, tweeturl, tweettime, tweetsentimentscore, tweetsentimentsmagnitude, tweetvalidstrcount, trend_id, url_id, tweettext):
    tblNm = "app_tweet"
    colList = "userid, retweetvolume, favoritevolume, tweeturl, tweettime, tweetsentimentscore, tweetsentimentsmagnitude, tweetvalidstrcount, trend_id, url_id, tweettext"

    insertValues = "'" + userid + "', "
    insertValues = insertValues +  str(retweetvolume) + ", "
    insertValues = insertValues +  str(favoritevolume) + ", "
    insertValues = insertValues +  "'" + tweeturl + "', "
    insertValues = insertValues +  "'" + str(tweettime) + "', "
    insertValues = insertValues +  str(tweetsentimentscore) + ", "
    insertValues = insertValues +  str(tweetsentimentsmagnitude) + ", "
    insertValues = insertValues +  str(tweetvalidstrcount) + ", "
    insertValues = insertValues +  str(trend_id) + ", "
    insertValues = insertValues +  str(url_id) + ", "
    insertValues = insertValues +  "'" + str(tweettext) + "'"

    cur.execute(getInsertSqlStatement(tblNm, colList, insertValues))
    conn.commit()


def getMaxIdByTweetTbl(cur):
    tblNm = "app_tweet"
    colNm = "id"

    cur.execute(getSelectMaxSqlStatement(tblNm, colNm))
    result = cur.fetchone()
    return  int(result[0])


def updateTweetTblUrlId(conn, cur, tweet_id, url_id):

    tblNm = "app_tweet"
    setValues = "url_id = " + str(url_id)
    whereValues = "id = " + str(tweet_id)

    cur.execute(getUpdateSqlStatement(tblNm, setValues, whereValues))
    conn.commit()


def insertUrlTbl(conn, cur, linkedurl, sentimentscore, sentimentsmagnitude, validstrcount, title, contents):

    tblNm = "app_url"
    colList = "linkedurl, sentimentscore, sentimentsmagnitude, validstrcount, title, contents"
    insertValues = "'" + linkedurl + "', "
    insertValues = insertValues +  str(sentimentscore) + ", "
    insertValues = insertValues +  str(sentimentsmagnitude) + ", "
    insertValues = insertValues +  str(validstrcount) + ", "
    insertValues = insertValues +  "'" + title + "', "
    insertValues = insertValues +  "'" + contents + "'"

    cur.execute(getInsertSqlStatement(tblNm, colList, insertValues))
    conn.commit()

def getMaxIdByUrlTbl(cur):
    tblNm = "app_url"
    colNm = "id"

    cur.execute(getSelectMaxSqlStatement(tblNm, colNm))
    result = cur.fetchone()
    return  int(result[0])


def getUrlIdByUrlTbl(cur, url):

    tblNm = "app_url"
    colNm = "id"
    whereValues = "linkedurl = '" + url + "'"

    cur.execute(getSelectSqlStatement(tblNm, colNm, whereValues))

    result = cur.fetchone()

    if result is None:
        return -1
    else:
        return  int(result[0])
