import streamlit as st
from db_operations import create_table, add_or_update_idea, fetch_all_ideas, delete_idea
import pandas as pd

def app():
    conn = create_table()

    st.title('Lifetime Thought Tracker')

    page = st.sidebar.selectbox('Choose a page', ['Summaries', 'Add/Edit Ideas', 'Data'])

    idea_to_edit = st.sidebar.text_input('Enter the ID of the idea you want to edit')
    edit_button = st.sidebar.button('Edit Idea')

    if edit_button and idea_to_edit:
        ideas = fetch_all_ideas(conn)
        idea_to_edit = next((idea for idea in ideas if idea[0] == int(idea_to_edit)), None)

        if idea_to_edit is not None:
            page = 'Add/Edit Ideas'

    if page == 'Summaries':
        keyword = st.text_input('Enter keyword to search ideas')
        search_button = st.button('Search')  # Add search button

        if search_button:  # Only execute search when button is pressed
            ideas = fetch_all_ideas(conn)
            matching_ideas = [idea for idea in ideas if keyword.lower() in (idea[1] or "").lower() or keyword.lower() in (idea[2] or "").lower() or keyword.lower() in (idea[3] or "").lower()]

            if matching_ideas:  # Check if any ideas were found
                for idea in matching_ideas:
                    st.write(idea)
            else:  # If no ideas found, display a message
                st.write('No ideas found for this keyword')

    elif page == 'Add/Edit Ideas':
        with st.form(key='ideas_form'):
            idea_id = st.hidden_input('Idea ID', value=str(idea_to_edit[0]) if idea_to_edit is not None else '')
            summary = st.text_area('Summary', value=idea_to_edit[1] if idea_to_edit is not None else '', help='Write a summary of your idea or thought')
            primary_tags = st.text_input('Primary Tags', value=idea_to_edit[2] if idea_to_edit is not None else '', help='Enter primary tags')
            secondary_tags = st.text_input('Secondary Tags', value=idea_to_edit[3] if idea_to_edit is not None else '', help='Enter secondary tags')
            link = st.text_input('Reference Link', value=idea_to_edit[4] if idea_to_edit is not None else '', help='Enter the link of reference')
            quotes = st.text_area('Quotes', value=idea_to_edit[5] if idea_to_edit is not None else '', help='Enter important quotes')
            media = st.text_input('Media', value=idea_to_edit[6] if idea_to_edit is not None else '', help='Enter media links')

            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            summary = summary or ""
            primary_tags = primary_tags or ""
            secondary_tags = secondary_tags or ""
            link = link or ""
            quotes = quotes or ""
            media = media or ""

            if summary.strip() == '':
                st.error('Summary cannot be empty')
            else:
                idea = (summary, primary_tags, secondary_tags, link, quotes, media)
                add_or_update_idea(conn, idea, idea_id if idea_id else None)
                st.experimental_rerun()

    elif page == 'Data':
        st.header("Data View")
        ideas = fetch_all_ideas(conn)

        ideas_df = pd.DataFrame(ideas, columns=['ID', 'Summary', 'Primary Tags', 'Secondary Tags', 'Link', 'Quotes', 'Media'])
        st.table(ideas_df)

        delete_idea_id = st.text_input('Enter the ID of the idea you want to delete')
        delete_button = st.button('Delete Idea')

        if delete_button and delete_idea_id:
            delete_idea(conn, delete_idea_id)
            st.experimental_rerun()

if __name__ == '__main__':
    app()
