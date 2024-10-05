import streamlit as st

from src.data_processor import DataProcessor
from src.logger import setup_logger
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.visualizer import Visualizer
import plotly.graph_objects as go

logger = setup_logger(__name__)

st.set_page_config(page_title="Stocks Trend Analysis Page!", layout="wide")
st.title("Stocks Trend Analysis Page!")

with st.spinner():
    db_conn = DataLoader().load_data()

processor = DataProcessor(db_conn)

stock_codes = processor.get_stock_codes()

selected_stock = st.selectbox("Select a Stock Code", stock_codes)
ma_window = st.number_input(
    "Select Rolling Average Window (in days)", min_value=1, value=7
)

if st.button("Compute time series chart with moving average"):
    logger.info(
        f"Starting computing data for stock {selected_stock}, window {ma_window}"
    )
    # Get data and compute moving average on the dataframe
    # stock_data = processor.get_stock_data(selected_stock)
    # stock_data["moving_average"] = stock_data["close"].rolling(window=ma_window).mean()
    # logger.info("Calculated dataframe. Starting visualization")
    # plt = Visualizer().plot_time_series_ma(
    #     stock_data, "date", "close", selected_stock, ma_window
    # )
    # Get data with moving average with a query
    stock_data = processor.get_stock_data_rolling_average(selected_stock, ma_window)
    logger.info("Calculated dataframe. Starting visualization")
    plt_rolling_average = Visualizer().plot_time_series_ma(
        df=stock_data,
        x_date_col="date",
        y_stock_price_col="close",
        y_ma_col="moving_average",
        stock_code=selected_stock,
        ma_window=ma_window,
    )

    # st.plotly_chart(plt_rolling_average)

    stock_return = processor.get_stock_return(selected_stock)

    # logger.info(stock_return.count())
    st.write(f"Daily Returns for {selected_stock}")
    stock_return["return_color"] = stock_return["daily_return"].apply(
        lambda x: "green" if x > 0 else "red"
    )
    plt_returns = Visualizer().plot_stock_returns_chart(
        df=stock_return,
        x_col="date",
        y_col="daily_return",
        marker_col="return_color",
        selected_stock=selected_stock,
    )

    # # TODO: Try fixing axes synchronization
    # # Synchronize both charts to zoom/pan together
    # plt_rolling_average.update_layout(xaxis_rangeslider_visible=False)
    # plt_returns.update_layout(xaxis_rangeslider_visible=False)

    # # Adding the synchronized updates using Plotly's relayout event
    # plt_rolling_average.update_xaxes(matches="x")
    # plt_returns.update_xaxes(matches="x")

    # Display both charts
    st.plotly_chart(plt_rolling_average)
    st.plotly_chart(plt_returns)
