import streamlit as st
from .utils.qa import SimpleDocumentQA
from .utils.loaders import extract_pages

def simple_document_qa_page():
    simple_doc_qa = SimpleDocumentQA()

    st.title("📃 Simple Document QA")
    st.write("QA with your PDF document")
    st.header("Please upload your PDF file below")

    file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="pdf file to be parsed",
    )

    @st.cache_resource
    def generate_qa_chain(file):
        pages = extract_pages(file)

        qa_chain = simple_doc_qa.load_qa_chain(pages)

        return qa_chain 
    

    if file is not None:
        st.success("File uploaded successfully", icon="✅")

        qa_chain = generate_qa_chain(file)

        query = st.text_area("Enter your query")

        if st.button("Submit Query", key="submit_query"):
            result = qa_chain({"query": query})

            st.write(result["result"])

            if(result["source_documents"]):
                for i, source in enumerate(result["source_documents"]):
                    with st.expander(f"Source {i+1}"):
                        st.write(source.page_content)