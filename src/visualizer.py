import plotly.express as px
import plotly.graph_objects as go


class Visualizer:
    def plot_line_chart(
        self, df, x_col, y_col, title="Line Chart", x_label=None, y_label=None
    ):
        x_label = x_label or x_col
        y_label = y_label or y_col
        fig = px.line(
            df, x=x_col, y=y_col, title=title, labels={x_col: x_label, y_col: y_label}
        )
        return fig

    def plot_time_series_ma(self, df, x_col, y_col, stock_code, ma_window):
        fig = px.line(df, x=x_col, y=y_col, title=f"Stock {stock_code} Price")
        fig.add_scatter(
            x=df["date"],
            y=df["moving_average"],
            mode="lines",
            name=f"{ma_window}-Day Rolling Average",
            line=dict(color="orange", dash="dash"),
        )
        return fig
