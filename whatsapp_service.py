from twilio.rest import Client
from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
import logging

# הגדרת הלוגר
logger = logging.getLogger(__name__)

# פונקציה לשליחת הודעת WhatsApp
def send_whatsapp_message(phone_number, message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{phone_number}'
        )
        logger.info(f"WhatsApp message sent successfully to {phone_number}. Message SID: {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Error sending WhatsApp message to {phone_number}: {str(e)}")
        raise

# פונקציה לשליחת הודעת WhatsApp מהבוט
def send_whatsapp_message_from_bot(bot_number, phone_number, message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=message,
            from_=f'whatsapp:{bot_number}',
            to=f'whatsapp:{phone_number}'
        )
        logger.info(f"WhatsApp message sent successfully from {bot_number} to {phone_number}. Message SID: {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Error sending WhatsApp message from {bot_number} to {phone_number}: {str(e)}")
        return None