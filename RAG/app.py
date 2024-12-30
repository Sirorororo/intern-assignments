import streamlit as st
import cohere
from data_ingestion import create_chunks
import embeddings as emd
from prompt_eng import build_prompt,generate_response
from constants import COHERE_API_KEY


def main():
    co = cohere.Client(COHERE_API_KEY)
    model = emd.load_model('BAAI/bge-small-en-v1.5')
    st.title("Chat With Docs")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        print("here")
        if 'df' not in st.session_state:
            # Create chunks of the file
            chunks = create_chunks(uploaded_file)
            df = emd.create_df(chunks,model)
            st.session_state.df = df
    
    search_query = st.text_input("Enter a word or phrase to search")

    if st.button("Search"):
        print(search_query)
        embedded_query = model.encode(search_query)
        top_k = emd.calculate_cosine_similarity(st.session_state.df,embedded_query)
        prompt = build_prompt(search_query,top_k)
        st.write(generate_response(co,prompt))
    
    if st.sidebar.button('Reset PDF'):
        if 'df' in st.session_state:
            del st.session_state['df']  # Remove the stored dataframe        
        st.sidebar.write("PDF reset successfully!")

if __name__ == "__main__":
    main()