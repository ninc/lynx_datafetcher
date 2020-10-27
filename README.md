# lynx_datafetcher

# Setup

## .env file
Create the file .env with your BorsData credentials

Example .env file:
BORSDATA_API_KEY=
FIREBASE_API_KEY=
FIREBASE_AUTH_DOMAIN=
FIREBASE_DATABASE_URL=
FIREBASE_STORAGE_BUCKET=
FIREBASE_PROJECT_ID=
FIREBASE_MESSAGING_SENDER_ID=
FIREBASE_APP_ID=
FIREBASE_MEASUREMENT_ID=
FIREBASE_USERNAME=
FIREBASE_PASSWORD=

## Git submodule
Run the following commands to update submodules:
git submodule init
git submodule update

## Running
./run_in_docker.sh is used to start the data fetcher