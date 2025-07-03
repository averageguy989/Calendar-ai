# 📅 Calendar AI Assistant

A conversational AI assistant to manage your Google Calendar using natural language, built with FastAPI, Streamlit, and LangChain.

## Features

- Book appointments and meetings using natural language
- Check your calendar for events and free slots
- Handles natural language dates like "tomorrow", "next Monday", etc.
- Chat interface with continuous conversation

## Tech Stack

- FastAPI (backend)
- Streamlit (frontend)
- LangChain + Gemini (AI agent)
- Google Calendar API

## Setup Instructions

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/calendar-ai.git
   cd calendar-ai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Place your `service_account.json` (Google Calendar) in the project root.

5. **Run the backend:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Run the frontend:**
   ```bash
   streamlit run app.py
   ```

7. **Open your browser to** `http://localhost:8501` **to use the chat UI.**

## Security

- **Never commit your `.env` or `service_account.json` to GitHub!**
- Use `.gitignore` to keep secrets out of version control.

## License

MIT 