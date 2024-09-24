class DataProcessor:
    def __init__(self, conn):
        self.conn = conn

    def get_summary_stats(self):
        query = (
            "SELECT name, AVG(high) as avg_price FROM stocks GROUP BY name ORDER BY 1"
        )
        return self.conn.execute(query).fetch_df()
