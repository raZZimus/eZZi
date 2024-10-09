import os
from dotenv import load_dotenv

# טעינת משתני הסביבה מקובץ .env
load_dotenv()

# Twilio הגדרות
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# הגדרות מסד נתונים
DATABASE_URL = os.getenv('DATABASE_URL')

# OpenAI הגדרות
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

