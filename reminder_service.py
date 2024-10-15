from models import Reminder, RecurrenceInterval
from datetime import datetime, timedelta
from whatsapp_service import send_whatsapp_message
import logging
import pytz

logger = logging.getLogger(__name__)

def add_reminder(db, phone_number, bot_number, message, reminder_date, reminder_time, timezone="UTC", is_recurring=False, recurrence_interval=None):
    new_reminder = Reminder(
        phone_number=phone_number,
        bot_number=bot_number,
        message=message,
        date=reminder_date,
        time=reminder_time,
        timezone=timezone,
        is_recurring=is_recurring,
        recurrence_interval=recurrence_interval
    )
    
    db.add(new_reminder)
    db.commit()
    logger.info(f"New reminder created: ID={new_reminder.id}, Phone={phone_number}, Bot={bot_number}, Message='{message}', Date={reminder_date}, Time={reminder_time}")
    return f"Got it! I'll remind you to {message} on {reminder_date} at {reminder_time}. Reminder ID: {new_reminder.id}"

def edit_reminder(db, phone_number, message, reminder_date, reminder_time):
    reminder = db.query(Reminder).filter_by(phone_number=phone_number, message=message).first()
    
    if reminder:
        reminder.date = reminder_date
        reminder.time = reminder_time
        db.commit()
        return f"הבנתי, עדכנתי את התזכורת '{message}' לתאריך {reminder_date} בשעה {reminder_time}"
    else:
        return f"מצטער, לא מצאתי תזכורת כזו ברשימה שלך"

def delete_reminder_by_id(db, reminder_id):
    reminder = db.query(Reminder).filter_by(id=reminder_id).first()
    if reminder:
        db.delete(reminder)
        db.commit()
        return f"תזכורת מספר {reminder_id} נמחקה בהצלחה."
    else:
        return f"לא נמצאה תזכורת עם מספר זיהוי: {reminder_id}"

def show_user_reminders_with_id(db, phone_number):
    reminders = db.query(Reminder).filter_by(phone_number=phone_number).all()
    if reminders:
        reminder_list = [f"{r.id}: {r.message} בתאריך {r.date} בשעה {r.time}" for r in reminders]
        return "\n".join(reminder_list)
    else:
        return "אין לך תזכורות כרגע."

def send_scheduled_reminders(db):
    logger.info(f"Starting to check reminders. Current UTC time: {now}")
    now = datetime.now(pytz.utc)

    
    reminders = db.query(Reminder).all()
    
    for reminder in reminders:
        reminder_time = pytz.timezone(reminder.timezone).localize(
            datetime.combine(reminder.date, reminder.time)
        ).astimezone(pytz.utc)
        
        logger.info(f"Checking reminder: ID={reminder.id}, scheduled for {reminder_time}, current time: {now}")
        
        if now >= reminder_time:
            try:
                send_reminder(reminder)
                logger.info(f"Sent reminder: ID={reminder.id}")
                
                if not reminder.is_recurring:
                    db.delete(reminder)
                else:
                    update_recurring_reminder(db, reminder)
                
                db.commit()
            except Exception as e:
                logger.error(f"Error sending reminder {reminder.id}: {str(e)}")
                db.rollback()
        else:
            logger.info(f"Reminder ID={reminder.id} not due yet. Time difference: {reminder_time - now}")

def send_reminder(reminder: Reminder):
    message = f"תזכורת: {reminder.message}"
    if reminder.is_recurring:
        message += " (תזכורת חוזרת)"
    
    logger.info(f"Sending reminder to {reminder.phone_number}: {message}")
    send_whatsapp_message(reminder.phone_number, message)

def update_recurring_reminder(db, reminder: Reminder):
    next_time = calculate_next_occurrence(reminder)
    reminder.date = next_time.date()
    reminder.time = next_time.time()
    logger.info(f"Updated recurring reminder {reminder.id} to next occurrence: {next_time}")

def calculate_next_occurrence(current_datetime, recurrence_interval):
    if recurrence_interval == RecurrenceInterval.DAILY:
        return current_datetime + timedelta(days=1)
    elif recurrence_interval == RecurrenceInterval.WEEKLY:
        return current_datetime + timedelta(weeks=1)
    elif recurrence_interval == RecurrenceInterval.MONTHLY:
        next_month = current_datetime.replace(day=1) + timedelta(days=32)
        return next_month.replace(day=min(current_datetime.day, (next_month.replace(day=1) - timedelta(days=1)).day))
    elif recurrence_interval == RecurrenceInterval.YEARLY:
        return current_datetime.replace(year=current_datetime.year + 1)
    else:
        return current_datetime