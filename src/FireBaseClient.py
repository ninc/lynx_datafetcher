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

    def set_instruments(self, data):
        results = self._db.child('metadata').child('instruments').set(data['instruments'], self._user['idToken'])

    def set_countries(self, data):
        results = self._db.child('metadata').child('countries').set(data['countries'], self._user['idToken'])

    def set_branches(self, data):
        results = self._db.child('metadata').child('branches').set(data['branches'], self._user['idToken'])

    def set_sectors(self, data):
        results = self._db.child('metadata').child('sectors').set(data['sectors'], self._user['idToken'])

    def set_markets(self, data):
        results = self._db.child('metadata').child('markets').set(data['markets'], self._user['idToken'])

    def set_kpi_metadata(self, data):
        results = self._db.child('metadata').child('kpi_metadata').set(data['kpiHistoryMetadatas'], self._user['idToken'])

    def set_reports_metadata(self, data):
        results = self._db.child('metadata').child('reports_metadata').set(data['reportMetadatas'], self._user['idToken'])
