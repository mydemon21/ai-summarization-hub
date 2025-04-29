import streamlit as st
from utils import generate_quiz, extract_text_from_pdf, get_youtube_transcript

def show():
    st.title("❓ Quiz Generator")
    st.write("Generate quiz questions from text, PDF, or YouTube video.")

    # Source selection
    source_type = st.radio(
        "Select content source:",
        options=["Text", "PDF", "YouTube Video"],
        horizontal=True
    )

    content = None

    # Content input based on source type
    if source_type == "Text":
        text_input = st.text_area(
            "Enter text for quiz generation:",
            height=200,
            placeholder="Paste your text here..."
        )
        content = text_input

    elif source_type == "PDF":
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                content = extract_text_from_pdf(uploaded_file)
                if content:
                    st.success("Text extracted successfully!")
                    with st.expander("Preview extracted text"):
                        st.text_area("Extracted text:", content, height=150)
                else:
                    st.error("Failed to extract text from the PDF.")

    elif source_type == "YouTube Video":
        youtube_url = st.text_input(
            "Enter YouTube video URL:",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        if youtube_url and ("youtube.com" in youtube_url or "youtu.be" in youtube_url):
            with st.spinner("Processing YouTube video..."):
                video_info = get_youtube_transcript(youtube_url)
                if video_info:
                    content = video_info["transcript"]
                    st.success(f"Processed video: {video_info['title']}")
                    with st.expander("View transcript"):
                        st.write(content)
                else:
                    st.error("Failed to process the YouTube video.")
        elif youtube_url:
            st.warning("Please enter a valid YouTube URL.")

    # Quiz generation options
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider("Number of questions:", min_value=3, max_value=10, value=5)

    # Generate quiz button
    if st.button("Generate Quiz"):
        if not content:
            st.warning("Please provide content for quiz generation.")
        else:
            with st.spinner("Generating quiz questions..."):
                quiz = generate_quiz(content, num_questions)

                if quiz:
                    st.subheader("Generated Quiz")
                    st.markdown(quiz)

                    # Download option
                    quiz_bytes = quiz.encode()
                    st.download_button(
                        label="Download Quiz",
                        data=quiz_bytes,
                        file_name="generated_quiz.txt",
                        mime="text/plain"
                    )

    # Removed tips section
