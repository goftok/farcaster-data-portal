from psycopg2 import sql
from fuzzywuzzy import fuzz

from copywriting.exact_cast import clean_cast_text


def find_similar_casts(conn, cleaned_cast_text):
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL(
                """
                SELECT text, viewCount, combinedRecastCount, reactions, replies, warpsTipped, timestamp, scrapped_timestamp
                FROM casts
            """
            )
        )
        all_casts = cur.fetchall()

        # Store similar casts
        similar_casts = []
        for cast in all_casts:
            cast_text = cast[0]
            similarity_score = fuzz.ratio(cleaned_cast_text, clean_cast_text(cast_text))

            if similarity_score > 70:  # Adjust threshold for similarity
                similar_casts.append((cast, similarity_score))

        # Sort by similarity score and return top 5
        similar_casts = sorted(similar_casts, key=lambda x: x[1], reverse=True)[:5]
        return [cast[0] for cast in similar_casts]
