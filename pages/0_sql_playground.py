import streamlit as st

from src.data_processor import DataProcessor
from src.logger import setup_logger
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.visualizer import Visualizer

logger = setup_logger(__name__)

st.set_page_config(page_title="SQL Query Playground", layout="wide")
st.title("SQL Query Playground")

with st.spinner():
    db_conn = DataLoader().load_data()

processor = DataProcessor(db_conn)

df = processor.get_data().iloc[:5]
st.dataframe(df, use_container_width=True)

# st.text_area("Enter SQL Query:")
query = st.text_area("Write your SQL query here", "SELECT * FROM stocks LIMIT 10")
if st.button("Run Query"):
    try:
        result = processor.get_custom_query(query)
        st.dataframe(result, use_container_width=True)
    except Exception as e:
        st.error(
            "Query produced bad result. Try again with a query like: *SELECT * FROM stocks LIMIT 10*"
        )
        logger.error(e)
