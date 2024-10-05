# app.py

import streamlit as st
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.visualizer import PlotlyVisualizer
from src.logger import setup_logger
import logging

st.set_page_config(page_title="Landing Page Stock Analysis", layout="wide")
logger = setup_logger(__name__)

st.title("Welcome to the Stock Analysis App!")

db_conn = DataLoader().load_data()

processor = DataProcessor(db_conn)

df = processor.get_data()
st.dataframe(data=df, use_container_width=True)
summary_df = processor.get_summary_stats()

# Plot charts
visualizer = PlotlyVisualizer()
st.plotly_chart(
    visualizer.plot_line_chart(
        summary_df,
        "name",
        "avg_price",
        "Stock Average Price",
        "stock code",
        "average price",
    )
)
