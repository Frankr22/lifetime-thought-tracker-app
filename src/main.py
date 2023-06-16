import streamlit as st
import pandas as pd
from sqlalchemy import text

def app():
    st.title('Lifetime Thought Tracker')
    conn = st.experimental_connection('thought_tracker_db', type='sql')
    conn.execute(text('''CREATE TABLE IF NOT EXISTS ideas
                (id SERIAL PRIMARY KEY, summary TEXT, primary_tags TEXT, secondary_tags TEXT, link TEXT, quotes TEXT, media TEXT)'''))

    page = st.sidebar.selectbox('Choose a page', ['Summaries', 'Add/Edit Ideas', 'Data'])

    if page == 'Summaries':
        keyword = st.text_input('Enter keyword to search ideas')
        search_button = st.button('Search')

        if search_button:
            result = conn.execute(text('SELECT * FROM ideas'))
            ideas = result.fetchall()
            matching_ideas = [idea for idea in ideas if keyword.lower() in (idea[1] or "").lower() or keyword.lower() in (idea[2] or "").lower() or keyword.lower() in (idea[3] or "").lower()]

            if matching_ideas:
                for idea in matching_ideas:
                    st.write(idea)
            else:
                st.write('No ideas found for this keyword')

    elif page == 'Add/Edit Ideas':
        idea_to_edit = None
        if 'edit_idea_id' in st.session_state:
            result = conn.execute(text('SELECT * FROM ideas WHERE id = :id'), {'id': st.session_state['edit_idea_id']})
            idea_to_edit = result.fetchone()

        with st.form(key='ideas_form'):
            summary = st.text_area('Summary', value=idea_to_edit[1] if idea_to_edit else '', help='Write a summary of your idea or thought')
            primary_tags = st.text_input('Primary Tags', value=idea_to_edit[2] if idea_to_edit else '', help='Enter primary tags')
            secondary_tags = st.text_input('Secondary Tags', value=idea_to_edit[3] if idea_to_edit else '', help='Enter secondary tags')
            link = st.text_input('Reference Link', value=idea_to_edit[4] if idea_to_edit else '', help='Enter the link of reference')
            quotes = st.text_area('Quotes', value=idea_to_edit[5] if idea_to_edit else '', help='Enter important quotes')
            media = st.text_input('Media', value=idea_to_edit[6] if idea_to_edit else '', help='Enter media links')

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
                if 'edit_idea_id' in st.session_state:
                    conn.execute(text('UPDATE ideas SET summary = :summary, primary_tags = :primary_tags, secondary_tags = :secondary_tags, link = :link, quotes = :quotes, media = :media WHERE id = :id'), {'summary': summary, 'primary_tags': primary_tags, 'secondary_tags': secondary_tags, 'link': link, 'quotes': quotes, 'media': media, 'id': st.session_state['edit_idea_id']})
                    del st.session_state['edit_idea_id']
                else:
                    conn.execute(text('INSERT INTO ideas(summary, primary_tags, secondary_tags, link, quotes, media) VALUES (:summary, :primary_tags, :secondary_tags, :link, :quotes, :media)'), {'summary': summary, 'primary_tags': primary_tags, 'secondary_tags': secondary_tags, 'link': link, 'quotes': quotes, 'media': media})

    elif page == 'Data':
        result = conn.execute(text('SELECT * FROM ideas'))
        ideas = result.fetchall()
        st.write(pd.DataFrame(ideas, columns=['ID', 'Summary', 'Primary Tags', 'Secondary Tags', 'Link', 'Quotes', 'Media']))
        delete_button = st.button('Delete selected')

        if delete_button:
            selected_idea = st.selectbox('Select an idea to delete', ideas)
            if selected_idea:
                conn.execute(text('DELETE FROM ideas WHERE id = :id'), {'id': selected_idea[0]})
            else:
                st.write('No ideas found')

if __name__ == '__main__':
    app()
