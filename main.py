"""A script that scrapes data from the Onion website."""

import requests as req
from bs4 import BeautifulSoup


class OnionError(Exception):
    """Errors accessing the Onion site."""
    pass


def get_article_details(url: str) -> dict:
    """Returns a dict of Onion article data."""
    
    result = req.get(url)

    if result.status_code >= 400:
        raise OnionError("Could not access URL successfully.")
    
    onion_soup = BeautifulSoup(result.text, features="html.parser")

    return {
        "title": onion_soup.find("h1").get_text()
    }



def get_articles_from_page(url: str) -> list[dict]:
    """Returns a list of all article details on the page."""
    pass


if __name__ == "__main__":

    print(get_article_details("https://theonion.com/report-most-americans-have-enough-saved-for-absolutely-incredible-single-day-of-retirement/"))