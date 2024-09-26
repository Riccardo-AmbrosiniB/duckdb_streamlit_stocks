import duckdb
import zipfile
import os
import streamlit as st

# import logging

from .logger import setup_logger

logger = setup_logger(__name__)


class DataLoader:
    def __init__(self, db_path=":memory:"):
        self.conn = duckdb.connect(db_path)

    def load_data(
        self,
        zip_path="data/stocks_data.zip",
        csv_filename="all_stocks_5yr.csv",
        session_name_field="stocks_data",
    ):
        # Unzip and read the file
        if session_name_field in st.session_state:
            logger.info("Retrieving connection from session")
            return st.session_state["stocks_data"]
        else:
            logger.info("Unzipping file.")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall("data/")

            csv_path = os.path.join("data", csv_filename)
            # Load CSV into DuckDB
            logger.info(f"Creating DuckDB table with data at {csv_path}")
            query = f"CREATE TABLE stocks AS SELECT date,open,high,low,close,volume,Name as name FROM read_csv_auto('{csv_path}')"
            self.conn.execute(query)
            logger.info("Data loaded successfully.")

            st.session_state[session_name_field] = self.conn

            return self.conn


# Example usage:
# loader = DataLoader()
# loader.load_data('data/stocks_data.zip', 'stocks.csv')
