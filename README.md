# Onion Scraping

A project that scrapes data from [The Onion](https://theonion.com/) and stores it in a database.

## Installation

- Create a `venv`
- `pip install -r requirements.txt`

## Development

`python main.py`

## Tasks

- Add a progress bar
- Create a `bulk_update.py` script that gets historical data
- Create an `update.py` script that just gets the most recent page of Onion articles
- Create a `schema.sql` that creates and setups a database
- Adapt the `update.py` and `bulk_update.py` so that they upload to a provided database
- Adapt `update.py` so that it gets all articles since the most recent upload
  