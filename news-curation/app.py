from datetime import datetime
from get_news import curate_news
import mongo_utils
import schedule
import constants

url_in_db = set()


def start_curating(interval: int):
    print("Curating at: ", datetime.now().strftime(constants.DATETIME_TO_STRING))
    curated_news = curate_news(interval=interval)
    print("No. of articles scraped: ", len(curated_news))
    mongo_utils.persist_to_mongo(items=curated_news, collection_name=constants.CURATED_TABLE)


def schedule_curation(interval: int = constants.SCHEDULE_MINUTES):
    schedule.every(interval).minutes.do(
        start_curating,
        interval=interval
    )

    while True:
        schedule.run_pending()


# TODO
# set url as the primary key.
# think of a way to prevent same articles.
# discard articles less than 45 words.

if __name__ == "__main__":
    schedule_curation()
