from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)

db = client[settings.MONGO_DB_NAME]

# collections
logs_collection = db["logs"]
config_collection = db["configurations"]