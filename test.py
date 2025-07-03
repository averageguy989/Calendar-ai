from calendar_utils import book_appointment, get_events

# 🔧 Test booking a meeting
print(book_appointment(
    "ChatGPT Test Meeting",
    "2025-07-02T15:00:00+05:30",
    "2025-07-02T15:30:00+05:30"
))

# 🔍 Test getting existing events for today
from datetime import date
print(get_events(str(date.today())))
