import streamlit as st
from utils import extract_text_from_pdf, summarize_text
from streamlit_extras.stylable_container import stylable_container

def show():
    # Premium header with gradient and icon
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 1px solid #e2e8f0;">
        <div style="background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 15px; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);">
            <span style="font-size: 24px;">📄</span>
        </div>
        <div>
            <h1 style="margin: 0; padding: 0; font-size: 2.2rem; font-weight: 700; background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-fill-color: transparent;">PDF Summarizer</h1>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 1.1rem;">Extract and summarize content from PDF documents</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main content in a premium card container with subtle gradient
    with stylable_container(
        key="pdf_upload_container",
        css_styles="""{
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            padding: 30px;
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            margin-bottom: 30px;
        }"""
    ):
        # File upload section with premium styling
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); width: 28px; height: 28px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                <span style="color: white; font-size: 14px;">📄</span>
            </div>
            <p style="margin: 0; font-weight: 600; color: #334155; font-size: 1.1rem;">Upload your PDF document</p>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced file uploader
        uploaded_file = st.file_uploader(
            "Upload a PDF file",
            type=["pdf"],
            help="Upload a PDF document to extract and summarize its content",
            label_visibility="collapsed"
        )

    # Process the uploaded file
    if uploaded_file is not None:
        # Display file details in a premium container
        with stylable_container(
            key="file_details_container",
            css_styles="""{
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                padding: 20px;
                background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
                animation: fadeIn 0.5s ease-out forwards;
            }"""
        ):
            st.markdown(f"""
            <div style="display: flex; align-items: center;">
                <div style="background: linear-gradient(90deg, #0369a1 0%, #0ea5e9 100%); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                    <span style="color: white; font-size: 20px;">📂</span>
                </div>
                <div>
                    <p style="margin: 0; font-weight: 600; color: #0c4a6e; font-size: 1.1rem;">{uploaded_file.name}</p>
                    <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">{uploaded_file.size / 1024:.2f} KB</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Extract text from PDF with premium styling
        with st.spinner():
            st.markdown("""
            <div style="display: flex; justify-content: center; margin: 30px 0;">
                <div style="display: flex; align-items: center; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); padding: 15px 25px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1);">
                    <div style="width: 24px; height: 24px; border-radius: 50%; border: 3px solid #3b82f6; border-top-color: transparent; margin-right: 12px; animation: spin 1s linear infinite;"></div>
                    <p style="margin: 0; color: #1e40af; font-weight: 500;">Extracting text from PDF...</p>
                </div>
            </div>
            <style>
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            </style>
            """, unsafe_allow_html=True)

            pdf_text = extract_text_from_pdf(uploaded_file)

            # Clear the spinner
            st.empty()

            if pdf_text:
                # Show text extraction success with premium styling
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1), 0 2px 4px -1px rgba(16, 185, 129, 0.06);">
                    <div style="display: flex; align-items: center;">
                        <div style="background: linear-gradient(90deg, #059669 0%, #10b981 100%); width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                            <span style="color: white; font-size: 14px;">✓</span>
                        </div>
                        <p style="margin: 0; color: #065f46; font-weight: 600; font-size: 1rem;">Text extracted successfully!</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Text preview with premium styling
                with stylable_container(
                    key="text_preview_container",
                    css_styles="""{
                        border-radius: 12px;
                        border: 1px solid #e2e8f0;
                        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
                        margin: 20px 0;
                        overflow: hidden;
                    }"""
                ):
                    st.markdown("""
                    <div style="padding: 20px 25px; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; cursor: pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none';">
                        <div style="background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                            <span style="color: white; font-size: 14px;">🔍</span>
                        </div>
                        <h3 style="margin: 0; font-size: 1.2rem; font-weight: 600; color: #1e40af;">Preview extracted text</h3>
                    </div>
                    <div style="padding: 25px; background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);">
                    """, unsafe_allow_html=True)

                    # Ensure text area has proper styling
                    st.markdown("""
                    <style>
                    /* Ensure text area has proper styling */
                    .stTextArea textarea {
                        background-color: #f8fafc !important;
                        width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    div[data-baseweb="textarea"] {
                        background-color: #f8fafc !important;
                        width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    div[data-baseweb="textarea"] > div {
                        background-color: #f8fafc !important;
                        width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    .stTextArea > div {
                        width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    # Container to ensure text area fits properly
                    with st.container():
                        # Text area for extracted text
                        st.text_area(
                            "Extracted text",
                            pdf_text,
                            height=200,
                            label_visibility="collapsed"
                        )

                    st.markdown("</div>", unsafe_allow_html=True)

                # Summary options with premium styling
                with stylable_container(
                    key="summary_options_container",
                    css_styles="""{
                        border-radius: 16px;
                        border: 1px solid #e2e8f0;
                        padding: 25px;
                        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
                        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
                        margin: 30px 0 20px 0;
                    }"""
                ):
                    st.markdown("""
                    <div style="display: flex; align-items: center; margin-bottom: 20px;">
                        <div style="background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); width: 28px; height: 28px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                            <span style="color: white; font-size: 14px;">⚙️</span>
                        </div>
                        <p style="margin: 0; font-weight: 600; color: #334155; font-size: 1.1rem;">Summary Options</p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, _ = st.columns(2)
                    with col1:
                        st.markdown("""
                        <p style="margin: 0 0 10px 0; font-weight: 500; color: #334155; font-size: 0.95rem;">Summary Length</p>
                        """, unsafe_allow_html=True)

                        summary_length = st.radio(
                            "Summary length",
                            options=["short", "medium", "long"],
                            index=1,
                            horizontal=True,
                            label_visibility="collapsed"
                        )

                    # Generate summary button with premium styling
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    generate_btn = st.button(
                        "✨ Generate Summary",
                        use_container_width=True,
                        type="primary"
                    )

                # Generate summary
                if generate_btn:
                    with st.spinner():
                        st.markdown("""
                        <div style="display: flex; justify-content: center; margin: 30px 0;">
                            <div style="display: flex; align-items: center; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); padding: 15px 25px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1);">
                                <div style="width: 24px; height: 24px; border-radius: 50%; border: 3px solid #3b82f6; border-top-color: transparent; margin-right: 12px; animation: spin 1s linear infinite;"></div>
                                <p style="margin: 0; color: #1e40af; font-weight: 500;">Generating your summary...</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        summary = summarize_text(pdf_text, summary_length)

                        if summary:
                            # Clear the spinner
                            st.empty()

                            # Display summary in a premium container with animation
                            with stylable_container(
                                key="summary_container",
                                css_styles="""{
                                    border-radius: 16px;
                                    border: 1px solid #e2e8f0;
                                    padding: 30px;
                                    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
                                    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
                                    margin: 30px 0;
                                    animation: fadeInUp 0.5s ease-out forwards;
                                }"""
                            ):
                                header_html = f"""
                                <div style="display: flex; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e2e8f0;">
                                    <div style="background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                                        <span style="color: white; font-size: 18px;">📋</span>
                                    </div>
                                    <div>
                                        <h3 style="margin: 0; padding: 0; font-size: 1.5rem; font-weight: 600; color: #1e40af;">Summary</h3>
                                        <p style="margin: 3px 0 0 0; color: #64748b; font-size: 0.9rem; text-transform: capitalize;">{summary_length} version</p>
                                    </div>
                                </div>
                                """
                                st.markdown(header_html, unsafe_allow_html=True)

                                # Display the summary text in a normal text component to avoid code formatting
                                st.markdown(f'<div style="line-height: 1.8; color: #334155; font-size: 1.05rem; padding: 0 5px;">{summary}</div>', unsafe_allow_html=True)

                                # Action buttons row with enhanced styling
                                st.markdown("<div style='margin: 25px 0 10px 0; height: 1px; background: linear-gradient(90deg, rgba(203, 213, 225, 0) 0%, rgba(203, 213, 225, 1) 50%, rgba(203, 213, 225, 0) 100%);'></div>", unsafe_allow_html=True)

                                # Download option with enhanced styling
                                summary_bytes = summary.encode()
                                st.download_button(
                                    label="💾 Download Summary",
                                    data=summary_bytes,
                                    file_name=f"{uploaded_file.name.split('.')[0]}_summary.txt",
                                    mime="text/plain",
                                    use_container_width=True
                                )
            else:
                # Error message with premium styling
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1), 0 2px 4px -1px rgba(239, 68, 68, 0.06);">
                    <div style="display: flex; align-items: center;">
                        <div style="background: linear-gradient(90deg, #ef4444 0%, #f87171 100%); width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                            <span style="color: white; font-size: 14px;">⚠️</span>
                        </div>
                        <p style="margin: 0; color: #b91c1c; font-weight: 600; font-size: 1rem;">Failed to extract text from the PDF. Please try another file.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Removed tips section

    # Add animation styles
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)
