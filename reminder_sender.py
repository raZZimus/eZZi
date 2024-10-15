import logging
from datetime import datetime, timedelta
import pytz
from sqlalchemy.orm import Session
from models import Reminder, RecurrenceInterval
from whatsapp_service import send_whatsapp_message

# הגדרת הלוגר
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_scheduled_reminders(session: Session):
    logger.info("Checking for reminders to send...")
    now = datetime.now(pytz.utc)
    
    reminders = session.query(Reminder).all()
    
    for reminder in reminders:
        reminder_time = datetime.combine(reminder.date, reminder.time)
        reminder_time = pytz.timezone(reminder.timezone).localize(reminder_time)
        
        if now >= reminder_time:
            try:
                send_reminder(reminder)
                
                if reminder.is_recurring:
                    update_recurring_reminder(session, reminder)
                else:
                    session.delete(reminder)
                
                session.commit()
            except Exception as e:
                logger.error(f"Error sending reminder {reminder.id}: {str(e)}")
                session.rollback()

def send_reminder(reminder: Reminder):
    message = f"תזכורת: {reminder.message}"
    if reminder.is_recurring:
        message += " (תזכורת חוזרת)"
    
    logger.info(f"Sending reminder to {reminder.phone_number}: {message}")
    send_whatsapp_message(reminder.bot_number, reminder.phone_number, message)

def update_recurring_reminder(session: Session, reminder: Reminder):
    next_time = calculate_next_occurrence(reminder)
    reminder.date = next_time.date()
    reminder.time = next_time.time()
    logger.info(f"Updated recurring reminder {reminder.id} to next occurrence: {next_time}")

def calculate_next_occurrence(reminder: Reminder) -> datetime:
    current_time = datetime.combine(reminder.date, reminder.time)
    if reminder.recurrence_interval == RecurrenceInterval.DAILY:
        return current_time + timedelta(days=1)
    elif reminder.recurrence_interval == RecurrenceInterval.WEEKLY:
        return current_time + timedelta(weeks=1)
    elif reminder.recurrence_interval == RecurrenceInterval.MONTHLY:
        next_month = current_time.replace(day=1) + timedelta(days=32)
        return next_month.replace(day=min(current_time.day, (next_month.replace(day=1) - timedelta(days=1)).day))
    elif reminder.recurrence_interval == RecurrenceInterval.YEARLY:
        return current_time.replace(year=current_time.year + 1)
    else:
        raise ValueError(f"Unknown recurrence interval: {reminder.recurrence_interval}")

if __name__ == "__main__":
    # זה מאפשר לבדוק את הקובץ באופן עצמאי
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from config import DATABASE_URL
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    send_scheduled_reminders(session)