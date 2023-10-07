# Generate a cover image for a poem using OpenAI LLM, LangChain and HuggingFace StableDiffusion Model
import io

import streamlit as st 
from constants.poem_generator import POEM_TYPES, POEM_STYLES

from utils.poem_generator import *
from utils.image_gen import generate_image

st.set_page_config(
    page_title="Poem Generator App",
    page_icon="✍"
)

openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", key="openai_api_key", type="password")
st.sidebar.markdown("[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)")

generate_cover_img = st.sidebar.checkbox("Generate Cover Image", value=True)

st.title("✍ Poem Generator App")
st.subheader("Write compelling poems with ease 🚀")

selected_poem_type = st.selectbox(
    "Select your preferred Poem type:",
    ("Standard", *tuple(map(lambda x: x["name"], POEM_TYPES)))
)

if selected_poem_type!="Standard":
    st.info(
        list(filter(lambda x: x["name"]==selected_poem_type, POEM_TYPES))[0]["description"],
        icon="ℹ"
    )

selected_poem_style = st.selectbox(
    "Select your preferred Poem style:",
    ("Standard", *tuple(POEM_STYLES))
)

poem_topic = st.text_input(
    "What is the poem topic? e.g. A poem about a bird in a cage",
    placeholder="Poem topic",
)

submit_btn = st.button("Generate ✍")

if submit_btn:
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key.", icon="⚠")
    else:
        poem_title = suggest_poem_title(
            poem_topic=poem_topic,
            poem_style=selected_poem_style,
            openai_api_key=openai_api_key
        )

        poem_content = generate_poem(
            poem_type=selected_poem_type,
            poem_topic=poem_topic,
            poem_style=selected_poem_style,
            openai_api_key=openai_api_key
        )

        st.divider()

        st.markdown(f"### **TITLE**: {poem_title}")
        st.write(poem_content)

        if generate_cover_img:
            huggingface_api_token = st.secrets[
                "HUGGINGFACE_API_TOKEN"
            ]
            if not huggingface_api_token:
                st.warning(
                    "Hugging Face API Token not set.", icon="⚠"
                )
            else:
                st.info(
                    "Here is a cover image generated for your poem",
                    icon="ℹ",
                )
                cover_image_bytes = generate_image(
                    query=poem_title,
                    api_key=huggingface_api_token,
                )
                st.image(io.BytesIO(cover_image_bytes))