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
            x=df[x_col],
            y=df[y_col],
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
