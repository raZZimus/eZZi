from twilio.rest import Client
from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER

# פונקציה לשליחת הודעת WhatsApp
def send_whatsapp_message(phone_number, message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{phone_number}'
        )
        return message.sid
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")
        return None
