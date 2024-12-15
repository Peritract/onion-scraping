"""A script that scrapes the most recent news articles from the Onion website."""

from time import sleep
import json

import requests as req
from bs4 import BeautifulSoup

class OnionError(Exception):
    """Errors accessing the Onion site."""


def get_article_details(url: str) -> dict:
    """Returns a dict of Onion article data."""

    result = req.get(url, timeout=5)

    if result.status_code >= 400:
        raise OnionError("Could not access URL successfully.")

    onion_soup = BeautifulSoup(result.text, features="html.parser")

    tag_holder = onion_soup.find("div", class_="taxonomy-post_tag")
    tags = tag_holder.find_all("a") if tag_holder else []
    content = onion_soup.find("div", class_="single-post-content")
    paragraphs = content.find_all("p") if content else []
    return {
        "title": onion_soup.find("h1").get_text(),
        "url": url,
        "published": onion_soup.find("time")["datetime"],
        "tags": [tag.get_text() for tag in tags],
        "text": [p.get_text() for p in paragraphs]
    }


def get_most_recent_articles() -> list[dict]:
    """Returns a list of all article details on the page."""

    result = req.get("https://theonion.com/news/page/1/",
                     timeout=5)

    if result.status_code >= 400:
        raise OnionError("Could not access URL successfully.")

    onion_soup = BeautifulSoup(result.text, features="html.parser")

    links = onion_soup.find_all("h3")

    articles = []
    for l in links:
        articles.append(get_article_details(l.find("a")["href"]))
        sleep(1)

    return articles