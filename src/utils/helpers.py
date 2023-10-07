import io
import os
import glob
import random

import streamlit as st

@st.cache_data
def read_example_document() -> None:
    """Read a random document from the 'examples' folder."""
    EXAMPLES_DIR = "./examples/documents"

    # Get a random document
    documents_list = glob.glob(f"{EXAMPLES_DIR}/*.pdf")
    rand_idx = random.randint(0, len(documents_list))

    file_path = documents_list[rand_idx]
    filename = os.path.basename(file_path)

    with open(file_path, "rb") as file:
        file_bytes = file.read()

    # Create a BytesIO object from the file bytes
    file_obj = io.BytesIO(file_bytes)
    return file_obj, filename