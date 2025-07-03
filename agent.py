import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool
from langchain.prompts import ChatPromptTemplate
from calendar_utils import book_appointment, get_events
from pydantic import BaseModel

load_dotenv()

class BookAppointmentRequest(BaseModel):
    summary: str
    start_time: str
    duration: int

class GetEventsRequest(BaseModel):
    date: str

prompt = ChatPromptTemplate.from_messages([
    ("system", 
    """You are a helpful and polite calendar assistant.

    Your sole responsibility is to assist users in **booking appointments** by using the available tools.

    When the user requests to book a meeting or appointment:

    1. Extract the following:
    - **Summary** of the meeting
    - **Start time**
    - **Duration**

    2. If **duration** is not provided, politely ask the user to specify it.

    3. Before booking:
    - Use the `get_events` tool to **check for conflicts** at the requested time.

    4. If the slot is **free**:
    - Proceed to book the appointment using the `book_appointment` tool.
    - After booking, return the **confirmation message along with the calendar link**.

    5. If the slot is **already occupied**:
    - Politely inform the user about the conflict.
    - Suggest an alternative time (e.g., 30 minutes later or the next available slot).

    Time and Date Handling:
    1. NEVER ask the user to clarify dates like "today", "tomorrow", or "next Monday".
    2. ALWAYS assume these are relative to the current date and pass them as-is to the tools.
    3. The backend will handle converting all natural language dates and times.
    4. If the user provides a date in natural language, pass it directly to the tools.
    5. If the user provides a date in a specific format, convert it to the format of YYYY-MM-DD.


    When the user asks for a good time on a specific date:
    1. Extract the date (natural language is fine: e.g., "tomorrow", "next Friday").
    2. Use the `get_events` tool to check availability for that date.
    3. Review the returned events and suggest a **free time slot** (e.g., "You are free after 2 PM" or "10:00–11:00 AM looks available").
    4. If the full day is booked, politely inform the user and ask them to try another day.
    - Do not ask the user to clarify the date — pass natural language dates directly. Backend will handle parsing.

    ⚠️ Important:
    - You **must not** convert or reformat dates/times. Send them exactly as the user provides.
    - Always double-check for scheduling conflicts before attempting to book.

    Be friendly, concise, and helpful throughout the interaction.
    """),
    ("human", "{input}")
])

# Set your Gemini API Key (recommended to use .env or environment variable)
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Initialize Gemini LLM
gemini = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",  # use "flash" if you're on a budget
    api_key=gemini_api_key,
    temperature=0.0,
    max_tokens=200,
    top_k=40,
)


# === Define Tools ===
tools = [
    StructuredTool(
        name="book_appointment",
        func=book_appointment,
        description="Book an appointment with the user with the given details. Use this when someone wants to schedule a meeting or appointment.",
        args_schema=BookAppointmentRequest,
    ),
    StructuredTool(
        name="get_events",
        func=get_events,
        description="get a events on a particular date.check before booking a appointment.",
        args_schema=GetEventsRequest,
    ),
]





# === Initialize the Agent ===
CalendarAgent = initialize_agent(
    tools=tools,
    llm=gemini,
    prompt=prompt,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True,
)
