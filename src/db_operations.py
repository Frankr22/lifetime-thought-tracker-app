import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('ideas.db', check_same_thread=False)  # Create a persistent database file named ideas.db and allow connections from different threads
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql_create_ideas_table = """CREATE TABLE IF NOT EXISTS ideas (
                                        id integer PRIMARY KEY,
                                        summary text NOT NULL,
                                        primary_tags text,
                                        secondary_tags text,
                                        link text,
                                        quotes text,
                                        media text
                                    ); """
        conn.execute(sql_create_ideas_table)
    except Error as e:
        print(e)

def add_idea(conn, idea):
    sql = ''' INSERT INTO ideas(summary,primary_tags,secondary_tags,link,quotes,media)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, idea)
    conn.commit()
    return cur.lastrowid

def fetch_all_ideas(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ideas';")
    if cur.fetchone() is not None:
        cur.execute("SELECT * FROM ideas")
        rows = cur.fetchall()
        return rows
    else:
        return []
