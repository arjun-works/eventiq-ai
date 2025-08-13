"""
Media Gallery Module for EventIQ Management System
Team Member: [Media Management Team]
"""

from .utils import *

def show_media_gallery_page():
    """Enhanced media gallery and upload page"""
    st.markdown("## 📸 Media Gallery & Upload")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Gallery", "📤 Upload", "📊 Statistics", "🎥 Live Stream"])
    
    with tab1:
        show_media_gallery()
    
    with tab2:
        show_media_upload()
    
    with tab3:
        show_media_statistics()
    
    with tab4:
        show_live_stream_management()

def show_media_gallery():
    """Display media gallery"""
    st.markdown("### 📸 Event Photo Gallery")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_date = st.date_input("Filter by Date:")
    with col2:
        filter_booth = st.selectbox("Filter by Location:", ["All", "Main Entrance", "Information Booth", "Main Stage", "Food Court", "Exhibition Hall"])
    with col3:
        filter_type = st.selectbox("Media Type:", ["All", "Photos", "Videos", "Documents"])
    
    # Get combined media (sample + uploaded)
    all_media = get_combined_media()
    
    # Apply filters
    filtered_media = apply_media_filters(all_media, filter_booth, filter_type)
    
    # Display media statistics
    show_gallery_overview(all_media)
    
    # Display media in grid
    show_media_grid(filtered_media)

def show_media_upload():
    """Media upload interface"""
    st.markdown("### 📤 Upload New Media")
    
    col1, col2 = st.columns(2)
    with col1:
        show_upload_interface()
    
    with col2:
        show_upload_metadata_form()

def show_media_statistics():
    """Display media analytics"""
    st.markdown("### 📊 Media Statistics & Analytics")
    
    # Key metrics
    show_media_metrics()
    
    # Charts
    show_media_charts()
    
    # Top contributors
    show_top_contributors()
    
    # Storage breakdown
    show_storage_breakdown()

def show_live_stream_management():
    """Live stream management interface"""
    st.markdown("### 🎥 Live Stream Management")
    
    col1, col2 = st.columns(2)
    with col1:
        show_active_streams()
    
    with col2:
        show_stream_controls()
    
    show_stream_settings()
    show_chat_moderation()

def get_sample_media():
    """Get sample media data"""
    return [
        {
            "name": "Registration Desk Setup",
            "type": "Photo",
            "booth": "Main Entrance",
            "date": "2025-01-30",
            "photographer": "John Smith",
            "size": "2.4 MB",
            "downloads": 15,
            "likes": 8,
            "tags": ["registration", "setup", "entrance"],
            "source": "sample"
        },
        {
            "name": "Information Booth Team",
            "type": "Photo",
            "booth": "Information Booth",
            "date": "2025-01-30",
            "photographer": "Sarah Johnson",
            "size": "3.1 MB",
            "downloads": 23,
            "likes": 12,
            "tags": ["team", "volunteers", "information"],
            "source": "sample"
        },
        {
            "name": "Main Stage Performance",
            "type": "Video",
            "booth": "Main Stage",
            "date": "2025-01-29",
            "photographer": "Mike Wilson",
            "size": "45.2 MB",
            "downloads": 8,
            "likes": 25,
            "tags": ["performance", "stage", "entertainment"],
            "source": "sample"
        },
        {
            "name": "Volunteer Training Session",
            "type": "Photo",
            "booth": "Conference Room",
            "date": "2025-01-29",
            "photographer": "Alice Brown",
            "size": "1.8 MB",
            "downloads": 12,
            "likes": 6,
            "tags": ["training", "volunteers", "preparation"],
            "source": "sample"
        },
        {
            "name": "Food Court Opening",
            "type": "Photo",
            "booth": "Food Court",
            "date": "2025-01-30",
            "photographer": "David Lee",
            "size": "2.7 MB",
            "downloads": 18,
            "likes": 14,
            "tags": ["food", "opening", "vendors"],
            "source": "sample"
        },
        {
            "name": "Exhibition Hall Overview",
            "type": "Video",
            "booth": "Exhibition Hall",
            "date": "2025-01-30",
            "photographer": "Emma Davis",
            "size": "38.5 MB",
            "downloads": 6,
            "likes": 9,
            "tags": ["exhibition", "overview", "booths"],
            "source": "sample"
        }
    ]

