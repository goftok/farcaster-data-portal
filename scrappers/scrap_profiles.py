import requests
import time
from psycopg2 import sql


def scrape_profile(fid):
    url = f"https://client.warpcast.com/v2/user?fid={fid}"
    response = requests.get(url)

    # Return None if there's an error
    if response.status_code != 200:
        return None

    data = response.json()
    if "result" in data and "user" in data["result"]:
        return data["result"]["user"]
    return None


def insert_profile_to_db(conn, profile):
    with conn.cursor() as cur:
        scrapped_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Extract necessary fields
        author_fid = profile.get("fid")
        displayName = profile.get("displayName", "")
        username = profile.get("username", "")
        followerCount = profile.get("followerCount", 0)
        followingCount = profile.get("followingCount", 0)

        # Insert into database
        cur.execute(
            sql.SQL(
                """
                INSERT INTO Profiles (author_fid, displayName, username, followerCount, followingCount, scrapped_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (author_fid) DO NOTHING
            """
            ),
            (author_fid, displayName, username, followerCount, followingCount, scrapped_timestamp),
        )
        conn.commit()
