from psycopg2 import sql


def find_exact_cast(conn, cast_text):
    with conn.cursor() as cur:
        # Query to fetch the cast and associated profile, ordered by timestamp (ascending)
        cur.execute(
            sql.SQL(
                """
                SELECT
                    casts.text, casts.viewCount, casts.combinedRecastCount, casts.reactions,
                    casts.replies, casts.warpsTipped, casts.timestamp, casts.scrapped_timestamp,
                    profiles.author_fid, profiles.displayName, profiles.username, profiles.followerCount,
                    profiles.followingCount, profiles.scrapped_timestamp AS profile_scrapped_timestamp
                FROM casts
                JOIN profiles ON casts.author_fid = profiles.author_fid
                WHERE casts.text = %s
                ORDER BY casts.timestamp ASC
                LIMIT 1
                """
            ),
            (cast_text,),
        )

        # Fetch the first result
        result = cur.fetchone()
        if result:
            # Map the result to a dictionary with field names as keys
            result_dict = {
                "text": result[0],
                "viewCount": result[1],
                "combinedRecastCount": result[2],
                "reactions": result[3],
                "replies": result[4],
                "warpsTipped": result[5],
                "timestamp": result[6],
                "scrapped_timestamp": result[7],
                "author_fid": result[8],
                "displayName": result[9],
                "username": result[10],
                "followerCount": result[11],
                "followingCount": result[12],
                "profile_scrapped_timestamp": result[13],
            }

            # Query to count the number of exact matches
            cur.execute(
                sql.SQL(
                    """
                    SELECT COUNT(*)
                    FROM casts
                    WHERE text = %s
                    """
                ),
                (cast_text,),
            )
            exact_count = cur.fetchone()[0]

            return result_dict, exact_count
        else:
            return None, 0
