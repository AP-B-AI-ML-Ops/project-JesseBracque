"""Importing the data into the database for evidently usage"""

import pandas as pd
from sqlalchemy import create_engine
from prefect import flow

DB_URI = "postgresql+psycopg://postgres:password@backend-database:5432/batch_db"

@flow(log_prints=True)
def import_data_into_db():
    """Import data from CSV into the database"""
    # Read the CSV file
    df = pd.read_csv("data-files/Daily.csv")

    # Rename columns if needed to match the table
    df = df.rename(columns={"Date": "date", "EUR": "eur"})
    df["eur"] = df["eur"].str.replace(',', '').astype(float)
    df = df.copy()
    df["gold_diff"] = df["eur"].diff()

    # Convert Date column to datetime if needed
    df["date"] = pd.to_datetime(df["date"])

    # Reorder columns to match the table definition and drop rows with nulls
    df = df[["date", "eur", "gold_diff"]].dropna()

    # Connect to the database
    engine = create_engine(DB_URI)

    # Insert data into batch_data table
    df.to_sql("batch_data", engine, if_exists="append", index=False)
    print("Data imported successfully!")

if __name__ == "__main__":
    import_data_into_db.serve(
        name="push-data-to-db"
    )
