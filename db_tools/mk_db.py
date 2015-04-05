import sqlite3

conn = sqlite3.connect('wrs.db')
c = conn.cursor()

sql1 = '''CREATE TABLE user(
    id          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    single_id   TEXT,
    name        TEXT NOT NULL
)'''

sql2 = '''CREATE TABLE report(
    id          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    job         TEXT NOT NULL,
    risk        TEXT NOT NULL,
    plan        TEXT NOT NULL,
    postdate    TEXT NOT NULL,
    
    who         TEXT NOT NULL
)'''

sql3 = '''CREATE TABLE issue(
    id          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    item        TEXT NOT NULL,
    detail      TEXT NOT NULL,
    status      TEXT NOT NULL,
    postdate    TEXT NOT NULL,
    
    who         TEXT NOT NULL
)'''



c.execute(sql1)
c.execute(sql2)
c.execute(sql3)
conn.commit()

c.close()
conn.close()
