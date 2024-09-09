import os
from dotenv import load_dotenv
from flask import request
from flask_restful import Resource
from flasgger import swag_from
from werkzeug.exceptions import BadRequest
from web3 import Web3

from psycopg2 import sql
from db_connection import get_connection, release_connection

load_dotenv()

INFURA_API_KEY = os.getenv("INFURA_API_KEY")
infura_url = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
web3 = Web3(Web3.HTTPProvider(infura_url))


class GetEnsForTheUser(Resource):
    @swag_from("./swagger_docs/get-ens-for-the-user.yml")
    def post(self):
        conn = get_connection()
        try:
            data = request.get_json()

            # Validate input
            if not data or "username" not in data or not isinstance(data["username"], str):
                raise BadRequest("Invalid or missing 'username' in request body.")

            username = data["username"]

            # Fetch author_fid from the profiles table
            with conn.cursor() as cur:
                cur.execute(sql.SQL("SELECT author_fid FROM profiles WHERE username = %s;"), (username,))
                author_fid_row = cur.fetchone()

                if not author_fid_row:
                    return {"ens": "No scrapped username found for this user."}, 404

                author_fid = author_fid_row[0]

                # Fetch addresses from the addresses table for the given author_fid
                cur.execute(sql.SQL("SELECT address FROM adresses WHERE author_fid = %s;"), (author_fid,))
                addresses = cur.fetchall()

                if not addresses:
                    return {"ens": "No verified addresses found for this user."}, 200

                # Retrieve ENS names for each address
                ens_names = []
                for address_tuple in addresses:
                    address = address_tuple[0]
                    ens_name = web3.ens.name(address) or "No ENS found"
                    ens_names.append(ens_name)

                return {"ens": ens_names}, 200  # Return a 200 status code with the response

        except BadRequest as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"An error occurred: {e}"}, 500
        finally:
            # Release the connection back to the pool after using it
            release_connection(conn)