def get_combined_media():
    """Combine sample media with uploaded media"""
    # Initialize session state for uploaded media
    if 'uploaded_media' not in st.session_state:
        st.session_state.uploaded_media = []
    
    sample_media = get_sample_media()
    all_media = sample_media.copy()
    
    # Add uploaded media from session state
    if st.session_state.uploaded_media:
        for uploaded in st.session_state.uploaded_media:
            media_item = {
                "name": uploaded['name'],
                "type": uploaded['type'],
                "booth": uploaded.get('location', 'Unknown'),
                "date": uploaded['date'],
                "photographer": uploaded.get('photographer', 'Unknown'),
                "size": uploaded['size'],
                "downloads": 0,
                "likes": 0,
                "tags": uploaded.get('tags', []),
                "source": "uploaded",
                "description": uploaded.get('description', ''),
                "category": uploaded.get('category', 'General')
            }
            all_media.append(media_item)
    
    return all_media

def apply_media_filters(media_list, filter_booth, filter_type):
    """Apply filters to media list"""
    filtered_media = media_list
    if filter_booth != "All":
        filtered_media = [m for m in filtered_media if m['booth'] == filter_booth]
    if filter_type != "All":
        filtered_media = [m for m in filtered_media if m['type'] == filter_type]
    return filtered_media

def show_gallery_overview(all_media):
    """Display gallery overview metrics"""
    st.markdown("#### 📊 Gallery Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📸 Total Media", len(all_media))
    with col2:
        photos = len([m for m in all_media if m['type'] == 'Photo'])
        st.metric("📷 Photos", photos)
    with col3:
        videos = len([m for m in all_media if m['type'] == 'Video'])
        st.metric("🎥 Videos", videos)
    with col4:
        uploaded = len([m for m in all_media if m.get('source') == 'uploaded'])
        st.metric("📤 Uploaded", uploaded)

def show_media_grid(filtered_media):
    """Display media in grid format"""
    st.markdown("#### 🖼️ Media Gallery")
    for i in range(0, len(filtered_media), 2):
        col1, col2 = st.columns(2)
        
        for j, col in enumerate([col1, col2]):
            if i + j < len(filtered_media):
                media = filtered_media[i + j]
                with col:
                    display_media_card(media, i + j)

def display_media_card(media, index):
    """Display individual media card"""
    with st.container():
        # Different styling for uploaded vs sample media
        border_color = "#4CAF50" if media.get('source') == 'uploaded' else "#ddd"
        source_badge = "🆕 NEW" if media.get('source') == 'uploaded' else "📋 SAMPLE"
        
        st.markdown(f"""
        <div style="border: 2px solid {border_color}; border-radius: 8px; padding: 15px; margin: 10px 0; background: white;">
            <h4>📸 {media['name']} <span style="background: {border_color}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;">{source_badge}</span></h4>
            <p><strong>Type:</strong> {media['type']} | <strong>Size:</strong> {media['size']}</p>
            <p><strong>Location:</strong> {media['booth']}</p>
            <p><strong>Date:</strong> {media['date']}</p>
            <p><strong>Photographer:</strong> {media['photographer']}</p>
            <p><strong>Tags:</strong> {', '.join(media['tags']) if isinstance(media['tags'], list) else media['tags']}</p>
            <p>👁️ {media['downloads']} downloads | ❤️ {media['likes']} likes</p>
            {f"<p><strong>Description:</strong> {media.get('description', '')}</p>" if media.get('description') else ""}
        </div>
        """, unsafe_allow_html=True)
        
        show_media_actions(media, index)

