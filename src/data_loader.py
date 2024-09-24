import duckdb
import zipfile
import os

# import logging

from .logger import setup_logger

logger = setup_logger(__name__)


class DataLoader:
    def __init__(self, db_path=":memory:"):
        self.conn = duckdb.connect(db_path)

    def load_data(self, zip_path, csv_filename):
        # Unzip and read the file
        logger.info("Unzipping file.")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("data/")

        csv_path = os.path.join("data", csv_filename)
        # Load CSV into DuckDB
        logger.info(f"Creating DuckDB table with data at {csv_path}")
        query = f"CREATE TABLE stocks AS SELECT * FROM read_csv_auto('{csv_path}')"
        self.conn.execute(query)
        logger.info("Table created")

        return self.conn


# Example usage:
# loader = DataLoader()
# loader.load_data('data/stocks_data.zip', 'stocks.csv')
