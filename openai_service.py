from openai import OpenAI
from config import OPENAI_API_KEY
from datetime import datetime, date, time
import json

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """
You are a virtual assistant that manages reminders.
Your task is to parse user input and respond with JSON-formatted data that includes:
- action (e.g., add_reminder, show_reminders, delete_reminder, edit_reminder)
- reminder_id (if the user specifies a reminder number)
- phone_number (if provided in the input)
- message (the content of the reminder)
- date (for the reminder, in YYYY-MM-DD format)
- time (for the reminder, in HH:MM format)
- timezone (if specified, otherwise use UTC)
- is_recurring (boolean, default to false)
- recurrence_interval (optional, can be DAILY, WEEKLY, MONTHLY, YEARLY)

If the user does not specify a time, default to 09:00.
If the user specifies a relative time like "in 2 minutes", "tomorrow", or "next week", convert it to an absolute date and time based on the current time.

If you cannot parse a date or time from the input, return null for those fields.

Always respond with a JSON dictionary. For example:
{
  "action": "add_reminder",
  "phone_number": null,
  "message": "call dad",
  "date": "2024-10-24",
  "time": "09:00",
  "timezone": "UTC",
  "is_recurring": false,
  "recurrence_interval": null
}
"""
def process_message_with_gpt(message, phone_number=None, timezone=None):
    try:
        current_time = datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M")
        full_prompt = f"{SYSTEM_PROMPT}\nCurrent time: {current_time_str}\nUser timezone: {timezone}\nUser message: {message}"
        
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": message}
            ]
        )
        
        response_content = completion.choices[0].message.content
        parsed_content = json.loads(response_content)
        
        if phone_number:
            parsed_content["phone_number"] = phone_number
        
        if parsed_content.get("date") and parsed_content.get("time"):
            parsed_content["date"] = date.fromisoformat(parsed_content["date"])
            parsed_content["time"] = time.fromisoformat(parsed_content["time"])
        
        return parsed_content
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Raw response: {response_content}")
    except Exception as e:
        print(f"Error processing message with GPT: {str(e)}")
    
    return None