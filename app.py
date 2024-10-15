from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from action_decider import ActionDecider
from models import get_session
from reminder_service import send_scheduled_reminders
import threading
import time
import logging

app = Flask(__name__)

# הגדרת לוגר
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

def reminder_loop():
    while True:
        db = next(get_db())
        try:
            send_scheduled_reminders(db)
        except Exception as e:
            logger.error(f"שגיאה בלולאת התזכורות: {e}")
        finally:
            db.close()
        time.sleep(60)  # בדיקה כל דקה

@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    incoming_message = request.values.get('Body', '').lower()
    phone_number = request.values.get('From', '')

    logger.info(f"Received message from {phone_number}: {incoming_message}")

    db = next(get_db())
    try:
        decider = ActionDecider(incoming_message, phone_number, db)
        bot_response = decider.decide_action()
        
        if "Got it!" in bot_response:
            logger.info(f"Reminder successfully created for {phone_number}: {bot_response}")
        else:
            logger.info(f"Action performed for {phone_number}: {bot_response}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        bot_response = "Sorry, an error occurred. Please try again later."
    finally:
        db.close()

    response = MessagingResponse()
    response.message(bot_response)

    logger.info(f"Sent response to {phone_number}: {bot_response}")

    return str(response)

def start_reminder_thread():
    reminder_thread = threading.Thread(target=reminder_loop)
    reminder_thread.daemon = True
    reminder_thread.start()
    logger.info("לולאת התזכורות הופעלה")

if __name__ == "__main__":
    start_reminder_thread()
    
    logger.info("מפעיל את השרת...")
    app.run(debug=False, host='0.0.0.0', port=11996)