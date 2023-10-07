import streamlit as st
from utils.qa import SimpleDocumentQA
from utils.loaders import extract_pages
from utils.helpers import read_example_document

st.set_page_config(
    page_title="Simple Document Chat App",
    page_icon="📃"
)

st.title("📃 Simple Document QA")
st.subheader("QA with your PDF document")

@st.cache_resource
def generate_qa_chain(file, openai_api_key: str):
    simple_doc_qa = SimpleDocumentQA(openai_api_key=openai_api_key)
    pages = extract_pages(file)
    qa_chain = simple_doc_qa.load_qa_chain(pages)
    return qa_chain 

openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", key="openai_api_key", type="password")
st.sidebar.markdown("[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)")

use_example_document = st.checkbox("Use Example Document")

if use_example_document:
    file, filename = read_example_document() 
else:
    file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="pdf file to be parsed",
    )

if file is not None:
    if type(file) != st.runtime.uploaded_file_manager.UploadedFile:
        st.info(f"Using file: {filename}", icon="ℹ")
    else:
        st.success("File uploaded successfully", icon="✅")
    query = st.text_area("Enter your query")
    submit_btn = st.button("Submit Query", key="submit_query")

    if submit_btn:
        if not openai_api_key:
            st.warning("Please enter your OpenAI API key to get started.", icon="⚠")
        else:
            qa_chain = generate_qa_chain(file, openai_api_key)
            result = qa_chain({"query": query})
            st.write(result["result"])

            if(result["source_documents"]):
                for i, source in enumerate(result["source_documents"]):
                    with st.expander(f"Source {i+1}"):
                        st.write(source.page_content)
else:
    st.info("Please upload your PDF file to get started.", icon="ℹ")