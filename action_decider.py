from reminder_service import add_reminder, edit_reminder, delete_reminder_by_id, show_user_reminders_with_id
from datetime import datetime
from openai_service import process_message_with_gpt


class CreateReminderAction:
    def execute(self, phone_number, message, reminder_date, reminder_time, timezone="UTC", is_recurring=False, recurrence_interval=None):

        return add_reminder(
            phone_number=phone_number,
            message=message,
            reminder_date=reminder_date,
            reminder_time=reminder_time,
            timezone=timezone,
            is_recurring=is_recurring,
            recurrence_interval=recurrence_interval
        )


class EditReminderAction:
    def execute(self, phone_number, message, reminder_date, reminder_time):
        return edit_reminder(phone_number, message, reminder_date, reminder_time)


class DeleteReminderAction:
    def execute(self, reminder_id):
        return delete_reminder_by_id(reminder_id)


class ShowReminderActions:
    def execute(self, phone_number):
        return show_user_reminders_with_id(phone_number)


class ActionDecider:
    def __init__(self, message, phone_number=None, timezone="UTC"):
        self.message = message
        self.phone_number = phone_number
        self.timezone = timezone

    def decide_action(self):
        gpt_result = process_message_with_gpt(
            self.message, self.phone_number, self.timezone)

        if not gpt_result or 'action' not in gpt_result:
            return "uWu I couldn't understand you"

        action = gpt_result['action']

        if action == 'add_reminder':
            return CreateReminderAction().execute(
                gpt_result['phone_number'],
                gpt_result['message'],
                gpt_result['date'],
                gpt_result['time'],
                gpt_result.get('timezone', 'UTC'),
                gpt_result.get('is_recurring', False),
                gpt_result.get('recurrence_interval', None)
            )
        elif action == 'show_reminders':
            return ShowReminderActions().execute(gpt_result['phone_number'])

        elif action == 'edit_reminder':
            return EditReminderAction().execute(
                gpt_result['phone_number'],
                gpt_result['message'],
                gpt_result['date'],
                gpt_result['time'])

        elif action == 'delete_reminder':
            return DeleteReminderAction().execute(
                gpt_result['phone_number'],
                gpt_result['message'])
        else:
            return f'uWu I can\'t do that {action} yet'