def show_media_actions(media, index):
    """Display media action buttons"""
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button(f"👁️ View", key=f"view_{index}"):
            if media.get('source') == 'uploaded':
                st.success(f"Viewing uploaded file: {media['name']}")
            else:
                st.success(f"Viewing {media['name']}")
    with col_b:
        if st.button(f"📥 Download", key=f"download_{index}"):
            st.success(f"Downloading {media['name']}")
            # Increment download count
            media['downloads'] += 1
    with col_c:
        if st.button(f"❤️ Like", key=f"like_{index}"):
            st.success(f"Liked {media['name']}")
            # Increment like count
            media['likes'] += 1

def show_upload_interface():
    """Show file upload interface"""
    st.markdown("#### 📷 Media Upload")
    uploaded_files = st.file_uploader(
        "Choose media files", 
        type=['jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov', 'pdf', 'doc', 'docx'], 
        accept_multiple_files=True,
        key="media_uploader"
    )
    
    if uploaded_files:
        st.success(f"Selected {len(uploaded_files)} file(s)")
        display_uploaded_files_preview(uploaded_files)
    
    show_sample_file_buttons()

def display_uploaded_files_preview(uploaded_files):
    """Display preview of uploaded files"""
    for idx, file in enumerate(uploaded_files):
        file_info = get_file_info(file)
        
        with st.expander(f"📄 {file_info['name']} ({file_info['size_mb']:.2f} MB)", expanded=True):
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                display_image_preview(file)
            
            with col_b:
                st.write(f"**File Type:** {file_info['type']}")
                st.write(f"**Size:** {file_info['size_mb']:.2f} MB")
                
                # File-specific metadata
                if file_info['type'].startswith('image/'):
                    try:
                        image = Image.open(file)
                        st.write(f"**Dimensions:** {image.size[0]} x {image.size[1]} pixels")
                    except Exception:
                        pass
                elif file_info['type'].startswith('video/'):
                    st.write("**Type:** Video File")
                elif 'pdf' in file_info['type']:
                    st.write("**Type:** PDF Document")

def show_sample_file_buttons():
    """Show sample file loading buttons"""
    st.markdown("#### 📁 Sample Files")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📷 Load Sample Images", use_container_width=True):
            load_sample_images()
    
    with col2:
        if st.button("🎥 Load Sample Videos", use_container_width=True):
            load_sample_videos()

def load_sample_images():
    """Load sample images"""
    sample_images = [
        {"name": "event_entrance.jpg", "type": "image/jpeg", "size": 2.4},
        {"name": "registration_desk.jpg", "type": "image/jpeg", "size": 1.8},
        {"name": "main_stage.jpg", "type": "image/jpeg", "size": 3.2}
    ]
    for img in sample_images:
        st.session_state.uploaded_media.append({
            "name": img["name"],
            "type": "Photo",
            "size": f"{img['size']} MB",
            "location": "Sample Location",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Uploaded"
        })
    st.success("✅ Sample images loaded!")

def load_sample_videos():
    """Load sample videos"""
    sample_videos = [
        {"name": "opening_ceremony.mp4", "type": "video/mp4", "size": 45.2},
        {"name": "workshop_session.mp4", "type": "video/mp4", "size": 38.5}
    ]
    for vid in sample_videos:
        st.session_state.uploaded_media.append({
            "name": vid["name"],
            "type": "Video",
            "size": f"{vid['size']} MB",
            "location": "Sample Location",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Uploaded"
        })
    st.success("✅ Sample videos loaded!")

