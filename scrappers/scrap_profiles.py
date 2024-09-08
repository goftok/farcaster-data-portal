import requests
import time
from psycopg2 import sql
from db_connection import conn


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
        # Extract necessary fields
        author_fid = profile.get("fid")
        displayName = profile.get("displayName", "")
        username = profile.get("username", "")
        followerCount = profile.get("followerCount", 0)
        followingCount = profile.get("followingCount", 0)
        scrapped_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # print(f"Inserting Profile: {author_fid}")
        # print(f"displayName: {displayName}")
        # print(f"username: {username}")
        # print(f"followerCount: {followerCount}")
        # print(f"followingCount: {followingCount}")
        # print(f"scrapped_timestamp: {scrapped_timestamp}")

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


def main():
    try:
        for fid in range(44000, 100001):
            profile = scrape_profile(fid)

            if profile:
                insert_profile_to_db(conn, profile)
                # print(f"Inserted profile with FID {fid} into the database.")
            else:
                print(f"FID {fid} not found or invalid.")

            if fid % 1000 == 0:
                print(f"Scrapped {fid} profiles.")

            time.sleep(0.01)  # Delay to avoid overwhelming the API
    finally:
        conn.close()


if __name__ == "__main__":
    main()
