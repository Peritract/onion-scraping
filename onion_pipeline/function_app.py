import logging
from os import environ as ENV

import azure.functions as func
from dotenv import load_dotenv

from scraping import get_most_recent_articles
from data_cleaning import get_all_new_tags, prepare_articles_for_upload
from database import get_db_connection, get_organisation_id, get_category_id, get_current_tags, insert_new_tags, insert_new_articles

app = func.FunctionApp()

@app.timer_trigger(schedule="* * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def onion_scraper_pipeline(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info("Triggering pipeline.")
    articles = get_most_recent_articles()

    with get_db_connection(ENV) as conn:

        organisation_id = get_organisation_id(conn)
        category_id = get_category_id(conn)
        current_tags = get_current_tags(conn)
        new_tags = get_all_new_tags(articles, current_tags.keys())
        if new_tags:
            insert_new_tags(conn, new_tags)
            current_tags = get_current_tags(conn)
        
        prepared_articles = prepare_articles_for_upload(organisation_id,
                                                        category_id, current_tags,
                                                        articles)

        insert_new_articles(conn, prepared_articles)

    logging.info('Python timer checked.')