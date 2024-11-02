from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima
from .logger import setup_logger

logger = setup_logger(__name__)


class Predictor:

    def season_decompose(self, timeseries, period=30):
        decomposed = seasonal_decompose(timeseries, model="additive", period=period)
        return decomposed

    def test_stationarity(self, timeseries, p_value=0.05):
        # Perform Augmented Dickey-Fuller test (ADF Test)
        result = adfuller(timeseries)
        logger.info(f"ADF Statistic: {result[0]}")
        logger.info(f"p-value: {result[1]}")

        # Check p-value and return True if we can reject the Null hyphotesis i.e. time series is stationary
        # return False otherwise.
        if result[1] < p_value:
            logger.info("Time series is stationary")
            return True
        else:
            logger.info("Time series is not stationary")
            return False

    def auto_arima(self, stock_data):
        stepwise_model = auto_arima(
            stock_data,
            start_p=1,
            start_q=1,
            max_p=10,
            max_q=10,
            seasonal=True,
            trace=True,
            suppress_warnings=True,
            stepwise=True,
        )
        return stepwise_model

    def fit_arma_model(self, timeseries, p, d, q):
        # Fit the ARMA model
        model = ARIMA(timeseries, order=(p, d, q))
        arma_model_fit = model.fit(disp=False)
        return arma_model_fit
