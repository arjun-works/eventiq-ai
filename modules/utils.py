"""
Shared utilities and imports for EventIQ modules
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
import os
import base64
from PIL import Image
import io

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# File Upload Helper Functions
def save_uploaded_file(uploaded_file, folder="uploads"):
    """Save uploaded file and return file info"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return {
        "name": uploaded_file.name,
        "size": len(uploaded_file.getvalue()),
        "type": uploaded_file.type,
        "path": file_path
    }

def get_file_info(uploaded_file):
    """Get file information without saving"""
    return {
        "name": uploaded_file.name,
        "size": len(uploaded_file.getvalue()),
        "type": uploaded_file.type,
        "size_mb": len(uploaded_file.getvalue()) / (1024 * 1024)
    }

def display_image_preview(uploaded_file):
    """Display image preview with file info"""
    if uploaded_file.type.startswith('image/'):
        image = Image.open(uploaded_file)
        st.image(image, caption=f"📸 {uploaded_file.name}", width=200)
        
        # Display metadata
        st.markdown(f"""
        **📊 File Details:**
        - 📁 Name: {uploaded_file.name}
        - 📏 Size: {len(uploaded_file.getvalue()) / (1024 * 1024):.2f} MB
        - 🎨 Type: {uploaded_file.type}
        - 📐 Dimensions: {image.size[0]} x {image.size[1]} pixels
        """)
    else:
        st.info(f"📄 {uploaded_file.name} ({uploaded_file.type})")

def get_base64_encoded_file(uploaded_file):
    """Convert uploaded file to base64 encoding"""
    return base64.b64encode(uploaded_file.getvalue()).decode()

def make_api_request(endpoint, method="GET", data=None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_datetime(dt_string):
    """Format datetime string for display"""
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return dt_string

def show_success_animation():
    """Show success animation with balloons"""
    st.balloons()
    time.sleep(0.5)

def validate_file_upload(uploaded_file, max_size_mb=50, allowed_types=None):
    """Validate uploaded file"""
    if uploaded_file is None:
        return False, "No file selected"
    
    # Check file size
    file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File size ({file_size_mb:.1f} MB) exceeds maximum allowed size ({max_size_mb} MB)"
    
    # Check file type
    if allowed_types and uploaded_file.type not in allowed_types:
        return False, f"File type {uploaded_file.type} not allowed. Allowed types: {', '.join(allowed_types)}"
    
    return True, "File is valid"

# Common UI Components
def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Create a metric card"""
    st.metric(title, value, delta=delta, delta_color=delta_color)

def create_info_box(title, content, icon="ℹ️"):
    """Create an info box"""
    st.info(f"{icon} **{title}:** {content}")

def create_warning_box(title, content, icon="⚠️"):
    """Create a warning box"""
    st.warning(f"{icon} **{title}:** {content}")

def create_success_box(title, content, icon="✅"):
    """Create a success box"""
    st.success(f"{icon} **{title}:** {content}")

def create_error_box(title, content, icon="❌"):
    """Create an error box"""
    st.error(f"{icon} **{title}:** {content}")