def show_upload_metadata_form():
    """Show metadata form for uploads"""
    st.markdown("#### 📝 Media Details")
    
    # Basic metadata
    booth_location = st.selectbox("Location:", [
        "Main Entrance", "Information Booth", "Main Stage", "Registration", 
        "Food Court", "Exhibition Hall", "Conference Room", "Networking Area"
    ])
    event_category = st.selectbox("Event Category:", [
        "Setup", "Registration", "Presentations", "Networking", 
        "Entertainment", "Workshops", "Closing", "Behind the Scenes"
    ])
    photographer = st.text_input("Photographer/Creator:")
    description = st.text_area("Description:")
    tags = st.text_input("Tags (comma-separated):")
    
    # Advanced options
    st.markdown("#### ⚙️ Advanced Options")
    make_public = st.checkbox("Make publicly visible", value=True)
    allow_downloads = st.checkbox("Allow downloads", value=True)
    require_attribution = st.checkbox("Require attribution", value=False)
    
    # Save button
    show_save_media_button(booth_location, event_category, photographer, description, tags, make_public, allow_downloads, require_attribution)

def show_save_media_button(booth_location, event_category, photographer, description, tags, make_public, allow_downloads, require_attribution):
    """Show save media button and handle saving"""
    if st.button("💾 Save Media", use_container_width=True):
        uploaded_files = st.session_state.get('media_uploader', [])
        if uploaded_files:
            process_uploaded_files(uploaded_files, booth_location, event_category, photographer, description, tags, make_public, allow_downloads, require_attribution)
        else:
            st.warning("⚠️ Please select files to upload first")

def process_uploaded_files(uploaded_files, booth_location, event_category, photographer, description, tags, make_public, allow_downloads, require_attribution):
    """Process and save uploaded files"""
    for file in uploaded_files:
        file_info = get_file_info(file)
        
        # Save file information to session state
        media_entry = {
            "name": file_info['name'],
            "type": "Photo" if file_info['type'].startswith('image/') else "Video" if file_info['type'].startswith('video/') else "Document",
            "size": f"{file_info['size_mb']:.2f} MB",
            "location": booth_location,
            "category": event_category,
            "photographer": photographer,
            "description": description,
            "tags": tags.split(',') if tags else [],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Uploaded",
            "public": make_public,
            "downloads_allowed": allow_downloads,
            "attribution_required": require_attribution,
            "file_data": get_base64_encoded_file(file)  # Store file data
        }
        
        st.session_state.uploaded_media.append(media_entry)
    
    st.success(f"✅ Successfully uploaded {len(uploaded_files)} file(s)!")
    show_success_animation()
    
    # Show uploaded files summary
    st.markdown("#### 📋 Upload Summary")
    for file in uploaded_files:
        st.info(f"✅ {file.name} - Saved to {booth_location}")
    
    # Display upload status
    if st.session_state.uploaded_media:
        st.markdown("#### 📊 Upload Status")
        st.metric("Total Uploaded Files", len(st.session_state.uploaded_media))
        
        if st.button("📋 View All Uploads"):
            st.markdown("##### 📁 Your Uploaded Files:")
            for idx, media in enumerate(st.session_state.uploaded_media):
                st.write(f"{idx+1}. {media['name']} - {media['type']} ({media['size']})")

