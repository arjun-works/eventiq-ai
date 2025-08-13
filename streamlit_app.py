# This file tells Streamlit Cloud to use the correct entry point
import streamlit as st
from app.frontend.main import render_page

if __name__ == "__main__":
    render_page()
