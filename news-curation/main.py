import schedule
from datetime import datetime

import constants
import mongo_utils
from get_news import curate_news

urls_in_db = set()


def read_urls():
    """ Reads the urls from news_articles present already in db """
    global urls_in_db

    urls = list()
    for article in mongo_utils.read_from_mongo(constants.CURATED_TABLE):
        urls.append(article["article_url"])
    urls_in_db |= set(urls)


def remove_duplicates(news_articles: list):
    """ Removes the curated news_articles with urls already present in db """
    global urls_in_db

    i = 0
    urls = list()
    while i < len(news_articles):
        url = news_articles[i]["article_url"]
        if url in urls_in_db:
            news_articles.pop(i)
        else:
            i += 1
            urls.append(url)

    urls_in_db |= set(urls)
    return news_articles


def start_curating(interval: int):
    """ Curates news_articles from get_news.py and persists them to mongoDB table """

    print("Curating at: ", datetime.now().strftime(constants.DATETIME_TO_STRING))
    curated_news = curate_news(interval=interval)
    curated_news = remove_duplicates(curated_news)
    print("No. of articles scraped: ", len(curated_news))

    mongo_utils.persist_to_mongo(items=curated_news, collection_name=constants.CURATED_TABLE)


def schedule_curation(interval: int = constants.SCHEDULE_MINUTES):
    schedule.every(interval).minutes.do(
        start_curating,
        interval=interval
    )

    read_urls()
    start_curating(interval)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    schedule_curation()
