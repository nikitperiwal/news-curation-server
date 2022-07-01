from datetime import datetime
from get_news import curate_news
import mongo_utils
import schedule

collection = "curated_news"


def start_curating(interval: int):
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print("Curating at: ", time)
    curated_news = curate_news(interval=interval)
    print("No. of articles scraped: ", len(curated_news))
    mongo_utils.persist_to_mongo(items=curated_news, collection_name=collection)


def schedule_curation(interval: int):
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
# shorten articles more than 1000 words. Split by punctuation too.

if __name__ == "__main__":
    schedule_curation(15)
