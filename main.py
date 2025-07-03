from fastapi import FastAPI, Request
from pydantic import BaseModel
from calendar_utils import book_appointment, get_events
from datetime import datetime
from agent import CalendarAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
def home(): 
    return {"status": "Server is running"}


@app.post("/agent")
async def agent(data: AgentRequest):
    print(data.message)
    response = CalendarAgent.invoke(data.message)
    print(response)
    return {"response": response}


