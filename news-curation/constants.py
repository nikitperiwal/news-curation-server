import os
import pytz
from dotenv import load_dotenv

load_dotenv()

# Defining the constants to be used throughout the app
DATETIME_TO_STRING = "%m/%d/%Y, %H:%M:%S"
UTC_OFFSET = pytz.timezone('Asia/Kolkata')._utcoffset

# News Scraper
NEWS_API_KEY = os.environ["API_KEY"]

LANGUAGE = "en"
COUNTRY = "in"
SOURCE_LIMIT = 25

MAX_ARTICLE_LENGTH = 880
SPLIT_REGEX = r"\w+(?:'\w+)?|[^\w\s]"

# Scheduler
SCHEDULE_MINUTES = 60

# MongoDB Constants
mongo_username = os.environ["MONGO_USERNAME"]
mongo_password = os.environ["MONGO_PASSWORD"]
MONGO_URL = f"mongodb+srv://{mongo_username}:{mongo_password}@shortly.autde.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME = "news_db"
CURATED_TABLE = "curated_news"
