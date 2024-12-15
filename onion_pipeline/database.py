"""Functions that interact with the database."""

from os import _Environ

from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor, execute_values


def get_db_connection(config: _Environ) -> connection:
    """Returns a live connection to the database."""
    return connect(
        host=config.get("DB_HOST", "localhost"),
        database=config["DB_NAME"],
        user=config.get("DB_USER"),
        password=config.get("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )


def get_organisation_id(conn: connection) -> int:
    """Returns the organisation ID for the Onion."""

    with conn.cursor() as cur:
        cur.execute("""SELECT organisation_id FROM organisation WHERE organisation_name = 'The Onion'""")
        response = cur.fetchone()

    return response["organisation_id"]


def get_category_id(conn: connection) -> int:
    """Returns the category ID for news."""

    with conn.cursor() as cur:
        cur.execute("""SELECT category_id FROM category WHERE category_name = 'News'""")
        response = cur.fetchone()
        
    return response["category_id"]


def get_current_tags(conn: connection) -> dict[str, int]:
    """Returns a dict of tag names and keys for all existing tags."""

    with conn.cursor() as cur:
        cur.execute("""SELECT tag_text, tag_id FROM tag;""")
        response = cur.fetchall()

    return {r["tag_text"]: r["tag_id"] for r in response}


def insert_new_tags(conn: connection, tags: set) -> None:

    q = """
    INSERT INTO tag
        (tag_text)
    VALUES
        %s
    ;
    """

    with conn.cursor() as cur:
        execute_values(cur, q, ((t,) for t in tags))

    conn.commit()


def insert_new_articles(conn: connection, articles: list[dict]) -> None:
    """Inserts new articles and tag-article connections into the database."""

    q = """
    INSERT INTO article
        (article_title, article_url, published, article_text,
         organisation_id, category_id)
    VALUES %s
    RETURNING article_id
    ;
    """

    with conn.cursor() as cur:
        all_ids = execute_values(cur, q, [a[:-1] for a in articles], fetch=True)
        all_ids = [r["article_id"] for r in all_ids]
        tag_connections = []
        for i in range(len(all_ids)):
            for t in articles[i][-1]:
                tag_connections.append((all_ids[i], t))

        q = """
        INSERT INTO article_tag_connection
            (article_id, tag_id)
        VALUES %s
        ;
        """

        execute_values(cur, q, tag_connections)

        conn.commit()