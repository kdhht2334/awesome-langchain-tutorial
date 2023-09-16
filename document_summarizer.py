import os
import streamlit as st

from module import config
from llama_index import SimpleDirectoryReader, VectorStoreIndex

CONFIG = config.CONFIG

openai_api_key = CONFIG.get("openai_api_key")
os.environ["OPENAI_API_KEY"] = openai_api_key

st.title("Langchain Text Summarizer")

text_query = st.text_area("Your query", height=200)

if st.button("Summarize"):
    try:
        documents = SimpleDirectoryReader("resources").load_data()
        index = VectorStoreIndex.from_documents(documents=documents)

        query_engine = index.as_query_engine()
        answer = query_engine.query(text_query)

        st.write(answer.response)
    except Exception as e:
        st.write(f"An error occurred: {e}")
