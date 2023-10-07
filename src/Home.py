import streamlit as st

def main():
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

    st.markdown("""
    # Hi there 👋
                
    This is is Streamlit application which contains a suite of useful apps powered by LLMs. 
    These apps combine cutting-edge technologies like text generation via LLMs, retrieval augmented generation (RAG), image generation, 
    audio transcription etc.
    
    This suite currently includes the following apps:
    
    - **Document Chat App** - for chatting with your PDF documents
    - **Simple Document QA App** - for performing QA on your PDF documents
    - **Web Page QA** - for performing QA on content from web pages
                
    These apps were birthed from simple experiments to apply LLMs to real-world problems, I genuinely hope they are useful for you 💗!
""")
    

if __name__ == "__main__":
    main()