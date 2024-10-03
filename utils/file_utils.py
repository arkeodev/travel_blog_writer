import logging
import os
import tempfile
from pathlib import Path

import streamlit as st


def save_uploaded_file(uploaded_file):
    """Saves an uploaded file to a temporary directory and returns the path."""
    if not uploaded_file:
        raise ValueError("No file uploaded")

    try:
        if "temp_dir" not in st.session_state:
            st.session_state.temp_dir = tempfile.mkdtemp()

        file_path = Path(st.session_state.temp_dir) / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        return file_path
    except Exception as e:
        logging.error(f"Failed to save uploaded file: {str(e)}")
        raise
