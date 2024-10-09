from datetime import datetime
import pytz

# זמן נוכחי של השרת
server_time = datetime.now()
print(f"Server time: {server_time}")

# זמן נוכחי ב-UTC
utc_time = datetime.now(pytz.utc)
print(f"Current UTC time: {utc_time}")
