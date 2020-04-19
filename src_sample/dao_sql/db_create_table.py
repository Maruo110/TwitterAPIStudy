# -*- coding: utf-8 -*-

import sqlite3

print('START')
dbname = 'TWEET_DATA.sqlite'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# personsというtableを作成してみる
# 大文字部はSQL文。小文字でも問題ない。
cur.execute("CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)")

# データベースへコミット。これで変更が反映される。
conn.commit()
conn.close()
print('END')