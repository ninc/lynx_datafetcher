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

    # TODO FIX GET FUNCTIONS
    def set_instruments(self, data):
        instruments = self._db.child('borsdata').child('metadata').child('instruments')
        results = instruments.set(data['instruments'], self._user['idToken'])

    def set_countries(self, data):
        countries = self._db.child('borsdata').child('metadata').child('countries')
        results = countries.set(data['countries'], self._user['idToken'])

    def set_branches(self, data):
        branches = self._db.child('borsdata').child('metadata').child('branches')
        results = branches.set(data['branches'], self._user['idToken'])

    def set_sectors(self, data):
        sectors = self._db.child('borsdata').child('metadata').child('sectors')
        results = sectors.set(data['sectors'], self._user['idToken'])

    def set_markets(self, data):
        markets = self._db.child('borsdata').child('metadata').child('markets')
        results = markets.set(data['markets'], self._user['idToken'])

    def set_kpi_metadata(self, data):
        kpi_metadata = self._db.child('borsdata').child('metadata').child('kpi_metadata')
        results = kpi_metadata.set(data['kpiHistoryMetadatas'], self._user['idToken'])

    def set_reports_metadata(self, data):
        reports_metadata = self._db.child('borsdata').child('metadata').child('reports_metadata')
        results = reports_metadata.set(data['reportMetadatas'], self._user['idToken'])

    def set_translation_metadata(self, data):
        translation_metadata = self._db.child('borsdata').child('metadata').child('translation_metadata')
        results = translation_metadata.set(data['translationMetadatas'], self._user['idToken'])

    def set_report(self, instrument_id, data):
        reports = self._db.child('borsdata').child('instrument').child(instrument_id).child('reports')
        results = reports.set(data, self._user['idToken'])

    def set_stock_prices(self, instrument_id, data):
        stock_prices = self._db.child('borsdata').child('instrument').child(instrument_id).child('stock_prices')
        results = stock_prices.set(data, self._user['idToken'])