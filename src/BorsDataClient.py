import os
import requests
import time
from BorsdataAPI.borsdata.borsdata_api import *
BORSDATA_API_KEY = os.environ.get("BORSDATA_API_KEY")

class BorsDataClient:

    def __init__(self, verbose=False):
        self._check_api_key()
        self._borsdata_api = BorsdataAPI(BORSDATA_API_KEY)
        self._api_key = BORSDATA_API_KEY
        self._params = {'authKey': self._api_key, 'maxYearCount': 20, 'maxR12QCount': 40, 'maxCount': 20, 'date': None, 'version': 1}
        self._url_root = 'https://apiservice.borsdata.se/v1/'
        self._last_api_call = 0
        self._api_calls_per_second = 10
        # used for tracing (api-calls in terminal)
        self._verbose = verbose

    def _check_api_key(self):
        assert BORSDATA_API_KEY is not None

    def _call_api(self, url):
        """
        internal function for api-calls
        :param url: url to be added to _url_root
        :return: json-encoded content if any
        """
        current_time = time.time()
        time_delta = current_time - self._last_api_call
        # introduce sleep if time-delta is too big to prevent error 429.
        if time_delta < 1 / self._api_calls_per_second:
            time.sleep(1 / self._api_calls_per_second - time_delta)
        response = requests.get(self._url_root + url, self._params)
        #self._debug_trace("BorsdataAPI >> calling API: " + self._url_root + url)
        self._last_api_call = time.time()
        # status_code == 200 SUCCESS!
        if response.status_code != 200:
            print(f"BorsdataAPI >> API-Error, status code: {response.status_code}")
            return response
        return response.json()

    """
    Instrument Meta
    """
    def get_branches(self):
        """
        returns branch data as json
        """
        json_data = self._call_api('branches')
        return json_data

    def get_countries(self):
        """
        returns countries data as json
        """
        json_data = self._call_api('countries')
        return json_data

    def get_markets(self):
        """
        returns market data as json
        """
        json_data = self._call_api('markets')
        return json_data

    def get_sectors(self):
        """
        returns sector data as json
        """
        json_data = self._call_api('sectors')
        return json_data

    def get_translation_meta_data(self):
        """
        returns translation metadata as json
        """
        url = 'translationmetadata'
        json_data = self._call_api(url)
        translation_data = pd.json_normalize(json_data['translationMetadatas'])
        return translation_data

    """
    Instruments
    """
    def get_instruments(self):
        """
        returns instrument data as json
        """
        url = 'instruments'
        json_data = self._call_api(url)
        # TODO, DO WE NEED TO NORMALIZE?
        #instruments = pd.json_normalize(json_data['instruments'])
        #instruments['listingDate'] = pd.to_datetime(instruments['listingDate'])
        #return instruments
        return json_data

    def get_instruments_updated(self):
        """
        returns all updated instruments as json
        """
        url = 'instruments/updated'
        json_data = self._call_api(url)
        # TODO, DO WE NEED TO NORMALIZE?
        #instruments = pd.json_normalize(json_data['instruments'])
        #print(instruments.tail())
        #return instruments
        return json_data

    """
    KPIs
    """
    # TODO, fix json format
    def get_kpi_history(self, ins_id, kpi_id, report_type, price_type):
        url = f"instruments/{ins_id}/kpis/{kpi_id}/{report_type}/{price_type}/history"
        json_data = self._call_api(url)
        # creating dataframes from json-data
        print(json_data)
        kpi_history = pd.DataFrame.from_dict(json_data['values'], orient='columns')
        # the structure of the data-columns received are; 'y' year, 'p' period, 'v' value (kpi).
        # renaming the columns
        kpi_history.rename(columns={"y": "year", "p": "period", "v": "kpi_value"}, inplace=True)
        kpi_history.fillna(0, inplace=True)
        return kpi_history

    # TODO, fix json format
    def get_kpi_summary(self, ins_id, report_type):
        """
        returns kpi summary for instrument
        :param ins_id: instrument id
        :param report_type: report type ['quarter', 'year', 'r12']
        :return: json object
        """
        url = f"instruments/{ins_id}/kpis/{report_type}/summary"
        json_data = self._call_api(url)
        return json_data

    # TODO, fix json format
    def get_kpi_data_instrument(self, ins_id, kpi_id, calc_group, calc):
        """
        get screener data, for more information: https://github.com/Borsdata-Sweden/API/wiki/KPI-Screener
        :param ins_id: instrument id
        :param kpi_id: kpi id
        :param calc_group: ['1year', '3year', '5year', '7year', '10year', '15year']
        :param calc: ['high', 'latest', 'mean', 'low', 'sum', 'cagr']
        :return: json object
        """
        url = f"instruments/{ins_id}/kpis/{kpi_id}/{calc_group}/{calc}"
        json_data = self._call_api(url)
        print(json_data)
        return json_data

    # TODO, fix json format
    def get_kpi_data_all_instruments(self, kpi_id, calc_group, calc):
        """
        get kpi data for all instruments
        :param kpi_id: kpi id
        :param calc_group: ['1year', '3year', '5year', '7year', '10year', '15year']
        :param calc: ['high', 'latest', 'mean', 'low', 'sum', 'cagr']
        :return: json object
        """
        url = f"instruments/kpis/{kpi_id}/{calc_group}/{calc}"
        json_data = self._call_api(url)
        print(json_data)
        return json_data

    # TODO, fix json format
    def get_updated_kpis(self):
        """
        get latest calculation time for kpis
        :return: json object
        """
        url = f"instruments/kpis/updated"
        json_data = self._call_api(url)
        return json_data

    # TODO, fix json format
    def get_kpi_metadata(self):
        """
        get kpi metadata
        :return: json object
        """
        url = f"instruments/kpis/metadata"
        json_data = self._call_api(url)
        return json_data

    """
    Reports
    """
    # TODO, fix json format
    def get_instrument_report(self, ins_id, report_type):
        """
        get specific report data
        :param ins_id: instrument id
        :param report_type: ['quarter', 'year', 'r12']
        :return: pd.DataFrame of report data
        """
        url = f"instruments/{ins_id}/reports/{report_type}"
        json_data = self._call_api(url)
        reports = pd.DataFrame.from_dict(json_data['reports'], orient='columns')
        return reports

    # TODO, fix json format
    def get_instrument_reports(self, ins_id):
        """
        get all report data
        :param ins_id:
        :return: [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
        """
        # constructing url for api-call, adding ins_id
        url = f'instruments/{ins_id}/reports'
        json_data = self._call_api(url)
        # creating dataframes from json-data
        reports_year = pd.DataFrame.from_dict(json_data['reportsYear'], orient='columns')
        reports_quarter = pd.DataFrame.from_dict(json_data['reportsQuarter'], orient='columns')
        reports_r12 = pd.DataFrame.from_dict(json_data['reportsR12'], orient='columns')
        # making the columns lower-case in all dataframes
        reports_year.columns = [x.lower() for x in reports_year.columns]
        reports_quarter.columns = [x.lower() for x in reports_quarter.columns]
        reports_r12.columns = [x.lower() for x in reports_r12.columns]
        # replacing all nans with a 0
        reports_year.fillna(0, inplace=True)
        reports_quarter.fillna(0, inplace=True)
        reports_r12.fillna(0, inplace=True)
        # sort data ascending
        reports_year = reports_year.sort_values(['year', 'period'], ascending=True)
        reports_quarter = reports_quarter.sort_values(['year', 'period'], ascending=True)
        reports_r12 = reports_r12.sort_values(['year', 'period'], ascending=True)
        return reports_quarter, reports_year, reports_r12

    # TODO, fix json format
    def get_reports_metadata(self):
        """
        get report metadata
        :return: pd.DataFrame with metadata
        """
        url = f"instruments/reports/metadata"
        json_data = self._call_api(url)
        metadata = pd.DataFrame.from_dict(json_data['reportMetadatas'], orient='columns')
        return metadata

    """
    Stockprices
    """
    # TODO, fix json format
    def get_instrument_stock_prices(self, ins_id):
        """
        get stock prices for ins_id
        :param ins_id:
        :return: pd.DataFrame()
        """
        url = f'instruments/{ins_id}/stockprices'
        json_data = self._call_api(url)
        stock_prices = pd.json_normalize(json_data['stockPricesList'])
        # re-naming the columns
        stock_prices.rename(columns={'d': 'date', 'c': 'close', 'h': 'high', 'l': 'low',
                                     'o': 'open', 'v': 'volume'}, inplace=True)
        # converting the date to a datetime-object
        stock_prices.date = pd.to_datetime(stock_prices.date)
        stock_prices.fillna(0, inplace=True)
        # setting the 'date'-column in dataframe (table/spreadsheet) as index
        stock_prices.set_index('date', inplace=True)
        # sorting by the new index (date)
        stock_prices = stock_prices.sort_index()
        return stock_prices

    # TODO, fix json format
    def get_instruments_stock_prices_last(self):
        """
        get last days' stock prices for all instruments
        :return: pd.DataFrame()
        """
        url = f'/instruments/stockprices/last'
        json_data = self._call_api(url)
        stock_prices = pd.json_normalize(json_data['stockPricesList'])
        stock_prices.rename(columns={'d': 'date', 'i': 'ins_id', 'c': 'close', 'h': 'high', 'l': 'low',
                                     'o': 'open', 'v': 'volume'}, inplace=True)
        stock_prices.fillna(0, inplace=True)
        return stock_prices

    # TODO, fix json format
    def get_stock_prices_date(self, date):
        """
        get all instrument stock prices for passed date
        :param date: date in string format, e.g. '2000-01-01'
        :return:
        """
        url = f'/instruments/stockprices/date'
        self._params['date'] = date
        json_data = self._call_api(url)
        stock_prices = pd.json_normalize(json_data['stockPricesList'])
        stock_prices.rename(columns={'d': 'date', 'i': 'ins_id', 'c': 'close', 'h': 'high', 'l': 'low',
                                     'o': 'open', 'v': 'volume'}, inplace=True)
        return stock_prices

    """
    Stocksplits
    """
    # TODO, fix json format
    def get_stock_splits(self):
        """
        get stock splits
        :return:
        """
        url = f'/instruments/stocksplits'
        json_data = self._call_api(url)
        stock_splits = pd.json_normalize(json_data['stockSplitList'])
        stock_splits['splitDate'] = pd.to_datetime(stock_splits['splitDate'] )
        return stock_splits
    
    def run(self):
        print('Running stuff')
        #print(self.get_countries())
        #print(self.get_branches())
        #print(self.get_sectors())
        #print(self.get_markets())
        print(self.get_instruments())
        #print(self.get_instruments_updated())