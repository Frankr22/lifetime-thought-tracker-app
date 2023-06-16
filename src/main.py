from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import streamlit as st
import pandas as pd
from datetime import datetime

def app():
    st.title("Lifetime Thought Tracker")

    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Data", "Add/Edit Idea"])

    if page == "Homepage":
        st.header("Welcome to Lifetime Thought Tracker!")
        search = st.text_input("Search ideas")  # Add a search box

        # Only run this block if there's input in the search box
        if search:
            result = session.execute("SELECT * FROM ideas")
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

            # Make sure any NaN values are replaced with an empty string
            df['primary_tags'].fillna("", inplace=True)
            df['secondary_tags'].fillna("", inplace=True)
            df['summary'].fillna("", inplace=True)

            # Filter the DataFrame based on the search keyword
            df = df[df['summary'].str.contains(search, case=False) |
                    df['primary_tags'].str.contains(search, case=False) |
                    df['secondary_tags'].str.contains(search, case=False)]

            # Loop over each idea and create an expander for its details
            for index, row in df.iterrows():
                expander = st.expander(row['summary'])
                with expander:
                    st.write(f"Primary Tags: {row['primary_tags']}")
                    st.write(f"Secondary Tags: {row['secondary_tags']}")
                    st.write(f"Link: {row['link']}")
                    st.write(f"Quotes: {row['quotes']}")
                    st.write(f"Media: {row['media']}")
        else:
            st.write("Use the search box above to find ideas or use the sidebar to navigate to different pages of the application.")

    if page == "Data":
        keyword = st.text_input("Enter a keyword")

        # Execute the SQL command and fetch all the results
        result = session.execute("SELECT * FROM ideas")
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

        # Make sure any NaN values are replaced with an empty string
        df['primary_tags'].fillna("", inplace=True)
        df['secondary_tags'].fillna("", inplace=True)

        # Filter the DataFrame based on the keyword
        if keyword:
            df = df[
                (df['summary'].str.lower().str.contains(keyword.lower())) |
                (df['primary_tags'].str.lower().str.contains(keyword.lower())) |
                (df['secondary_tags'].str.lower().str.contains(keyword.lower()))
            ]

        # Display the ideas in a table
        st.dataframe(df)

        # Add a delete button for each idea
        for index, row in df.iterrows():
            if st.button(f"Delete Idea {row['id']}"):
                # Execute the SQL command to delete the idea
                session.execute("DELETE FROM ideas WHERE id=:id", {"id": row['id']})
                session.commit()
                st.success("Idea deleted successfully!")

    elif page == "Add/Edit Idea":
        idea_input_fields(session)

def idea_input_fields(session):
    summary = st.text_input('Summary')
    primary_tags = st.text_input('Primary Tags')
    secondary_tags = st.text_input('Secondary Tags')
    link = st.text_input('Link')
    quotes = st.text_input('Quotes')
    media = st.text_input('Media')

    if st.button('Submit'):
        idea = {
            'summary': summary, 
            'primary_tags': primary_tags, 
            'secondary_tags': secondary_tags, 
            'link': link, 
            'quotes': quotes, 
            'media': media,
            'created_at': datetime.now(),  # Set the created_at timestamp
            'updated_at': datetime.now()  # Set the updated_at timestamp
        }

        session.execute(
            text(
                "INSERT INTO ideas(summary, primary_tags, secondary_tags, link, quotes, media, created_at, updated_at) "
                "VALUES (:summary, :primary_tags, :secondary_tags, :link, :quotes, :media, :created_at, :updated_at)"
            ),
            idea
        )
        session.commit()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/thought_tracker_db')
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
ideas = Table('ideas', metadata, autoload_with=engine)

if __name__ == "__main__":
    app()
