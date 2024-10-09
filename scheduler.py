from apscheduler.schedulers.background import BackgroundScheduler
from reminder_service import send_scheduled_reminders

# פונקציה להפעלת המתזמן
def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # הפעלת הפונקציה לשליחת תזכורות כל דקה
    scheduler.add_job(send_scheduled_reminders, 'interval', minutes=1)

    # התחלת המתזמן
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
