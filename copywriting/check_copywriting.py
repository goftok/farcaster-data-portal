from db_connection import get_connection, release_connection
from copywriting.exact_cast import find_exact_cast

from copywriting.similar_cast import find_similar_casts

# from utils.console import console


def check_cast_for_copyright(cast_text):
    conn = get_connection()
    try:
        # Check for exact matches
        exact_cast, exact_count = find_exact_cast(conn, cast_text)
        if exact_count > 0:
            return [exact_cast], exact_count

        # If no exact match found, clean the input and look for similar casts
        similar_casts, similar_count = find_similar_casts(conn, cast_text)

        return similar_casts, similar_count

    finally:
        # Release the connection back to the pool after using it
        release_connection(conn)


if __name__ == "__main__":
    cast_text = input("Enter the cast text: ")
    print(check_cast_for_copyright(cast_text))
