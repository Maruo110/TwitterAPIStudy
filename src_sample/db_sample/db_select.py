# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TWEET_DATA.sqlite'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# Insert a row of data
#cur.execute("INSERT INTO persons(name) values('Mike')")
#cur.execute("INSERT INTO persons(name) values('John')")
#cur.execute("INSERT INTO persons(name) values('Will')")

# Browse inserted data
cur.execute("SELECT * FROM persons")
print(cur.fetchall())

# データベースへコミット。これで変更が反映される。
cur.close()
conn.close()
