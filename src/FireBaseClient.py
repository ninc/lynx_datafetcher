import os
import pyrebase
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")
FIREBASE_AUTH_DOMAIN = os.environ.get("FIREBASE_AUTH_DOMAIN")
FIREBASE_DATABASE_URL = os.environ.get("FIREBASE_DATABASE_URL")
FIREBASE_STORAGE_BUCKET = os.environ.get("FIREBASE_STORAGE_BUCKET")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID")
FIREBASE_MESSAGING_SENDER_ID = os.environ.get("FIREBASE_MESSAGING_SENDER_ID")
FIREBASE_APP_ID = os.environ.get("FIREBASE_APP_ID")
FIREBASE_MEASUREMENT_ID = os.environ.get("FIREBASE_MEASUREMENT_ID")
FIREBASE_USERNAME = os.environ.get("FIREBASE_USERNAME")
FIREBASE_PASSWORD = os.environ.get("FIREBASE_PASSWORD")

class FireBaseClient:

    def __init__(self, verbose=False):
        self._check_env()
        self._firebase_config = self._create_firebase_config()
        self._firebase = pyrebase.initialize_app(self._firebase_config)
        self._db = self._firebase.database()
        self._auth = self._firebase.auth()
        self._user = self._auth.sign_in_with_email_and_password(FIREBASE_USERNAME, FIREBASE_PASSWORD)

    def _check_env(self):
        assert FIREBASE_API_KEY is not None
        assert FIREBASE_AUTH_DOMAIN is not None
        assert FIREBASE_DATABASE_URL is not None
        assert FIREBASE_STORAGE_BUCKET is not None
        assert FIREBASE_PROJECT_ID is not None
        assert FIREBASE_MESSAGING_SENDER_ID is not None
        assert FIREBASE_APP_ID is not None
        assert FIREBASE_MEASUREMENT_ID is not None
        assert FIREBASE_USERNAME is not None
        assert FIREBASE_PASSWORD is not None       

    def _refresh_auth_token(self):
        self._user = self._auth.refresh(self._user['refreshToken'])

    def _create_firebase_config(self):
        firebase_config = {
          "apiKey": FIREBASE_API_KEY,
          "authDomain": FIREBASE_AUTH_DOMAIN,
          "databaseURL": FIREBASE_DATABASE_URL,
          "storageBucket": FIREBASE_STORAGE_BUCKET,
          "projectId": FIREBASE_PROJECT_ID,
          "messagingSenderId": FIREBASE_MESSAGING_SENDER_ID,
          "appId": FIREBASE_APP_ID,
          "measurementId": FIREBASE_MEASUREMENT_ID,
        }
        return firebase_config


    """ METADATA """
    def set_metadata_instruments(self, data):
        self._refresh_auth_token()
        for instrument in data['instruments']:
            instrument_id = instrument['insId']
            result = self._db.child('borsdata').child('metadata').child('instruments').child(instrument_id).update(instrument, self._user['idToken'])

    def set_metadata_countries(self, data):
        self._refresh_auth_token()
        for country in data['countries']:
            country_id = country['id']
            result = self._db.child('borsdata').child('metadata').child('countries').child(country_id).update(country, self._user['idToken'])

    def set_metadata_branches(self, data):
        self._refresh_auth_token()
        for branch in data['branches']:
            branch_id = branch['id']
            result = self._db.child('borsdata').child('metadata').child('branches').child(branch_id).update(branch, self._user['idToken'])

    def set_metadata_sectors(self, data):
        self._refresh_auth_token()
        for sector in data['sectors']:
            sector_id = sector['id']
            result = self._db.child('borsdata').child('metadata').child('sectors').child(sector_id).update(sector, self._user['idToken'])

    def set_metadata_markets(self, data):
        self._refresh_auth_token()
        for market in data['markets']:
            market_id = market['id']
            result = self._db.child('borsdata').child('metadata').child('markets').child(market_id).update(market, self._user['idToken'])

    def set_metadata_kpi(self, data):
        self._refresh_auth_token()
        for kpi in data['kpiHistoryMetadatas']:
            kpi_id = kpi['kpiId']
            result = self._db.child('borsdata').child('metadata').child('kpi_metadata').child(kpi_id).update(kpi, self._user['idToken'])

    def set_metadata_reports(self, data):
        self._refresh_auth_token()
        results = self._db.child('borsdata').child('metadata').child('reports_metadata').update(data['reportMetadatas'], self._user['idToken'])

    def set_metadata_translation(self, data):
        self._refresh_auth_token()
        results = self._db.child('borsdata').child('metadata').child('translation_metadata').update(data['translationMetadatas'], self._user['idToken'])


    """ INDIVIDUAL INSTRUMENT DATA """
    def set_report(self, instrument_id, data):
        self._refresh_auth_token()
        reports = self._db.child('borsdata').child('instrument').child(instrument_id).child('reports')
        results = reports.update(data, self._user['idToken'])

    def set_stock_prices(self, instrument_id, data):
        self._refresh_auth_token()
        stock_prices = self._db.child('borsdata').child('instrument').child(instrument_id).child('stock_prices')
        results = stock_prices.update(data, self._user['idToken'])

    """ LYNX SPECIFIC """
    def set_quality_instrument(self, instrument_id, data):
        self._refresh_auth_token()
        results = self._db.child('quality_instruments').child(instrument_id).update(data, self._user['idToken'])