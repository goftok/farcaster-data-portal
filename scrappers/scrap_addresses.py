import time
import requests
from psycopg2 import sql


def scrape_addresses(fid):
    url = f"https://client.warpcast.com/v2/verifications?fid={fid}"
    response = requests.get(url)

    # Return None if there's an error
    if response.status_code != 200:
        return None

    data = response.json()
    if "result" in data and "verifications" in data["result"]:
        return data["result"]["verifications"]
    return None


def insert_address_to_db(conn, fid, address):
    with conn.cursor() as cur:
        scrapped_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Insert address into database
        cur.execute(
            sql.SQL(
                """
                INSERT INTO adresses (author_fid, address, scrapped_timestamp)
                VALUES (%s, %s, %s)
                ON CONFLICT (author_fid, address) DO NOTHING
            """
            ),
            (fid, address, scrapped_timestamp),
        )
        conn.commit()
