from db_connection import conn
from copywriting.exact_cast import find_exact_cast

from copywriting.similar_cast import find_similar_casts

# from utils.console import console


def check_cast_for_copyright(cast_text):
    # Check for exact matches
    exact_cast, exact_count = find_exact_cast(conn, cast_text)
    if exact_count > 0:
        # console.print(f"Exact match found: {exact_cast}")
        # console.print(f"Number of exact matches: {exact_count}")
        return [exact_cast], exact_count

    # If no exact match found, clean the input and look for similar casts
    similar_casts, similar_count = find_similar_casts(conn, cast_text)

    return similar_casts, similar_count


if __name__ == "__main__":
    cast_text = input("Enter the cast text: ")
    check_cast_for_copyright(cast_text)
