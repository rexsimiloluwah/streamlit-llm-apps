import streamlit as st 
from utils.qa import SimpleDocumentQA
from utils.loaders import extract_web_content

st.set_page_config(
    page_title="Web Page App",
    page_icon="🌎"
)

st.title("🌎 Web Page QA")
st.subheader("QA with content from a web page")

@st.cache_resource
def generate_qa_chain(url: str, openai_api_key: str):
    simple_doc_qa = SimpleDocumentQA(openai_api_key=openai_api_key)
    pages = extract_web_content(url)
    qa_chain = simple_doc_qa.load_qa_chain(pages)
    return qa_chain 

openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", key="openai_api_key", type="password")
st.sidebar.markdown("[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)")

use_example_url = st.checkbox("Use Example Web Page URL")

if not use_example_url:
    web_page_url_input = st.text_input("Enter URL to the web page")
    url = web_page_url_input 
else:
    url = "https://docs.streamlit.io/library/get-started/multipage-apps/create-a-multipage-app"

if url:
    st.info(f"You can now ask questions from the web page: {url}.", icon="🚀")
    query = st.text_area("Enter your query")

    submit_btn = st.button("Submit Query", key="submit_query")

    if submit_btn:
        if not openai_api_key:
            st.warning("Please enter your OpenAI API key to get started.", icon="⚠")
        else:
            qa_chain = generate_qa_chain(url, openai_api_key)
            result = qa_chain({"query": query})

            st.write(result["result"])

            if(result["source_documents"]):
                for i, source in enumerate(result["source_documents"]):
                    with st.expander(f"Source {i+1}"):
                        st.write(source.page_content)
else:
    st.info("Please enter the URL to the web page to get started.", icon="ℹ")




