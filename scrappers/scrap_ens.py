import os
import time
from dotenv import load_dotenv
from web3 import Web3
from psycopg2 import sql
from db_connection import conn

load_dotenv()

INFURA_API_KEY = os.getenv("INFURA_API_KEY")
# Connect to an Ethereum node (using Infura in this case)
infura_url = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Ensure connection to the Ethereum network
if web3.is_connected():
    print("Connected to Ethereum")


# Function to resolve ENS associated with a public address and update the DB
def get_ens_for_address(address):
    try:
        # Use the ENS module from web3 to resolve ENS associated with the address
        ens_name = web3.ens.name(address)

        # Check if the address has an ENS domain and update the is_ens column
        if ens_name:
            is_ens = True
        else:
            is_ens = False

        # Return the ENS name if available, or None otherwise
        return is_ens
    except Exception as e:
        return f"Error resolving ENS: {e}"


# Function to update the 'is_ens' field in the PostgreSQL table
def update_is_ens_in_db(conn, address, is_ens):
    try:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    """
                    UPDATE adresses
                    SET is_ens = %s
                    WHERE address = %s
                """
                ),
                (is_ens, address),
            )
            conn.commit()
    except Exception as e:
        print(f"Error updating is_ens for address {address}: {e}")


def get_addresses(conn):
    with conn.cursor() as cur:
        query = """
            SELECT address
            FROM adresses
            Order by author_fid asc
        """
        cur.execute(query)
        results = cur.fetchall()

    addresses = [row[0] for row in results]

    return addresses


# Main scraping and ENS updating function
def main():
    try:
        addresses = get_addresses(conn)

        if addresses:
            for idx, address in enumerate(addresses):
                if address[:2] != "0x":
                    continue
                if idx % 1000 == 0:
                    print(f"Processing address {idx + 1} of {len(addresses)}")
                is_ens = get_ens_for_address(address)
                update_is_ens_in_db(conn, address, is_ens)
                # print(f"Inserted address for FID {fid}: {address}")
        else:
            # print(f"No addresses found for FID {fid}")
            pass

        time.sleep(0.01)  # Delay to avoid overwhelming the API
    finally:
        conn.close()


if __name__ == "__main__":
    main()
