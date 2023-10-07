import streamlit as st 
from streamlit_chat import message
from utils.chat import DocumentChat 
from utils.loaders import extract_pages 
from utils.helpers import read_example_document

st.set_page_config(
    page_title="Document Chat App",
    page_icon="📄"
)

@st.cache_resource
def generate_conv_qa_chain(file, openai_api_key: str):
    document_chat = DocumentChat(openai_api_key=openai_api_key)
    pages = extract_pages(file)
    conv_qa_chain = document_chat.load_conv_qa_chain(pages)
    return conv_qa_chain

st.title("📃 Document Chat")
st.subheader("Chat with your PDF document")

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

    if not openai_api_key:
        st.warning("Please enter your OpenAI API key to get started.", icon="⚠")
    else:
        conv_qa_chain = generate_conv_qa_chain(file, openai_api_key)

        if "generated" not in st.session_state:
            st.session_state["generated"] = []

        if "past" not in st.session_state:
            st.session_state["past"] = []

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        input_text = st.chat_input("Enter your message")

        if input_text:
            result = conv_qa_chain({
                "question": input_text,
                "chat_history": st.session_state.chat_history
            })

            st.session_state.past.append(input_text)
            st.session_state.generated.append(result["answer"])
            st.session_state.chat_history.extend([(input_text, result["answer"])])

        if st.session_state.chat_history:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
else:
    st.info("Please upload your PDF file to get started.", icon="ℹ")