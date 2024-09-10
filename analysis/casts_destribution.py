import matplotlib.pyplot as plt
from db_connection import get_connection, release_connection


def plot_casts_per_author():
    conn = get_connection()
    # Create a cursor object
    cur = conn.cursor()

    # Raw SQL query to get the count of casts per author_fid
    query = """
    SELECT author_fid, COUNT(id) as cast_count
    FROM casts
    GROUP BY author_fid
    ORDER BY author_fid;
    """

    # Execute the query
    cur.execute(query)

    # Fetch the results
    results = cur.fetchall()

    # Close the cursor and connection
    cur.close()

    # Extract author_fid and cast counts from the query results
    author_fids = [row[0] for row in results]
    cast_counts = [row[1] for row in results]

    # Plotting the data using matplotlib
    plt.figure(figsize=(40, 6))
    plt.bar(author_fids, cast_counts, color="blue")
    plt.xlabel("Author FID")
    plt.xlim([0, 40000])
    plt.ylabel("Number of Casts")
    plt.title("Number of Casts per Author FID")
    plt.grid(True)
    # Show the plot
    plt.savefig("./casts_per_author40k.png")

    release_connection(conn)


if __name__ == "__main__":
    plot_casts_per_author()
