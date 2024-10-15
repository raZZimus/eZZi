from reminder_service import add_reminder, edit_reminder, delete_reminder_by_id, show_user_reminders_with_id
from datetime import datetime
from openai_service import process_message_with_gpt
from config import TWILIO_WHATSAPP_NUMBER
import logging

logger = logging.getLogger(__name__)

class CreateReminderAction:
    def execute(self, db, phone_number, message, reminder_date, reminder_time, timezone="UTC", is_recurring=False, recurrence_interval=None):
        return add_reminder(
            db,
            phone_number=phone_number,
            bot_number=TWILIO_WHATSAPP_NUMBER,
            message=message,
            reminder_date=reminder_date,
            reminder_time=reminder_time,
            timezone=timezone,
            is_recurring=is_recurring,
            recurrence_interval=recurrence_interval
        )

class EditReminderAction:
    def execute(self, db, phone_number, message, reminder_date, reminder_time):
        return edit_reminder(db, phone_number, message, reminder_date, reminder_time)

class DeleteReminderAction:
    def execute(self, db, reminder_id):
        return delete_reminder_by_id(db, reminder_id)

class ShowReminderActions:
    def execute(self, db, phone_number):
        reminders = show_user_reminders_with_id(db, phone_number)
        return f"הנה התזכורות שלך:\n{reminders}"

class ActionDecider:
    def __init__(self, message, phone_number, db, timezone="UTC"):
        self.message = message
        self.phone_number = phone_number
        self.db = db
        self.timezone = timezone

    def decide_action(self):
        try:
            gpt_result = process_message_with_gpt(
                self.message, self.phone_number, self.timezone)

            if not gpt_result or 'action' not in gpt_result:
                return "מצטער, לא הצלחתי להבין את הבקשה שלך."

            action = gpt_result['action']

            if action == 'add_reminder':
                return CreateReminderAction().execute(
                    self.db,
                    gpt_result['phone_number'],
                    gpt_result['message'],
                    gpt_result['date'],
                    gpt_result['time'],
                    gpt_result.get('timezone', 'UTC'),
                    gpt_result.get('is_recurring', False),
                    gpt_result.get('recurrence_interval', None)
                )
            elif action == 'show_reminders':
                return ShowReminderActions().execute(self.db, gpt_result['phone_number'])
            elif action == 'edit_reminder':
                return EditReminderAction().execute(
                    self.db,
                    gpt_result['phone_number'],
                    gpt_result['message'],
                    gpt_result['date'],
                    gpt_result['time'])
            elif action == 'delete_reminder':
                return DeleteReminderAction().execute(
                    self.db,
                    gpt_result['reminder_id'])
            else:
                return f'מצטער, אני לא יכול לבצע את הפעולה {action} כרגע.'
        except Exception as e:
            logger.error(f"שגיאה בעיבוד הפעולה: {e}")
            return "אירעה שגיאה בעיבוד הבקשה. אנא נסה שוב."