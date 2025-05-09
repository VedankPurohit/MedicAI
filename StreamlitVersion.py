import streamlit as st
import sys

# Displaying the title
st.title("Python Version Checker")

# Fetching and displaying the Python version
python_version = sys.version
st.write(f"Python Version: {python_version}")
