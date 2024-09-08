from psycopg2 import sql
from fuzzywuzzy import fuzz

from copywriting.utils import clean_cast_text

SIMILARITY_THRESHOLD = 80


def find_similar_casts(conn, cast_text_to_check):
    # TODO: Add checking of the cast is a substring of any existing cast
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL(
                """
                SELECT text, viewCount, combinedRecastCount, reactions, replies, warpsTipped, timestamp, scrapped_timestamp
                FROM casts
                ORDER BY casts.timestamp ASC
            """
            )
        )
        all_casts = cur.fetchall()

        # Store similar casts
        similar_casts = []
        for cast in all_casts:
            cast_text = cast[0]
            cleaned_cast_text = clean_cast_text(cast_text)
            cleaned_cast_text_to_check = clean_cast_text(cast_text_to_check)

            similarity_score = fuzz.ratio(cleaned_cast_text, cleaned_cast_text_to_check)

            if similarity_score > SIMILARITY_THRESHOLD:
                similar_casts.append((cast, similarity_score))

        # Sort by similarity score and return top 5
        similar_casts = sorted(similar_casts, key=lambda x: x[1], reverse=True)[:5]
        return [cast[0] for cast in similar_casts], len(similar_casts)
