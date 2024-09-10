import re
import pandas as pd
from keybert import KeyBERT

from db_connection import conn

# Initialize KeyBERT model
kw_model = KeyBERT()


# Function to extract keywords from a text (cast)
def extract_keywords(cast, top_n=5):
    keywords = kw_model.extract_keywords(
        cast,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=top_n,
    )
    return [kw[0] for kw in keywords]  # Return only the keywords (not scores)


# Function to fetch all casts from the PostgreSQL database
def fetch_all_casts(conn):
    # SQL query to fetch all casts from the 'casts' table
    query = """SELECT DISTINCT text
        FROM casts
        limit 1000
    """

    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()

    # Extract the text column from each row
    casts = [row[0] for row in results]
    return casts


def clean_text(text):
    # Remove any control characters and other illegal characters
    return re.sub(r"[\x00-\x1F\x7F-\x9F]", "", text)


# Main function to generate the Excel file with keywords and casts
def create_excel_with_casts_and_keywords(output_excel_file, conn):
    # Step 1: Fetch all casts from the database
    casts = fetch_all_casts(conn)

    # Step 2: Generate keywords for each cast
    keywords_list = []
    clean_casts = []
    for idx, cast in enumerate(casts):
        if idx % 1000 == 0:
            print(f"Processing cast {idx + 1} of {len(casts)}")

        if len(cast) < 20:
            continue

        keywords = extract_keywords(cast)  # Extract keywords for each cast
        if len(keywords) == 0:
            continue
        keywords_list.append(", ".join(keywords))
        clean_casts.append(cast)

    clean_casts = [clean_text(cast) for cast in clean_casts]
    clean_keywords = [clean_text(keywords) for keywords in keywords_list]

    # Step 3: Prepare data for the Excel file
    data = {"Casts": clean_casts, "Keywords": clean_keywords}

    # Step 4: Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Step 5: Write the DataFrame to an Excel file
    df.to_excel(output_excel_file, index=False)

    print(f"Excel file '{output_excel_file}' created successfully.")


# Example usage
if __name__ == "__main__":

    # Output Excel file
    output_excel_file = "/home/ubuntu/hackathon6/data/100k_casts_and_keywords.xlsx"

    # Create the Excel file with casts and their corresponding keywords
    create_excel_with_casts_and_keywords(output_excel_file, conn)

    # Close the database connection
    conn.close()
