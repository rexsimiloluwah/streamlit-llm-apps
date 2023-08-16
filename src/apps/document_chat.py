import streamlit as st 
from streamlit_chat import message
from .utils.chat import DocumentChat 
from .utils.loaders import extract_pages 

def document_chat_page():
    document_chat = DocumentChat()
    st.title("📃 Document Chat")
    st.write("Chat with your PDF document")

    file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="pdf file to be parsed",
    )

    @st.cache_resource
    def generate_conv_qa_chain(file):
        pages = extract_pages(file)
        conv_qa_chain = document_chat.load_conv_qa_chain(pages)
        return conv_qa_chain


    if file is not None:
        st.success("File uploaded successfully", icon="✅")

        conv_qa_chain = generate_conv_qa_chain(file)

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