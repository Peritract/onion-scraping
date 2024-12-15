"""Functions that manage/transform data before it is uploaded."""

def get_all_new_tags(articles: list[dict], current_tags) -> set:
    """Returns all unique tags that are not currently recorded."""
    tags = []
    for article in articles:
        for t in article["tags"]:
            if t not in current_tags:
                tags.append(t)
    return set(tags)


def prepare_articles_for_upload(organisation_id: int, category_id: int, 
                                current_tags: dict, articles: list[dict]):
    prepared_articles = []

    for article in articles:
        article["text"] = "\n".join(article["text"])
        article["tags"] = [current_tags[t] for t in article["tags"]]

        prepared_articles.append((
            article["title"],
            article["url"],
            article["published"],
            article["text"],
            organisation_id,
            category_id,
            article["tags"]
        ))

    return prepared_articles
