from datetime import datetime, timedelta
from newsapi import NewsApiClient
from newspaper import Article
import constants
import re

# secret_keys contains the api_key
api = NewsApiClient(api_key=constants.NEWS_API_KEY)


def get_sources() -> list:
    """
    Returns the list of source id's truncated to the limit set
    """

    sources = []
    for src in api.get_sources(language=constants.LANGUAGE, country=constants.COUNTRY)['sources']:
        sources.append(src['id'])
    return sources[:constants.SOURCE_LIMIT]


def get_news_from_sources(from_time: datetime) -> list:
    """
    Retrieve the news articles using NEWS API

    Parameters
    ----------
    from_time: Time to get news from.

    Returns
    -------
    articles: A list of news articles.
    """

    sources = get_sources()
    sources = ",".join(sources)
    return api.get_everything(
        sources=sources,
        from_param=from_time,
        page_size=100,
        language=constants.LANGUAGE
    )['articles']


def get_full_description(articles: list):
    """
    Replace the description in the articles

    Parameters
    ----------
    articles: The list of articles
    """

    for article in articles:
        url = article['url']
        news_article = Article(url)
        news_article.download()
        news_article.parse()
        article['content'] = news_article.text
        article['source_url'] = news_article.source_url
    return articles


def reformat_articles(articles: list):
    """
    Reformat the article dict to rename and restructure keys.

    Parameters
    ----------
    articles: The list of articles
    """
    # TODO fix this: the length
    def truncate_text(text):
        while len(re.findall(constants.SPLIT_REGEX, text)) > constants.MAX_ARTICLE_LENGTH:
            index = text.rfind(".")
            index = index*10 if index == -1 else index
            text = text[:index]
        return text

    new_list = []
    for article in articles:
        new_list.append({
            "title": article["title"],
            "content": truncate_text(article["content"]),
            "datetime": article["publishedAt"],
            "source": article["source"]["name"],
            "source_url": article["source_url"],
            "image_url": article["urlToImage"],
            "article_url": article["url"],
        })
    return new_list


def curate_news(interval: int):
    """
    Retrieve the news and store the news into the database.

    Parameters
    ----------
    interval: The time interval of the scheduler in minutes.
    """

    # Selects a 'from_time' from the last curation.
    from_time = datetime.now() - constants.UTC_OFFSET - timedelta(hours=1, minutes=interval)

    articles = get_news_from_sources(from_time=from_time)
    articles = get_full_description(articles)
    articles = reformat_articles(articles)
    return articles
