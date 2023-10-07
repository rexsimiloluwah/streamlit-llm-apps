from typing import List 

import streamlit as st
from PyPDF2 import PdfReader 
from langchain.schema.document import Document 
from langchain.document_loaders import WebBaseLoader

@st.cache_data
def extract_pages(file) -> List[Document]:
    """Extracts the pages from a PDF document"""
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)

    pages = []

    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        pages.append(
            Document(
                page_content=text,
                metadata={
                    "source": file.name if type(file) == st.runtime.uploaded_file_manager.UploadedFile else "",
                    "page": i
                }
        ))
    
    return pages

@st.cache_data
def extract_web_content(url: str) -> List[Document]:
    """Extracts content from a web page"""
    loader = WebBaseLoader(url)
    docs = loader.load()

    return docs