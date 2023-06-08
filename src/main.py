import streamlit as st
from db_operations import create_connection, create_table, add_idea, fetch_all_ideas

def app():
    st.title('Lifetime Thought Tracker')
    conn = create_connection()
    create_table(conn)

    page = st.sidebar.selectbox('Choose a page', ['Summaries', 'Add/Edit Ideas', 'Data'])

    if page == 'Summaries':
        keyword = st.text_input('Enter keyword to search ideas')
        search_button = st.button('Search')  # Add search button

        if search_button:  # Only execute search when button is pressed
            ideas = fetch_all_ideas(conn)
            matching_ideas = [idea for idea in ideas if keyword.lower() in idea[1].lower() or keyword.lower() in idea[2].lower()]

            if matching_ideas:  # Check if any ideas were found
                for idea in matching_ideas:
                    st.write(idea)
            else:  # If no ideas found, display a message
                st.write('No ideas found for this keyword')

    elif page == 'Add/Edit Ideas':
        with st.form(key='ideas_form'):
            summary = st.text_area('Summary', help='Write a summary of your idea or thought')
            primary_tags = st.text_input('Primary Tags', help='Enter primary tags')
            secondary_tags = st.text_input('Secondary Tags', help='Enter secondary tags')
            link = st.text_input('Reference Link', help='Enter the link of reference')
            quotes = st.text_area('Quotes', help='Enter important quotes')
            media = st.text_input('Media', help='Enter media links')

            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                idea = (summary, primary_tags, secondary_tags, link, quotes, media)
                add_idea(conn, idea)
                st.experimental_rerun()

    elif page == 'Data':
        st.header("Data View")
        ideas = fetch_all_ideas(conn)
        
        # convert to pandas DataFrame for better visualization
        ideas_df = pd.DataFrame(ideas, columns=['ID', 'Title', 'Description', 'Primary Tags', 'Secondary Tags', 'Link', 'Quotes'])
        st.table(ideas_df)

if __name__ == '__main__':
    app()
