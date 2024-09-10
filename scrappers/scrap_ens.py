import os
from web3 import Web3
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

INFURA_API_KEY = os.getenv("INFURA_API_KEY")

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
        conn.rollback()  # Rollback the transaction if an error occurs


def get_addresses(conn):
    with conn.cursor() as cur:
        query = """
            SELECT address
            FROM adresses
            WHERE author_fid > 2000
            ORDER BY author_fid ASC
        """
        cur.execute(query)
        results = cur.fetchall()

    addresses = [row[0] for row in results]

    return addresses
