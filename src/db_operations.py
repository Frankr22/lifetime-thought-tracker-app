import sqlite3

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(':memory:')   # Creates an in-memory SQLite database
        return conn
    except Error as e:
        print(e)

def close_connection(conn):
    conn.close()

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ideas
                (id INTEGER PRIMARY KEY AUTOINCREMENT, summary TEXT, primary_tags TEXT, secondary_tags TEXT, link TEXT, quotes TEXT, media TEXT)''')
    conn.commit()

def add_idea(idea):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO ideas(summary, primary_tags, secondary_tags, link, quotes, media) VALUES (?,?,?,?,?,?)', idea)
    conn.commit()

def fetch_all_ideas():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM ideas')
    ideas = c.fetchall()
    return ideas

def fetch_idea(id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM ideas WHERE id = ?', (id,))
    idea = c.fetchone()
    return idea

def update_idea(idea, id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('UPDATE ideas SET summary = ?, primary_tags = ?, secondary_tags = ?, link = ?, quotes = ?, media = ? WHERE id = ?', (*idea, id))
    conn.commit()

def delete_idea(id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM ideas WHERE id = ?', (id,))
    conn.commit()
