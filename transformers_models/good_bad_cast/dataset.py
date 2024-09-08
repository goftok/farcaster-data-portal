import torch
import pandas as pd

from psycopg2 import sql


class RegressionDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


def create_dataset(conn):
    """
    Creates a dataset for training a model from the Casts table.

    Parameters:
    conn (psycopg2 connection): A connection object to the PostgreSQL database.

    Returns:
    tuple: train_df, test_df (Pandas DataFrames with 'text' and 'labels' columns)
    """

    # Step 1: Build the SQL query using psycopg2.sql
    query = sql.SQL(
        """
        SELECT
            text,
            AVG(combinedRecastCount) AS combinedRecastCount_avg,
            AVG(reactions) AS reactions_avg,
            AVG(replies) AS replies_avg,
            AVG(warpsTipped) AS warpsTipped_avg
        FROM casts
        WHERE text IS NOT NULL
        GROUP BY text
    """
    )

    # Step 2: Execute the query using the connection
    with conn.cursor() as cur:
        cur.execute(query)
        # Fetch all rows from the executed query
        results = cur.fetchall()

    # Step 3: Convert query results to a DataFrame
    df = pd.DataFrame(results, columns=["text", "combinedRecastCount", "reactions", "replies", "warpsTipped"])

    metrics = ["combinedRecastCount", "reactions", "replies", "warpsTipped"]

    for metric in metrics:
        mean = df[metric].mean()
        std = df[metric].std()
        df[metric] = (df[metric] - mean) / std

    # Step 4: Create the 'labels' column as a combination of the metrics
    df["labels"] = df["combinedRecastCount"] + df["reactions"] + df["replies"] + df["warpsTipped"]

    # Step 5: Split into train and test sets (e.g., 80% train, 20% test)
    train_df = df.sample(frac=0.8, random_state=42)
    test_df = df.drop(train_df.index)

    # Step 6: Normalize the labels in both train and test sets
    mean = train_df["labels"].mean()
    std = train_df["labels"].std()

    train_df["labels"] = (train_df["labels"] - mean) / std
    test_df["labels"] = (test_df["labels"] - mean) / std

    # Ensure the dataset has the required columns
    train_df = train_df[["text", "labels"]]
    test_df = test_df[["text", "labels"]]

    return train_df, test_df
