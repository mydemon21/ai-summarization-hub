import streamlit as st
from utils import generate_flashcards, extract_text_from_pdf, get_youtube_transcript
import json

def show():
    st.title("🗃️ Flashcard Generator")
    st.write("Generate study flashcards from text, PDF, or YouTube video.")

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
            "Enter text for flashcard generation:",
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

    # Flashcard generation options
    col1, col2 = st.columns(2)
    with col1:
        num_cards = st.slider("Number of flashcards:", min_value=5, max_value=20, value=10)

    # Generate flashcards button
    if st.button("Generate Flashcards"):
        if not content:
            st.warning("Please provide content for flashcard generation.")
        else:
            with st.spinner("Generating flashcards..."):
                flashcards_text = generate_flashcards(content, num_cards)

                if flashcards_text:
                    st.subheader("Generated Flashcards")

                    # Parse the flashcards text into individual cards
                    cards = []
                    current_card = {}

                    lines = flashcards_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith("CARD"):
                            if current_card and 'front' in current_card and 'back' in current_card:
                                cards.append(current_card)
                            current_card = {}
                        elif line.startswith("Front:"):
                            current_card['front'] = line[6:].strip()
                        elif line.startswith("Back:"):
                            current_card['back'] = line[5:].strip()

                    # Add the last card if it exists
                    if current_card and 'front' in current_card and 'back' in current_card:
                        cards.append(current_card)

                    # Display flashcards
                    for i, card in enumerate(cards):
                        with st.expander(f"Flashcard {i+1}: {card['front']}"):
                            st.markdown(f"**Answer:** {card['back']}")

                    # Download option
                    flashcards_json = json.dumps(cards, indent=2)
                    st.download_button(
                        label="Download Flashcards (JSON)",
                        data=flashcards_json,
                        file_name="flashcards.json",
                        mime="application/json"
                    )

                    st.download_button(
                        label="Download Flashcards (Text)",
                        data=flashcards_text,
                        file_name="flashcards.txt",
                        mime="text/plain"
                    )

    # Removed tips section
