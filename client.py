import streamlit as st 
from module import stuff_document_summarization
import os 

st.title('Summarize your Document')

if 'count' not in st.session_state : 
    st.session_state.count = 0

uploaded_file = st.file_uploader('Upload document', type=['pdf'])

if uploaded_file : 
    if st.session_state['count'] >= 3 : 
        st.warning("You've reached the summarization limit")
    else : 
        if not os.path.exists('data/') : 
            os.makedirs('data/', exist_ok=True)
        temp_data_path = os.path.join('data/', uploaded_file.name)
        with open(temp_data_path, 'wb') as f : 
            f.write(uploaded_file.read())

        summarization = stuff_document_summarization(temp_data_path)
        if summarization : 
            st.write(summarization)
            st.session_state['count'] += 1 
            os.remove(temp_data_path)


    

