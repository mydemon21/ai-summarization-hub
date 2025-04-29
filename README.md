# AI Summarization Hub

A comprehensive Streamlit application that uses Google's Gemini API to provide various content summarization and learning tools.

![AI Summarization Hub](https://img.icons8.com/fluency/96/000000/artificial-intelligence.png)

## Live Demo

Try the app: [AI Summarization Hub on Streamlit Cloud](https://your-app-url-here.streamlit.app)

## Features

1. **Text Summarizer**: Summarize any text with adjustable summary length
2. **PDF Summarizer**: Extract and summarize content from PDF files
3. **YouTube Summarizer**: Generate summaries from YouTube video content
4. **Quiz Generator**: Create quiz questions from text, PDF, or YouTube content
5. **Flashcard Generator**: Generate study flashcards from various content sources

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an account or sign in
3. Generate an API key
4. Add the key to your `.env` file

## Usage

### Text Summarizer
- Enter or paste text in the text area
- Select summary length (short, medium, long)
- Click "Generate Summary"
- Download the summary as a text file

### PDF Summarizer
- Upload a PDF file
- Preview the extracted text
- Select summary length
- Generate and download the summary

### YouTube Summarizer
- Enter a YouTube video URL
- View video details and transcript
- Generate a summary of the video content
- Download the summary

### Quiz Generator
- Select a content source (Text, PDF, YouTube)
- Provide the content
- Choose the number of questions
- Generate quiz questions with answers and explanations
- Download the quiz

### Flashcard Generator
- Select a content source (Text, PDF, YouTube)
- Provide the content
- Choose the number of flashcards
- Generate study flashcards with terms and definitions
- Download flashcards in JSON or text format

## Requirements

- Python 3.7+
- Streamlit
- Google Generative AI Python SDK
- PyPDF2
- pytube
- Other dependencies listed in requirements.txt

## Notes

- For best results, provide clear, well-structured content
- The quality of AI-generated content depends on the input quality

## Deployment on Streamlit Cloud

Follow these steps to deploy the app on Streamlit Cloud:

1. **Fork or push this repository to GitHub**

2. **Sign up for Streamlit Cloud**
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account

3. **Deploy the app**
   - Click "New app"
   - Select your repository, branch, and main file (app.py)
   - Click "Deploy"

4. **Add your secrets**
   - In the app settings, find the "Secrets" section
   - Add your Google API key in the following format:
     ```
     GOOGLE_API_KEY = "your-actual-api-key-here"
     ```

5. **Your app is now live!**
   - Share the URL with others
   - The app will automatically update when you push changes to your repository

## Security Notes

- Never commit your actual API keys to GitHub
- Always use environment variables or secrets management for API keys
- The `.env` file and `.streamlit/secrets.toml` are included in `.gitignore` to prevent accidental exposure
