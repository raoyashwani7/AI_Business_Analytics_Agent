import pandas as pd
import re

from sqlalchemy import create_engine


DATABASE_URL = (
    "postgresql+psycopg2://"
    "yashwanirao@localhost:5432/project18_db"
)


engine = create_engine(DATABASE_URL)


def read_csv_file(file):

    df = pd.read_csv(file)

    return df


def create_table_from_csv(df, filename):

    # Remove .csv from filename
    table_name = filename.rsplit(".", 1)[0]

    # Make table name PostgreSQL-safe
    table_name = re.sub(r"[^a-zA-Z0-9_]", "_", table_name)

    # Convert column names to PostgreSQL-safe names
    df.columns = [
        re.sub(r"[^a-zA-Z0-9_]", "_", column)
        for column in df.columns
    ]

    # Upload DataFrame to PostgreSQL
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    return table_name