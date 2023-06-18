from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

PAGES = ["Homepage", "Data", "Add/Edit Idea"]
DB_URL = 'postgresql://postgres:postgres@localhost:5432/postgres'
TIMEZONE = pytz.timezone('Australia/Perth')
COLUMNS = ['topic', 'summary', 'primary_tags', 'secondary_tags', 'link', 'quotes', 'media', 'created_at', 'updated_at']

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
metadata = MetaData()
ideas = Table('ideas', metadata, autoload_with=engine)

from sqlalchemy import text

def create_filtered_df(session, search_term=None):
    result = session.execute(text("SELECT * FROM ideas"))
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

    df['primary_tags'].fillna("", inplace=True)
    df['secondary_tags'].fillna("", inplace=True)
    df['summary'].fillna("", inplace=True)

    if search_term:
        df = df[df['summary'].str.contains(search_term, case=False) |
                df['primary_tags'].str.contains(search_term, case=False) |
                df['secondary_tags'].str.contains(search_term, case=False)]
    return df

def display_idea_details(row):
    expander = st.expander(row['topic'] + " : " + row['summary'])
    with expander:
        for column in COLUMNS:
            st.write(f"{column.title().replace('_', ' ')}: {row[column]}")

def idea_input_fields(session):
    idea = {column: st.text_input(column.title().replace('_', ' ')) for column in COLUMNS[:-2]}
    idea['created_at'] = idea['updated_at'] = datetime.now(TIMEZONE)

    if st.button('Submit'):
        session.execute(text(f"INSERT INTO ideas({','.join(COLUMNS)}) VALUES (:{',:'.join(COLUMNS)})"), idea)
        session.commit()

def app():
    st.title("Lifetime Thought Tracker")
    page = st.sidebar.selectbox("Choose a page", PAGES)

    session = Session()

    if page == "Homepage":
        st.header("Welcome to Lifetime Thought Tracker!")
        search = st.text_input("Search ideas")

        if search:
            df = create_filtered_df(session, search_term=search)
            for _, row in df.head(4).iterrows():
                display_idea_details(row)
        else:
            st.write("Use the search box above to find ideas or use the sidebar to navigate to different pages of the application.")

    elif page == "Data":
        keyword = st.text_input("Enter a keyword")

        df = create_filtered_df(session, search_term=keyword)
        st.dataframe(df)

        for _, row in df.iterrows():
            if st.button(f"Delete Idea {row['id']}"):
                session.execute("DELETE FROM ideas WHERE id=:id", {"id": row['id']})
                session.commit()
                st.success(f"Idea {row['topic']} deleted successfully!") 

    elif page == "Add/Edit Idea":
        idea_input_fields(session)

    session.close()

if __name__ == "__main__":
    app()
