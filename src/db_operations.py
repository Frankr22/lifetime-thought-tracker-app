import pandas as pd

DB_FILE = "ideas.csv"

def create_table():
    try:
        df = pd.DataFrame(columns=['summary', 'primary_tags', 'secondary_tags', 'link', 'quotes', 'media'])
        df.to_csv(DB_FILE, index=False)
    except Exception as e:
        print(e)

def add_idea(idea):
    try:
        df = pd.read_csv(DB_FILE)
        df.loc[len(df.index)] = list(idea)
        df.to_csv(DB_FILE, index=False)
    except Exception as e:
        print(e)

def fetch_all_ideas():
    try:
        df = pd.read_csv(DB_FILE)
        return df.values.tolist()
    except Exception as e:
        print(e)
        return []
