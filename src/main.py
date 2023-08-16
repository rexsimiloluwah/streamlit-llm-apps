import os
import openai
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from apps.home import home_page
from apps.simple_document_qa import simple_document_qa_page
from apps.document_chat import document_chat_page
from apps.web_page_qa import web_page_qa_page

_ = load_dotenv(find_dotenv())

openai.api_key = os.environ["OPENAI_API_KEY"]

st.markdown("""
    <style> 
        div.stButton > button:first-child { 
            background-color: rgb(204, 49, 49);
            color: white;
        }

        div.stButton > button:first-child:hover{
            background-color: white;
            color: rgb(204, 49, 49);
            border: 2px solid rgb(204, 49, 49);
        } 
    </style>""", unsafe_allow_html=True)


def main():
    st.sidebar.title("Navigation")
    page_options = ["Home", "Simple Document QA", "Document Chat","Web Page QA"]
    selected_page = st.sidebar.radio("Select a page", page_options)

    if selected_page == page_options[0]:
        home_page()
    elif selected_page == page_options[1]:
        simple_document_qa_page()
    elif selected_page == page_options[2]:
        document_chat_page()
    elif selected_page == page_options[3]:
        web_page_qa_page()

if __name__ == "__main__":
    main()