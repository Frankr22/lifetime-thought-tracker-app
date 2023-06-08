import pandas as pd

DB_FILE = "ideas.csv"

def create_table():
    # Check if ideas.csv exists and if not, create it with column names
    try:
        df = pd.read_csv('ideas.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['summary', 'primary_tags', 'secondary_tags', 'link', 'quotes', 'media'])
        df.to_csv('ideas.csv', index=False)

def add_idea(idea):
    df = pd.read_csv('ideas.csv')
    new_idea = pd.Series(idea, index=df.columns)
    df = df.append(new_idea, ignore_index=True)
    df.to_csv('ideas.csv', index=False)

def add_or_update_idea(conn, idea, idea_id=None):
    if idea_id is None:
        sql = ''' INSERT INTO ideas(summary,primary_tags,secondary_tags,link,quotes,media)
                  VALUES(?,?,?,?,?,?) '''
    else:
        sql = ''' UPDATE ideas SET summary = ?, primary_tags = ?, secondary_tags = ?, link = ?, quotes = ?, media = ? WHERE id = ?'''

    cur = conn.cursor()
    cur.execute(sql, (*idea, idea_id) if idea_id is not None else idea)
    conn.commit()
    return cur.lastrowid

def fetch_all_ideas():
    df = pd.read_csv('ideas.csv')
    return df.values.tolist()

def delete_idea(conn, idea_id):
    sql = 'DELETE FROM ideas WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (idea_id,))
    conn.commit()
