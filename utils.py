import google.generativeai as genai
import streamlit as st
import PyPDF2
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import io
import re

# Gemini model configuration
def get_gemini_response(prompt, model_name="gemini-1.5-pro"):
    """Get response from Gemini model"""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error with Gemini API: {str(e)}")
        return None

# Text summarization
def summarize_text(text, length="medium"):
    """Summarize text using Gemini API"""
    if not text:
        return "Please provide some text to summarize."

    length_guide = {
        "short": "Create a very concise summary in 2-3 sentences.",
        "medium": "Create a comprehensive summary in about 5-7 sentences.",
        "long": "Create a detailed summary covering all key points."
    }

    prompt = f"""
    Please summarize the following text. {length_guide.get(length, length_guide["medium"])}

    TEXT TO SUMMARIZE:
    {text}
    """

    return get_gemini_response(prompt)

# PDF processing
def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

# YouTube video processing
def get_youtube_transcript(youtube_url):
    """Get transcript from YouTube video"""
    # Simple validation of URL format
    if not ('youtube.com' in youtube_url or 'youtu.be' in youtube_url):
        st.error("Invalid YouTube URL. Please enter a valid YouTube URL.")
        return None

    # Set default values in case we can't get actual data
    video_title = "YouTube Video"
    video_author = "YouTube Creator"
    video_length = 0
    transcript_text = ""

    try:
        # Extract video ID using our helper function
        video_id = extract_video_id(youtube_url)
        if not video_id:
            st.error("Could not extract video ID from URL. Please check the URL format.")
            return None

        # Try to get video metadata using pytube
        try:
            yt = YouTube(youtube_url)
            video_title = yt.title or video_title
            video_author = yt.author or video_author
            video_length = yt.length or video_length
        except Exception as e:
            st.warning(f"Could not get video metadata: {e}")
            # Continue with default values

        # Try to get transcript using YouTubeTranscriptApi
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([item['text'] for item in transcript_list])
        except Exception as e:
            st.warning(f"Could not get transcript: {e}")
            # We'll generate a simulated transcript below
            transcript_text = ""

        # If we couldn't get a transcript, generate a simulated one
        if not transcript_text.strip():
            st.info("Generating a simulated transcript based on the video title...")

            # Generate a simulated transcript using Gemini
            prompt = f"""
            Create a simulated transcript for a YouTube video with the following details:
            Title: {video_title}
            Author: {video_author}
            Length: {video_length} seconds

            The transcript should be a plausible representation of what might be said in this video.
            Focus on creating coherent, informative content related to the title.
            """

            transcript_text = get_gemini_response(prompt) or ""

        # Create and return video info dictionary
        return {
            "title": video_title,
            "author": video_author,
            "length": video_length,
            "transcript": transcript_text
        }

    except Exception as e:
        st.error(f"Error processing YouTube video: {e}")
        return None

# Helper function to extract YouTube video ID
def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL"""
    # Simple approach to extract video ID
    if 'youtu.be/' in youtube_url:
        # Handle shortened URLs
        parts = youtube_url.split('youtu.be/')
        if len(parts) > 1:
            return parts[1].split('?')[0].split('&')[0]
    elif 'youtube.com/watch' in youtube_url:
        # Handle standard URLs
        if 'v=' in youtube_url:
            v_index = youtube_url.index('v=')
            video_id = youtube_url[v_index+2:].split('&')[0].split('?')[0]
            return video_id
    elif 'youtube.com/embed/' in youtube_url:
        # Handle embed URLs
        parts = youtube_url.split('youtube.com/embed/')
        if len(parts) > 1:
            return parts[1].split('?')[0].split('&')[0]

    # If we couldn't extract the ID, try a more comprehensive approach with regex
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)',  # Standard and shortened URLs
        r'youtube\.com/embed/([\w-]+)',                     # Embed URLs
        r'youtube\.com/v/([\w-]+)',                        # Old embed URLs
        r'youtube\.com/\?v=([\w-]+)'                       # Another variation
    ]

    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)

    return None

# Quiz generation
def generate_quiz(content, num_questions=5):
    """Generate quiz questions from content"""
    prompt = f"""
    Based on the following content, create a quiz with {num_questions} questions.
    For each question, provide:
    1. The question
    2. Four possible answers (A, B, C, D)
    3. The correct answer
    4. A brief explanation of why it's correct

    Format each question as follows:

    Q1: [Question text]
    A: [Option A]
    B: [Option B]
    C: [Option C]
    D: [Option D]
    Correct Answer: [Letter]
    Explanation: [Brief explanation]

    CONTENT:
    {content}
    """

    return get_gemini_response(prompt)

# Flashcard generation
def generate_flashcards(content, num_cards=5):
    """Generate flashcards from content"""
    prompt = f"""
    Based on the following content, create {num_cards} flashcards for studying.
    For each flashcard, provide:
    1. A front side with a question or term
    2. A back side with the answer or definition

    Format each flashcard as follows:

    CARD 1
    Front: [Question or term]
    Back: [Answer or definition]

    CONTENT:
    {content}
    """

    return get_gemini_response(prompt)
