import streamlit as st
from db_operations import create_connection, create_table, add_idea

def app():
    st.title('Lifetime Thought Tracker')

    with st.form(key='ideas_form'):
        summary = st.text_area('Summary', help='Write a summary of your idea or thought')
        primary_tags = st.text_input('Primary Tags', help='Enter primary tags')
        secondary_tags = st.text_input('Secondary Tags', help='Enter secondary tags')
        link = st.text_input('Reference Link', help='Enter the link of reference')
        quotes = st.text_area('Quotes', help='Enter important quotes')
        media = st.text_input('Media', help='Enter media links')

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            conn = create_connection()
            create_table(conn)
            idea = (summary, primary_tags, secondary_tags, link, quotes, media)
            add_idea(conn, idea)

if __name__ == '__main__':
    app()
