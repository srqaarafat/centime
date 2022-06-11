from jsonschema import validators
from datetime import datetime
from src.alpha_vantage_constants import AlphaVantageConstants
from src.api_base import ApiBase


class AlphaViews(ApiBase):

    def __init__(self, properties, env, request_api_series):
        """
        :param properties:
        :param env:
        """
        self.properties = properties
        self.env = env
        self.url = self.properties.get(self.env, self.env+"_api")
        self.request_api_series = request_api_series
        self.response = ""
        self.response_body = ""
        self.month_data = {
            "01": "31", "02": "28", "03": "31", "04": "30", "05": "31",
            "06": "30", "07": "31", "08": "31", "09": "30", "10": "31", "11": "30", "12": "31"
        }
        super(AlphaViews, self).__init__(self.url)

    def get_series(self) -> str:
        switch = {
            "iseries": AlphaVantageConstants.intra_day_function,
            "ieseries": AlphaVantageConstants.intra_day_extended_function,
            "dseries": AlphaVantageConstants.daily_function,
            "daseries": AlphaVantageConstants.daily_adjusted_function,
            "wseries": AlphaVantageConstants.weekly_function,
            "waseries": AlphaVantageConstants.weekly_Adjusted_function,
            "mseries": AlphaVantageConstants.monthly_function,
            "maseries": AlphaVantageConstants.monthly_adjusted_function,

        }
        return switch.get(self.request_api_series, "No series")

    def alpha_schema_validation(self, request_api_series) -> str:
        switch = {
            "iseries": self.intra_day_schema_validation,
            "dseries": self.intra_day_schema_validation,
            "daseries": self.daily_schema_validation,
            "wseries": self.intra_day_schema_validation,
            "waseries": self.weekly_schema_validation,
            "mseries": self.intra_day_schema_validation
            # "maseries": self.,

        }
        return switch.get(request_api_series, self.default_fun)()

    def get_uri(self, type_of_series, symbol, interval=0, slice_year_month=(0, 0)) -> str:
        series = self.get_series()
        uri = "{}?function={}&symbol={}&apikey={}".format(
            self.properties.get('common', 'uri'),
            series,
            symbol,
            self.properties.get(self.env, self.env + "_api_key")
        )
        if interval:
            uri += "&interval=" + AlphaVantageConstants.min_interval(interval)

        if any(slice_year_month):
            uri += "&slice_year_month=" + AlphaVantageConstants.slice_year_month(slice_year_month[0], slice_year_month[1])
        return uri

    def get_stock_response(self, stock_type, symbol, interval=0, time_slice=(0, 0)) -> object:
        self.response = self.get_api_response(
            'get',
            self.properties.get(self.env, self.env+"_protocol"),
            self.get_uri(stock_type, symbol, interval, time_slice)
        )
        self.response_body = self.parse_response(self.response)

    def intra_day_schema_validation(self) -> None:
        for key, value in self.response_body.items():
            if 'Time' in key:
                for k, v in value.items():
                    validators.validate(v, AlphaVantageConstants.time_series_schema)
        validators.validate(self.response_body, AlphaVantageConstants.meta_deta_schema)

    def daily_schema_validation(self):
        validators.validate(self.response_body, AlphaVantageConstants.daily_series_adjusted_schema)

    def weekly_schema_validation(self):
        for key, value in self.response_body.items():
            if 'Time' in key:
                for k, v in value.items():
                    validators.validate(v, AlphaVantageConstants.weekly_adjusted_time_series_schema)
        validators.validate(self.response_body, AlphaVantageConstants.meta_deta_schema)

    def default_fun(self):
        print(self.response_body)
        pass

    def basic_response_validation(self, content_type="json"):
        assert self.response.status_code == 200, "Status validation failed {}".format(self.response.status_code)
        assert content_type in self.response.headers['Content-Type'], "Content_Type validation failed {}".format(self.response.headers['Content-Type'])

    def data_error_validation(self):
        assert 'Error Message' not in self.response_body, "Error Message in response body {}".format(self.response_body)

    def data_time_data_validation(self, month=False):
        dd = datetime.now()
        ex_month = dd.month
        ex_year = dd.year
        for k, v in self.response_body.items():
            if 'Time' in k:
                for key, value in v.items():
                    op, lw, hi, cl = float(value.get('1. open', 0.0)), float(value.get('3. low', 0)), float(
                        value.get('2. high', 0)), float(value.get('4. close', 0.0))
                    assert lw <= hi, "Trading low, high validation {}".format(value)
                    assert op <= hi or cl <= hi, "Trading open-high, close-high validation {}".format(value)
                    assert op >= lw or cl >= lw, "Trading open-low, close-low validation {}".format(value)
                    # monthly , day, year validation
                    if month:
                        yr, mt, dy = key.split("-")
                        # ex_dy = "29" if int(yr) % 4 == 0 else self.month_data.get(mt, "0")
                        # if int(yr) == dd.year and int(mt) == dd.month:
                        #     ex_dy = str(dd.day-1)
                        # assert ex_dy == dy, "{} Monthly day validation {} expected: {}".format(key, dy,  ex_dy)
                        assert ex_month == int(mt), "{} Month validation {} expected: {}".format(key, ex_month, mt)
                        assert ex_year == int(yr), "{} Year validation {} expected: {}".format(key, ex_year, yr)
                        if ex_month == 1:
                            ex_month = 12
                            ex_year -= 1
                        else:
                            ex_month -= 1
