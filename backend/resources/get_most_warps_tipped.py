from flask_restful import Resource
from flasgger import swag_from
from werkzeug.exceptions import BadRequest

from psycopg2 import sql
from db_connection import get_connection, release_connection


class GetMostWarpsTipped(Resource):
    @swag_from("./swagger_docs/get-most-warps-tipped.yml")  # Update Swagger doc reference
    def post(self):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Execute SQL query to get the top 5 most warps tipped
                cur.execute(
                    sql.SQL(
                        """
                        SELECT author_fid, text, warpsTipped, viewcount, reactions, replies
                        FROM casts
                        ORDER BY warpsTipped DESC
                        LIMIT 5;
                        """
                    )
                )

                # Fetch all results from the query
                rows = cur.fetchall()

                # Format the response as a list of dictionaries
                result = [
                    {
                        "author_fid": row[0],
                        "text": row[1],
                        "warpsTipped": row[2],
                        "viewcount": row[3],
                        "reactions": row[4],
                        "replies": row[5],
                    }
                    for row in rows
                ]

            return result

        except BadRequest as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"An error occurred: {e}"}, 500
        finally:
            release_connection(conn)