def show_media_metrics():
    """Display media metrics"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📸 Total Media", "24")
    with col2:
        st.metric("👥 Contributors", "8")
    with col3:
        st.metric("📥 Total Downloads", "156")
    with col4:
        st.metric("💾 Storage Used", "2.3 GB")

def show_media_charts():
    """Display media analytics charts"""
    col1, col2 = st.columns(2)
    with col1:
        # Media type distribution
        media_types = {"Photos": 18, "Videos": 4, "Documents": 2}
        fig = px.pie(values=list(media_types.values()), names=list(media_types.keys()),
                    title="Media Type Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Upload activity over time
        dates = ["2025-01-28", "2025-01-29", "2025-01-30", "2025-01-31"]
        uploads = [3, 8, 10, 3]
        fig = px.bar(x=dates, y=uploads, title="Daily Upload Activity")
        st.plotly_chart(fig, use_container_width=True)

def show_top_contributors():
    """Display top contributors table"""
    st.markdown("#### 🏆 Top Contributors")
    contributors = [
        {"Name": "Sarah Johnson", "Uploads": 8, "Downloads": 45, "Likes": 32},
        {"Name": "Mike Wilson", "Uploads": 6, "Downloads": 38, "Likes": 28},
        {"Name": "Alice Brown", "Uploads": 4, "Downloads": 22, "Likes": 15},
        {"Name": "John Smith", "Uploads": 3, "Downloads": 28, "Likes": 18},
        {"Name": "David Lee", "Uploads": 2, "Downloads": 15, "Likes": 12},
    ]
    
    contrib_df = pd.DataFrame(contributors)
    st.dataframe(contrib_df, use_container_width=True, hide_index=True)

def show_storage_breakdown():
    """Display storage usage breakdown"""
    st.markdown("#### 💾 Storage Breakdown")
    storage_data = {
        "Photos": 1.8,
        "Videos": 0.4,
        "Documents": 0.1
    }
    
    fig = px.bar(x=list(storage_data.keys()), y=list(storage_data.values()),
                title="Storage Usage by Type (GB)")
    st.plotly_chart(fig, use_container_width=True)

def show_active_streams():
    """Display active streams"""
    st.markdown("#### 📡 Active Streams")
    streams = [
        {"Location": "Main Stage", "Status": "🔴 Live", "Viewers": 142, "Duration": "2h 15m"},
        {"Location": "Workshop Room A", "Status": "🔴 Live", "Viewers": 67, "Duration": "1h 45m"},
        {"Location": "Exhibition Hall", "Status": "⏸️ Paused", "Viewers": 0, "Duration": "0h 30m"},
    ]
    
    for stream in streams:
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin: 5px 0;">
            <h4>📹 {stream['Location']}</h4>
            <p><strong>Status:</strong> {stream['Status']}</p>
            <p><strong>Viewers:</strong> {stream['Viewers']}</p>
            <p><strong>Duration:</strong> {stream['Duration']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_stream_controls():
    """Display stream control interface"""
    st.markdown("#### 🎮 Stream Controls")
    selected_location = st.selectbox("Select Stream:", ["Main Stage", "Workshop Room A", "Exhibition Hall"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶️ Start Stream", use_container_width=True):
            st.success(f"Started stream for {selected_location}")
    with col_b:
        if st.button("⏹️ Stop Stream", use_container_width=True):
            st.success(f"Stopped stream for {selected_location}")
    
    col_c, col_d = st.columns(2)
    with col_c:
        if st.button("⏸️ Pause Stream", use_container_width=True):
            st.success(f"Paused stream for {selected_location}")
    with col_d:
        if st.button("📹 Record", use_container_width=True):
            st.success(f"Recording started for {selected_location}")

def show_stream_settings():
    """Display stream settings"""
    st.markdown("#### ⚙️ Stream Settings")
    col1, col2, col3 = st.columns(3)
    with col1:
        quality = st.selectbox("Video Quality:", ["720p", "1080p", "4K"])
    with col2:
        bitrate = st.slider("Bitrate (kbps):", 500, 5000, 2000)
    with col3:
        fps = st.selectbox("Frame Rate:", ["24 fps", "30 fps", "60 fps"])

def show_chat_moderation():
    """Display chat moderation interface"""
    st.markdown("#### 💬 Live Chat Moderation")
    chat_messages = [
        {"User": "participant123", "Message": "Great presentation!", "Time": "14:35"},
        {"User": "volunteer_sarah", "Message": "Thanks for joining everyone!", "Time": "14:34"},
        {"User": "organizer_mike", "Message": "Next session starts in 10 minutes", "Time": "14:33"},
    ]
    
    for msg in chat_messages:
        col1, col2, col3, col4 = st.columns([2, 4, 1, 1])
        with col1:
            st.write(f"**{msg['User']}**")
        with col2:
            st.write(msg['Message'])
        with col3:
            st.write(msg['Time'])
        with col4:
            if st.button("🗑️", key=f"delete_{msg['Time']}"):
                st.success("Message deleted")
