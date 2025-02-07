from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
mongo_uri = os.getenv('DATABASE_URI')
mongo_db = os.getenv('MONGO_DB')

# Check if environment variables are set
if not mongo_uri or not mongo_db:
    raise ValueError("Environment variables DATABASE_URI or MONGO_DB are not set.")

try:
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[mongo_db]  # Access the database
    sentences_collection = db['sentences']  # Access the sentences collection

    print("Database connection successful")
except errors.PyMongoError as e:
    print(f"Database connection failed: {e}")
