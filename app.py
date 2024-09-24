# app.py

import streamlit as st
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.visualizer import Visualizer
from src.logger import setup_logger
import logging

# Setup logger
logger = setup_logger(__name__)

# Streamlit app layout
st.title("Stock Analysis")

# Load data
with st.spinner():
    # st.write("Loading data...")
    loader = DataLoader()
    loader.load_data("data/stocks_data.zip", "all_stocks_5yr.csv")
logger.info("Data loaded successfully.")

# Process data
processor = DataProcessor(loader.conn)
summary_df = processor.get_summary_stats()

# Display summary stats
st.write("Summary Statistics", summary_df)

# Plot charts
visualizer = Visualizer()
st.plotly_chart(visualizer.plot_line_chart(summary_df, "Name", "avg_price"))
