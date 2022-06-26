from datetime import datetime, timedelta
from newsapi import NewsApiClient
from newspaper import Article
from secret_keys import api_key
import pytz

# secret_keys contains the api_key
api = NewsApiClient(api_key=api_key)


def get_sources(lang: str, country: str, limit: int) -> list:
    """
    Fetch the news sources based on language and/or country

    Parameters
    ----------
    lang    -> Find sources that display news in a specific language (2-letter ISO code of the language).
    country -> Find sources that display news in a specific country (2-letter code of the country).
    limit   -> The maximum amount of sources to return

    Returns
    -------
    sources -> The list of source id's truncated to the limit set
    """

    sources = []
    for src in api.get_sources(language=lang, country=country)['sources']:
        sources.append(src['id'])
    return sources[:limit]


def get_news_from_sources(lang: str, country: str, limit: int, from_time: datetime) -> list:
    """
    Retrieve the news articles using NEWS API

    Parameters
    ----------
    lang    -> Find news in a specific language (2-letter ISO code of the language).
    country -> Find news from a specific country (2-letter code of the country).
    limit   -> The maximum amount of sources.

    Returns
    -------
    articles -> A list of news articles.
    """
    sources = get_sources(lang, country, limit)
    sources = ",".join(sources)
    return api.get_everything(sources=sources, from_param=from_time, page_size=100, language=lang)['articles']


def get_full_description(articles: list):
    """
    Replace the description in the articles

    Parameters
    ----------
    articles -> The list of articles
    """

    for article in articles:
        url = article['url']
        news_article = Article(url)
        news_article.download()
        news_article.parse()
        article['content'] = news_article.text
        #article['tags'] = news_article.tags
        article['source']['source_url'] = news_article.source_url
    return articles


def curate_news(interval: int, lang: str = "en", country: str = "in", limit: int = 25):
    """
    Retrieve the news and store the news into the database.

    Parameters
    ----------
    interval -> The time interval of the scheduler in minutes.
    lang     -> Find news in a specific language (2-letter ISO code of the language).
    country  -> Find news from a specific country (2-letter code of the country).
    limit    -> The maximum amount of sources.
    """

    # Selects a 'from_time' from the last curation.
    utc_offset = pytz.timezone('Asia/Kolkata')._utcoffset
    from_time = datetime.now() - utc_offset - timedelta(hours=1, minutes=interval)

    articles = get_news_from_sources(lang=lang, country=country, limit=limit, from_time=from_time)
    return get_full_description(articles)


if __name__ == "__main__":
    from pprint import pprint
    for x in curate_news(1, "en", "in", 5):
        pprint(x)
        print("\n\n")
