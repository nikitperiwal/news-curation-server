from secret_keys import mongo_username, mongo_password, api_key
import pytz

# Defining the constants to be used throughout the app
DATETIME_TO_STRING = "%m/%d/%Y, %H:%M:%S"
UTC_OFFSET = pytz.timezone('Asia/Kolkata')._utcoffset

# News Scraper
NEWS_API_KEY = api_key

LANGUAGE = "en"
COUNTRY = "in"
SOURCE_LIMIT = 25

MAX_ARTICLE_LENGTH = 880
SPLIT_REGEX = r"\w+(?:'\w+)?|[^\w\s]"

# Scheduler
SCHEDULE_MINUTES = 60

# MongoDB Constants
MONGO_URL = f"mongodb+srv://{mongo_username}:{mongo_password}@shortly.autde.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME = "news_db"
CURATED_TABLE = "curated_news"
