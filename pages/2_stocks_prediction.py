import streamlit as st
from src import *
import plotly.graph_objects as go
from statsmodels.graphics.tsaplots import plot_acf

logger = logger.setup_logger(__name__)

logger.info("hello world")
st.set_page_config(page_title="Stocks Prediction Page!", layout="wide")
st.title("Stocks Prediction Page!")

with st.spinner():
    db_conn = data_loader.DataLoader().load_data()

processor = data_processor.DataProcessor(db_conn)
predictor_instance = predictor.Predictor()
viz_plotly = visualizer.PlotlyVisualizer()
viz_matlib = visualizer.MatplotlibVisualizer()

stock_codes = processor.get_stock_codes()

selected_stock = st.selectbox("Select a Stock Code", stock_codes)

if st.button("Compute prediction for selected stock"):
    logger.info(f"Starting computing prediction for stock {selected_stock}")

    df = processor.get_stock_data(selected_stock)
    stationarity = predictor_instance.test_stationarity(df["close"])
    # Let's overcomplicate this!
    stationarity_string = f"{selected_stock} is {{}} stationary!"
    st.subheader(stationarity_string.format("" if stationarity else "Not"))
    # Base plot
    line_plt = viz_plotly.plot_line_chart(df, "date", "close")
    st.plotly_chart(line_plt)

    # Time series analysis plots
    decomposed_ts = predictor_instance.season_decompose(df["close"])
    fig = viz_matlib.tsa_plots(decomposed_ts, df["close"])
    st.pyplot(fig)
