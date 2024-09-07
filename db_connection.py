import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_DATABASE_NAME = os.getenv("POSTGRES_DATABASE_NAME")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

if not all([POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOSTNAME, POSTGRES_DATABASE_NAME, POSTGRES_PORT]):
    raise ValueError("Please make sure to set the environment variables for the database connection")

# Connect to the database
conn = psycopg2.connect(
    dbname=POSTGRES_DATABASE_NAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOSTNAME,
    port=POSTGRES_PORT,
)
