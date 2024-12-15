# ETL Pipeline (Onion)

A pipeline that scrapes data from the Onion and stores in the database.

## Set up and installation

1. Create a virtual environment
2. Install all libraries with `pip install -r requirements.txt`
3. Create a `.env` file with the following keys:

```sh
DB_HOST=XXXXXXXXXX
DB_NAME=XXXXXXXXXX
DB_USER=XXXXXXXXXX
DB_PASSWORD=XXXXXXXXXX
```

## Development

`python main.py`