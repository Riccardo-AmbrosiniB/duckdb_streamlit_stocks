import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf


class PlotlyVisualizer:
    def plot_line_chart(
        self, df, x_col, y_col, title="Line Chart", x_label=None, y_label=None
    ):
        x_label = x_label or x_col
        y_label = y_label or y_col
        fig = px.line(
            df, x=x_col, y=y_col, title=title, labels={x_col: x_label, y_col: y_label}
        )
        return fig

    def plot_time_series_ma(
        self, df, x_date_col, y_stock_price_col, y_ma_col, stock_code, ma_window
    ):
        fig = px.line(
            df, x=x_date_col, y=y_stock_price_col, title=f"Stock {stock_code} Price"
        )
        fig.add_scatter(
            x=df[x_date_col],
            y=df[y_ma_col],
            mode="lines",
            name=f"{ma_window}-Day Rolling Average",
            line=dict(color="orange", dash="dash"),
        )
        return fig

    def plot_stock_returns_chart(
        self, df, x_col, y_col, marker_col, selected_stock, title="Stock returns"
    ):
        fig = go.Figure()

        # Add the daily returns, with color based on positive or negative values
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode="lines+markers",
                marker=dict(color=df[marker_col]),  # Color points conditionally
                line=dict(color="blue", width=1),  # Line color
                name=title,
            )
        )

        # Customize layout
        fig.update_layout(
            title=f"Daily Returns for {selected_stock}",
            xaxis_title="Date",
            yaxis_title="Daily Return",
            yaxis_tickformat=".2%",
            showlegend=False,
        )

        return fig


class MatplotlibVisualizer:
    def tsa_plots(self, seasonal_decompose, timeseries):
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # Adjust figsize as needed
        fig.tight_layout(pad=4.0)  # Adjust padding between plots

        # Plot each component in the first three quadrants
        seasonal_decompose.trend.plot(
            ax=axs[0, 0], title="Trend Component", color="blue"
        )
        axs[0, 0].set_xlabel("Date")
        axs[0, 0].set_ylabel("Values")

        seasonal_decompose.seasonal.plot(
            ax=axs[0, 1], title="Seasonal Component", color="orange"
        )
        axs[0, 1].set_xlabel("Date")
        axs[0, 1].set_ylabel("Values")

        seasonal_decompose.resid.plot(
            ax=axs[1, 0], title="Residual Component", color="green"
        )
        axs[1, 0].set_xlabel("Date")
        axs[1, 0].set_ylabel("Values")

        # Plot the ACF in the last quadrant
        plot_acf(timeseries, ax=axs[1, 1])  # Specify the fourth axis
        axs[1, 1].set_title("Autocorrelation Function (ACF)")

        # Adjust layout
        plt.tight_layout()
        return fig

    def prediction_plot(self, time_series, forecast, conf_int, n_periods=60):
        fig = plt.figure(figsize=(12, 6))
        time_series = time_series.tail(n_periods * 3)
        plt.plot(time_series, label="Historical Data")
        plt.plot(
            pd.date_range(time_series.index[-1], periods=n_periods, freq="D"),
            forecast,
            label="Forecast",
        )
        plt.fill_between(
            pd.date_range(time_series.index[-1], periods=n_periods, freq="D"),
            conf_int[:, 0],
            conf_int[:, 1],
            color="pink",
            alpha=0.3,
        )
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.title("Stock Price Forecast")
        plt.legend()
        plt.grid()
        return fig
