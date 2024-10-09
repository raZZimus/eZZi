from models import Reminder, session
from datetime import datetime

def add_reminder(phone_number, message, reminder_date, reminder_time, timezone = "UTC", is_recurring=False, recurrence_interval=None):

    new_reminder = Reminder(
        phone_number=phone_number,
        message=message,
        date=reminder_date,
        time=reminder_time,
        timezone=timezone,
        is_recurring=is_recurring,
        recurrence_interval=recurrence_interval
    )
    
    session.add(new_reminder)
    session.commit()
    return f"Got it! ill remind you to {message} on {reminder_date} at {reminder_time}. uWu"

#def add_reminder(phone_number, message, reminder_date, reminder_time, timezone=None):

    if isinstance(reminder_date, str):
        reminder_date = datetime.strptime(reminder_date, "%Y-%m-%d").date()

    if isinstance(reminder_time, str):
        reminder_time = datetime.strptime(reminder_time, "%H:%M").time()

    new_reminder = Reminder(
        phone_number=phone_number,
        message=message,
        date=reminder_date,
        time=reminder_time,
        timezone=timezone
    )

    session.add(new_reminder)
    session.commit()

    return f"Reminder added for {phone_number}: {message} on {reminder_date} at {reminder_time}"

# פונקציה לעריכת תזכורת במסד הנתונים
def edit_reminder(phone_number, message, reminder_date, reminder_time):
    # שליפת התזכורת הקיימת לפי מספר הטלפון והודעת התזכורת
    reminder = session.query(Reminder).filter_by(phone_number=phone_number, message=message).first()
    
    if reminder:
        # עדכון פרטי התזכורת
        reminder.date = reminder_date
        reminder.time = reminder_time
        session.commit()
        return f"Gotcha, I've updated {message} on {reminder_date} at {reminder_time} uWu"
    else:
        return f"I'm sowwy 🥺 I don't see this reminder in my list"


# פונקציה למחיקת תזכורת
def delete_reminder_by_id(reminder_id):
    reminder = session.query(Reminder).filter_by(id=reminder_id).first()
    if reminder:
        session.delete(reminder)
        session.commit()
        return f"Iv'e deleted the reminder (I will kill for you FYI.. uWu)."
    else:
        return f"I don't see this reminder in my list, maybe we deleted it already? uWu?"


# פונקציה להצגת כל התזכורות
def show_user_reminders_with_id(phone_number):
    reminders = session.query(Reminder).filter_by(phone_number=phone_number).all()
    if reminders:
        return [f"uWu {r.id}: {r.message} on {r.date} at {r.time}" for r in reminders]
    else:
        return "You don't have any reminders."