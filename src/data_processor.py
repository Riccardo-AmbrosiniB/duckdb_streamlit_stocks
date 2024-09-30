class DataProcessor:
    def __init__(self, conn):
        self.conn = conn

    def get_data(self):
        query = "FROM stocks"
        return self.conn.execute(query).fetch_df()

    def get_summary_stats(self):
        query = (
            "SELECT name, AVG(high) as avg_price FROM stocks GROUP BY name ORDER BY 1"
        )
        return self.conn.execute(query).fetch_df()

    def get_stock_codes(self):
        query = "SELECT DISTINCT name FROM stocks ORDER BY 1"
        return self.conn.execute(query).fetch_df()["name"].tolist()

    def get_stock_data(self, stock_code):
        query = f"SELECT date,close FROM stocks WHERE name='{stock_code}'"
        return self.conn.execute(query).fetch_df()

    def get_stock_data_rolling_average(self, stock_code, ma_window):
        query = f"""
            SELECT date, close, \
            AVG(close) OVER (PARTITION BY name ORDER BY date ROWS BETWEEN {ma_window} PRECEDING AND CURRENT ROW) AS moving_average \
            FROM stocks WHERE name = '{stock_code}';
        """
        return self.conn.execute(query).fetch_df()

    def get_stock_return(self, stock_code):
        query = f"""
            SELECT date, name, close, \
            (close - LAG(close) OVER (PARTITION BY name ORDER BY date)) / LAG(close) OVER (PARTITION BY name ORDER BY date) AS daily_return \
            FROM stocks \
            WHERE name = '{stock_code}';
        """
        return self.conn.execute(query).fetch_df()

    def get_custom_query(self, query):
        return self.conn.execute(query).fetch_df()
