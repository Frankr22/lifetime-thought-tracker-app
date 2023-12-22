from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, DateTime, text
from sqlalchemy.orm import sessionmaker
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

PAGES = ["Homepage", "Data", "Add/Edit Idea"]
DB_URL = 'sqlite:///ideas.db'
TIMEZONE = pytz.timezone('Australia/Perth')
COLUMNS = ['id', 'title', 'summary', 'primary_tags', 'secondary_tags', 'sources', 'status', 'notes', 'date_added', 'date_last_updated']

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

metadata = MetaData()

# Manually define the 'ideas' table
ideas = Table(
    'ideas',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('summary', String),
    Column('primary_tags', String),
    Column('secondary_tags', String),
    Column('sources', String),
    Column('status', String),
    Column('notes', String),
    Column('date_added', DateTime),  # Change the type to DateTime
    Column('date_last_updated', DateTime),  # Change the type to DateTime
)

metadata.create_all(engine)

def create_filtered_df(session, search_term=None, primary_tag=None):
    result = session.execute(text("SELECT * FROM ideas"))
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

    df['primary_tags'].fillna("", inplace=True)
    df['secondary_tags'].fillna("", inplace=True)
    df['summary'].fillna("", inplace=True)

    if search_term:
        df = df[df['summary'].str.contains(search_term, case=False) |
                df['primary_tags'].str.contains(search_term, case=False) |
                df['secondary_tags'].str.contains(search_term, case=False)]

    if primary_tag:
        df = df[df['primary_tags'].str.contains(primary_tag, case=False)]

    return df

def display_idea_details(row):
    expander = st.expander(row['title'] + " : " + row['summary'])
    with expander:
        for column in COLUMNS:
            st.write(f"{column.title().replace('_', ' ')}: {row[column]}")

def get_all_primary_tags(session):
    select_query = session.execute(text("SELECT DISTINCT primary_tags FROM ideas"))
    all_tags = set()

    for row in select_query:
        tags = row[0]
        if tags:
            all_tags.update(tags.split(','))

    return sorted(all_tags)

def idea_input_fields(session):
    st.write("## Add a new idea")

    title = st.text_input("Title", help="Enter the title for your thought. This should be succinct, encapsulating the main idea in up to 60 characters.")
    summary = st.text_area("Summary", help="This is the body of your thought. Ensure your thoughts are digestible and clear, limiting to 280 characters.")
    primary_tags_str = st.text_input("Primary Tags", help="Assign one or two primary tags to broadly categorize your thoughts. For example, 'personal', 'work', 'science', 'literature'. Separate multiple tags with commas.")
    secondary_tags_str = st.text_input("Secondary Tags", help="Enter specific tags related to certain themes or ideas. There's no strict limit on these, but aim for 2-5 for usability. Separate with commas.")
    sources = st.text_input("Sources", help="Keep track of any references or sources that are relevant to your thought.")
    status = st.selectbox("Status", options=["idea", "in progress", "completed"], help="Choose the status of your thought. This can be useful if you plan to do something with certain thoughts.")
    notes = st.text_area("Notes", help="This is an optional field for any additional thoughts or follow-up ideas you might have.")

    # Convert string of tags to list
    primary_tags = [tag.strip() for tag in primary_tags_str.split(",")]
    secondary_tags = [tag.strip() for tag in secondary_tags_str.split(",")]

    if st.button('Submit'):
        new_idea = {
            "title": title,
            "summary": summary,
            "primary_tags": primary_tags_str,
            "secondary_tags": secondary_tags_str,
            "sources": sources,
            "status": status,
            "notes": notes,
            "date_added": datetime.now(TIMEZONE),
            "date_last_updated": datetime.now(TIMEZONE)
        }

        insert_query = ideas.insert().values(new_idea)
        session.execute(insert_query)
        session.commit()
        st.success("Idea added successfully!")

def app():
    st.title("Lifetime Thought Tracker")
    page = st.sidebar.selectbox("Choose a page", PAGES)

    session = Session()

    if page == "Homepage":
        st.header("Welcome to Lifetime Thought Tracker!")
        search = st.text_input("Search ideas")
        primary_tag = st.selectbox('Select a primary tag', options=get_all_primary_tags(session))

        if search:
            df = create_filtered_df(session, search_term=search, primary_tag=primary_tag)
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
                st.success(f"Idea {row['title']} deleted successfully!") 

    elif page == "Add/Edit Idea":
        idea_input_fields(session)

    session.close()

if __name__ == "__main__":
    app()
