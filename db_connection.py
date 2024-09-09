import os
import psycopg2
import psycopg2.pool
import subprocess
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_DATABASE_NAME = os.getenv("POSTGRES_DATABASE_NAME")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

if not all([POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOSTNAME, POSTGRES_DATABASE_NAME, POSTGRES_PORT]):
    raise ValueError("Please make sure to set the environment variables for the database connection")


# Setup connection pool
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        user=POSTGRES_USERNAME,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOSTNAME,
        port=POSTGRES_PORT,
        database=POSTGRES_DATABASE_NAME,
    )
    if connection_pool:
        print("Connection pool created successfully")
except Exception as e:
    print(f"Error creating connection pool: {e}")
    raise


def get_connection():
    try:
        return connection_pool.getconn()
    except Exception as e:
        print(f"Failed to get connection from pool: {e}")
        raise


def release_connection(conn):
    try:
        connection_pool.putconn(conn)
    except Exception as e:
        print(f"Failed to release connection: {e}")
        raise


def close_all_connections():
    try:
        connection_pool.closeall()
    except Exception as e:
        print(f"Failed to close all connections: {e}")


def backup_postgres_db(output_path) -> str:
    """
    Creates a backup of the PostgreSQL database connected via conn.

    Parameters:
    conn (psycopg2 connection): A connection object to the PostgreSQL database.
    output_path (str): The path where the dump file will be saved.

    Returns:
    str: The path to the saved backup file.
    """

    # Check if output directory exists, if not, create it
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    # Create the pg_dump command
    dump_command = [
        "pg_dump",
        "-U",
        POSTGRES_USERNAME,
        "-h",
        POSTGRES_HOSTNAME,
        "-F",
        "c",  # Custom format for pg_restore
        "-d",
        POSTGRES_DATABASE_NAME,
        "-f",
        output_path,  # Output path for dump file
    ]

    try:
        # Run the pg_dump command
        subprocess.run(dump_command, check=True, env={"PGPASSWORD": POSTGRES_PASSWORD})
        print(f"Backup successfully created at {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during backup: {e}")
        raise


if __name__ == "__main__":
    backup_postgres_db("./data/backup.dump")
