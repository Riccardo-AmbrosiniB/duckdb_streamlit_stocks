import plotly.express as px


class Visualizer:
    def plot_line_chart(self, df, x_col, y_col, title="Line Chart"):
        fig = px.line(df, x=x_col, y=y_col, title=title)
        return fig
