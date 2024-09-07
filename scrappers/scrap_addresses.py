import requests
import time
from psycopg2 import sql
from db_connection import conn


# Function to scrape addresses for a specific FID
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


# Function to insert address data into PostgreSQL
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


def main():
    try:
        for fid in range(31000, 100001):
            addresses = scrape_addresses(fid)

            if addresses:
                for address_data in addresses:
                    address = address_data.get("address")
                    if address:
                        insert_address_to_db(conn, fid, address)
                        # print(f"Inserted address for FID {fid}: {address}")
            else:
                # print(f"No addresses found for FID {fid}")
                pass

            if fid % 1000 == 0:
                print(f"Scrapped {fid} profiles.")

            time.sleep(0.01)  # Delay to avoid overwhelming the API
    finally:
        conn.close()


if __name__ == "__main__":
    main()
