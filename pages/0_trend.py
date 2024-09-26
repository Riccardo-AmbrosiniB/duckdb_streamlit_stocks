import streamlit as st

from src.data_processor import DataProcessor
from src.logger import setup_logger
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.visualizer import Visualizer

logger = setup_logger(__name__)

with st.spinner():
    db_conn = DataLoader().load_data()

processor = DataProcessor(db_conn)
# df = processor.get_data()

stock_codes = processor.get_stock_codes()
# st.write(stock_names)
# st.dataframe(df)

selected_stock = st.selectbox("Select a Stock Code", stock_codes)
ma_window = st.number_input(
    "Select Rolling Average Window (in days)", min_value=1, value=7
)

if st.button("Compute time series chart with moving average"):
    logger.info(
        f"Starting computing data for stock {selected_stock}, window {ma_window}"
    )
    stock_data = processor.get_stock_data(selected_stock)
    stock_data["moving_average"] = stock_data["close"].rolling(window=ma_window).mean()
    logger.info("Calculated dataframe. Starting visualization")
    plt = Visualizer().plot_time_series_ma(
        stock_data, "date", "close", selected_stock, ma_window
    )

    st.plotly_chart(plt)
