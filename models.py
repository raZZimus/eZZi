from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Boolean, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from enum import Enum as PyEnum
from config import DATABASE_URL
import logging

# הגדרת הלוגר
logger = logging.getLogger(__name__)

Base = declarative_base()

# מחלקה עבור תזכורות חוזרות
class RecurrenceInterval(PyEnum):
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    MONTHLY = 'Monthly'
    YEARLY = 'Yearly'

class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(15), nullable=False, index=True)
    bot_number = Column(String(15), nullable=False)
    message = Column(String(255), nullable=True)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False, index=True)
    timezone = Column(String(50), nullable=True)
    is_recurring = Column(Boolean, default=False, index=True)
    recurrence_interval = Column(Enum(RecurrenceInterval), nullable=True)

# חיבור למסד הנתונים
engine = create_engine(DATABASE_URL)

# יצירת הטבלאות אם הן לא קיימות
def create_tables():
    try:
        Base.metadata.create_all(engine)
        logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")

# פונקציה ליצירת סשן חדש
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

# יצירת הטבלאות בעת טעינת המודול
create_tables()