import os

import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter

st.title("Langchain Text Summarizer")


from config import CONFIG

openai_api_key = CONFIG.get("openai_api_key")

source_text = st.text_area("Source Text", height=200)

if st.button("Summarize"):
    try:
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(source_text)

        docs = [Document(page_content=t) for t in texts[:3]]

        llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(docs)

        st.write(summary)
    except Exception as e:
        st.write(f"An error occurred: {e}")
