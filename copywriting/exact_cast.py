from psycopg2 import sql


def find_exact_cast(conn, cast_text):
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL(
                """
                SELECT text, viewCount, combinedRecastCount, reactions, replies, warpsTipped, timestamp, scrapped_timestamp
                FROM casts
                WHERE text = %s
            """
            ),
            (cast_text,),
        )
        results = cur.fetchall()

        if results:
            first_occurrence = results[0]
            return first_occurrence, len(results)
        else:
            return None, 0
