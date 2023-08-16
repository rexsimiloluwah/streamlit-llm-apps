import streamlit as st 
from .utils.qa import SimpleDocumentQA
from .utils.loaders import extract_web_content

def web_page_qa_page():
    simple_doc_qa = SimpleDocumentQA()

    st.title("🌎 Web Page QA")
    st.write("QA with content from a web page")

    web_page_url_input = st.text_input("Enter URL to the web page")

    @st.cache_resource
    def generate_qa_chain(url):
        pages = extract_web_content(url)

        qa_chain = simple_doc_qa.load_qa_chain(pages)

        return qa_chain 
    

    if web_page_url_input:
        qa_chain = generate_qa_chain(web_page_url_input)

        query = st.text_area("Enter your query")

        if st.button("Submit Query", key="submit_query"):
            result = qa_chain({"query": query})

            st.write(result["result"])

            if(result["source_documents"]):
                for i, source in enumerate(result["source_documents"]):
                    with st.expander(f"Source {i+1}"):
                        st.write(source.page_content)




