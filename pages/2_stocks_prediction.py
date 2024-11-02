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

    closure_ts = df.set_index("date")["close"]
    stationarity = predictor_instance.test_stationarity(closure_ts)
    # Let's overcomplicate this!
    stationarity_string = f"{selected_stock} is {{}} stationary!"
    st.subheader(stationarity_string.format("" if stationarity else "Not"))
    # Base plot
    line_plt = viz_plotly.plot_line_chart(df, "date", "close")
    st.plotly_chart(line_plt)

    # Time series analysis plots
    decomposed_ts = predictor_instance.season_decompose(closure_ts)
    fig = viz_matlib.tsa_plots(decomposed_ts, closure_ts)
    st.pyplot(fig)

    # Time series prediction
    # arma_model = predictor_instance.fit_arma_model(df)
    with st.spinner(text="Calculating best model..."):
        auto_arima_model = predictor_instance.auto_arima(closure_ts)
    st.write(auto_arima_model.summary())
    forecast, confidence_interval = auto_arima_model.predict(
        n_periods=60, return_conf_int=True
    )
    fig_forecast = viz_matlib.prediction_plot(closure_ts, forecast, confidence_interval)
    st.pyplot(fig_forecast)
