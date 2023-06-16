import streamlit as st
import pandas as pd

def app():
    st.title('Lifetime Thought Tracker')
    
    conn = st.experimental_connection('thought_tracker_db', type='sql')

    page = st.sidebar.selectbox('Choose a page', ['Summaries', 'Add/Edit Ideas', 'Data'])

    if page == 'Summaries':
        keyword = st.text_input('Enter keyword to search ideas')
        search_button = st.button('Search')

        if search_button:
            ideas = conn.query('SELECT * FROM ideas')
            matching_ideas = [idea for idea in ideas if keyword.lower() in (idea[1] or "").lower() or keyword.lower() in (idea[2] or "").lower() or keyword.lower() in (idea[3] or "").lower()]

            if matching_ideas:
                for idea in matching_ideas:
                    st.write(idea)
            else:
                st.write('No ideas found for this keyword')

    elif page == 'Add/Edit Ideas':
        idea_to_edit = None
        if 'edit_idea_id' in st.session_state:
            idea_to_edit = conn.query(f'SELECT * FROM ideas WHERE id = {st.session_state["edit_idea_id"]}')[0]

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
                    conn.session.execute(f'UPDATE ideas SET summary = "{summary}", primary_tags = "{primary_tags}", secondary_tags = "{secondary_tags}", link = "{link}", quotes = "{quotes}", media = "{media}" WHERE id = {st.session_state["edit_idea_id"]}')
                    conn.session.commit()
                    del st.session_state['edit_idea_id']
                else:
                    conn.session.execute(f'INSERT INTO ideas (summary, primary_tags, secondary_tags, link, quotes, media) VALUES ("{summary}", "{primary_tags}", "{secondary_tags}", "{link}", "{quotes}", "{media}")')
                    conn.session.commit()
                st.experimental_rerun()

    elif page == 'Data':
        st.header("Data View")
        ideas = conn.query('SELECT * FROM ideas')
        ideas_df = pd.DataFrame(ideas, columns=['ID', 'Summary', 'Primary Tags', 'Secondary Tags', 'Link', 'Quotes', 'Media'])
        st.table(ideas_df)

        edit_idea_id = st.text_input('Enter the ID of the idea you want to edit')
        edit_button = st.button('Edit Idea')

        if edit_button:
            st.session_state['edit_idea_id'] = edit_idea_id
            st.experimental_rerun()

        delete_idea_id = st.text_input('Enter the ID of the idea you want to delete')
        delete_button = st.button('Delete Idea')

        if delete_button:
            conn.session.execute(f'DELETE FROM ideas WHERE id = {delete_idea_id}')
            conn.session.commit()
            st.experimental_rerun()

if __name__ == '__main__':
    app()
