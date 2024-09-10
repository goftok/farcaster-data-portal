import time
import requests
from psycopg2 import sql


def scrape_casts(fid, limit=100):
    url = f"https://client.warpcast.com/v2/profile-casts?fid={fid}&limit={limit}"
    response = requests.get(url)

    # Return None if there's an error
    if response.status_code != 200:
        return None

    data = response.json()
    if "result" in data and "casts" in data["result"]:
        return data["result"]["casts"]
    return None


def insert_cast_to_db(conn, fid, cast_data):
    with conn.cursor() as cur:
        scrapped_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Extract cast details
        text = cast_data.get("text", "")
        viewCount = cast_data.get("viewCount", 0)
        combinedRecastCount = cast_data.get("combinedRecastCount", 0)
        reactions = cast_data.get("reactions", {}).get("count", 0)
        replies = cast_data.get("replies", {}).get("count", 0)
        warpsTipped = cast_data.get("warpsTipped", 0)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cast_data.get("timestamp") / 1000))

        # Insert cast into the database with conflict handling
        cur.execute(
            sql.SQL(
                """
                INSERT INTO casts (author_fid, text, viewCount, combinedRecastCount, reactions, replies, warpsTipped, timestamp, scrapped_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (author_fid, timestamp) DO NOTHING
            """
            ),
            (fid, text, viewCount, combinedRecastCount, reactions, replies, warpsTipped, timestamp, scrapped_timestamp),
        )
        conn.commit()
