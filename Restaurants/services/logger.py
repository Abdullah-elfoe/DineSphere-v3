from .mongo import logs_collection
from datetime import datetime

def log_event(event, data=None):
    logs_collection.insert_one({
        "event": event,
        "data": data or {},
        "timestamp": datetime.utcnow()
    })