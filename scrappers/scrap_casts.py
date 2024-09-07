import requests
import time
from psycopg2 import sql
from db_connection import conn


# Function to scrape casts for a specific FID
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


# Function to insert cast data into PostgreSQL with conflict handling
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


def main():
    try:
        for fid in range(1, 100001):
            casts = scrape_casts(fid)

            if casts:
                for cast in casts:
                    insert_cast_to_db(conn, fid, cast)
            else:
                print(f"No casts found for FID {fid}")

            if fid % 1000 == 0:
                print(f"Scraped {fid} profiles.")

            time.sleep(0.1)  # Delay to avoid overwhelming the API
    finally:
        conn.close()


if __name__ == "__main__":
    main()
