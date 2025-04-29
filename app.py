import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from modules import text_summarizer, pdf_summarizer, youtube_summarizer, quiz_generator, flashcard_generator

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Please set your GOOGLE_API_KEY in the .env file")
    st.stop()

genai.configure(api_key=api_key)

# App configuration
st.set_page_config(
    page_title="AI Summarization Hub",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for premium UI
st.markdown("""
<style>
    /* Hide hamburger menu, footer, and other unwanted elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .stToolbar {display: none !important;}
    .stDecoration {display: none !important;}
    .appview-container .main .block-container {padding-top: 1rem;}

    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

    /* Main container styling with gradient background */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
        padding: 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Typography system */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #0f172a;
        letter-spacing: -0.02em;
    }
    h1 {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
    }
    h2 {
        font-size: 1.875rem;
        margin-top: 1.5rem;
        color: #1e40af;
    }
    h3 {
        font-size: 1.5rem;
        color: #334155;
        margin-bottom: 1rem;
    }
    p, li, span {
        font-family: 'Inter', sans-serif;
        color: #475569;
        line-height: 1.7;
        font-size: 1rem;
    }

    /* Modern button styling with gradient */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
        color: white;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2), 0 2px 4px -1px rgba(37, 99, 235, 0.1);
        transition: all 0.2s ease;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Fix for button container */
    .stButton {
        width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Fix for button container parent */
    .stButton > div {
        width: 100% !important;
        box-sizing: border-box !important;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3), 0 4px 6px -2px rgba(37, 99, 235, 0.1);
        transform: translateY(-2px);
    }
    .stButton>button:active {
        transform: translateY(0);
    }

    /* Primary button styling */
    button[kind="primary"] {
        background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%) !important;
        font-weight: 600 !important;
    }

    /* Input fields with modern styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
        background-color: #f8fafc !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        background-color: #f8fafc !important;
    }

    /* Fix for text area background */
    .stTextArea textarea {
        background-color: #f8fafc !important;
    }

    /* Override Streamlit's default text area styling */
    div[data-baseweb="textarea"] {
        background-color: #f8fafc !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    div[data-baseweb="textarea"] > div {
        background-color: #f8fafc !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    div[data-baseweb="textarea"] > div > textarea {
        background-color: #f8fafc !important;
        color: #334155 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Fix for text area container */
    .stTextArea > div {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Ensure text areas fit within containers */
    .element-container, .stTextArea, .css-ocqkz7, .css-10trblm, .css-16idsys {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Sidebar styling with gradient */
    .css-1d391kg, .css-1lcbmhc, .css-12oz5g7 {
        background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%);
        border-right: 1px solid #e2e8f0;
    }

    /* Radio buttons in sidebar */
    .stRadio > div {
        background-color: white;
        border-radius: 10px;
        padding: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }
    .stRadio > div:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    /* Card-like containers with subtle shadow */
    .stExpander, div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
    }
    .stExpander:hover, div[data-testid="stExpander"]:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03);
    }
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        padding: 1rem !important;
    }

    /* File uploader with drag and drop styling */
    .stFileUploader>div>button {
        background-color: white;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem 1rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    .stFileUploader>div>button:hover {
        border-color: #3b82f6;
        background-color: #f0f9ff;
    }

    /* Alert messages with modern styling */
    .stAlert {
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .stAlert.success {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
    }
    .stAlert.info {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
    }
    .stAlert.error {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
    }

    /* Tabs with modern styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0f2fe;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
    }

    /* Horizontal divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, rgba(203, 213, 225, 0) 0%, rgba(203, 213, 225, 1) 50%, rgba(203, 213, 225, 0) 100%);
        margin: 2rem 0;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Animations for elements */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main .block-container {
        animation: fadeIn 0.5s ease-out forwards;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Premium sidebar with modern styling and branding
st.sidebar.markdown("""
<div style='text-align: center; padding: 20px 0; margin-bottom: 20px; background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%); border-radius: 12px;'>
    <div style='background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-fill-color: transparent; font-size: 2.2rem; font-weight: 700; font-family: "Poppins", sans-serif; margin-bottom: 5px; letter-spacing: -0.02em;'>Gemini</div>
    <div style='font-size: 1.5rem; font-weight: 600; color: #334155; font-family: "Poppins", sans-serif; margin-bottom: 5px;'>Summarization Hub</div>
    <div style='width: 50px; height: 4px; background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); margin: 10px auto 15px auto; border-radius: 2px;'></div>
    <p style='font-size: 0.9rem; color: #64748b; font-family: "Inter", sans-serif;'>AI-powered content tools</p>
</div>
""", unsafe_allow_html=True)

# Modern logo/icon with animation
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 25px;'>
    <img src="https://img.icons8.com/fluency/96/000000/artificial-intelligence.png" width="80" style="filter: drop-shadow(0px 4px 6px rgba(0, 0, 0, 0.1)); animation: pulse 2s infinite ease-in-out;">
</div>
<style>
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# Feature selection with enhanced styling
st.sidebar.markdown("""
<div style='margin: 10px 0 20px 0; padding: 8px 15px; background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%); color: white; border-radius: 8px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.05em; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);'>FEATURES</div>
""", unsafe_allow_html=True)

# Custom radio buttons with hover effects
page = st.sidebar.radio(
    "Features",
    ["Text Summarizer", "PDF Summarizer", "YouTube Summarizer", "Quiz Generator", "Flashcard Generator"],
    format_func=lambda x: f"{'📝' if x == 'Text Summarizer' else '📄' if x == 'PDF Summarizer' else '🎥' if x == 'YouTube Summarizer' else '❓' if x == 'Quiz Generator' else '🗃️'} {x}",
    label_visibility="collapsed"
)

# Gradient divider
st.sidebar.markdown("""
<div style='margin: 30px 0; height: 1px; background: linear-gradient(90deg, rgba(203, 213, 225, 0) 0%, rgba(203, 213, 225, 1) 50%, rgba(203, 213, 225, 0) 100%);'></div>
""", unsafe_allow_html=True)

# Enhanced information box with icon
st.sidebar.markdown("""
<div style='background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1), 0 2px 4px -1px rgba(37, 99, 235, 0.06);'>
    <div style='display: flex; align-items: center; margin-bottom: 12px;'>
        <div style='background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;'>
            <span style='color: white; font-size: 16px;'>ℹ️</span>
        </div>
        <p style='margin: 0; color: #1e40af; font-weight: 600; font-size: 1rem; font-family: "Inter", sans-serif;'>About This App</p>
    </div>
    <p style='margin: 0; font-size: 0.9rem; color: #334155; line-height: 1.6; font-family: "Inter", sans-serif;'>This application uses Google's Gemini API to provide AI-powered summarization and content generation capabilities.</p>
</div>
""", unsafe_allow_html=True)

# Add version info and credits with enhanced styling
st.sidebar.markdown("""
<div style='position: fixed; bottom: 20px; left: 0; right: 0; text-align: center; padding: 10px; font-family: "Inter", sans-serif;'>
    <div style='font-size: 0.75rem; color: #64748b; margin-bottom: 5px;'>v1.0.0</div>
    <div style='font-size: 0.75rem; color: #94a3b8;'>Created with <span style='color: #ef4444;'>❤️</span> using Streamlit</div>
</div>
""", unsafe_allow_html=True)

# Main content based on selected page
if page == "Text Summarizer":
    text_summarizer.show()
elif page == "PDF Summarizer":
    pdf_summarizer.show()
elif page == "YouTube Summarizer":
    youtube_summarizer.show()
elif page == "Quiz Generator":
    quiz_generator.show()
elif page == "Flashcard Generator":
    flashcard_generator.show()